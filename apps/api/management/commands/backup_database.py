import gzip
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command


class Command(BaseCommand):
    help = "Create a database backup and optionally upload it to Supabase Storage."

    def add_arguments(self, parser):
        parser.add_argument(
            "--format",
            choices=["sql", "json"],
            default="sql",
            help="Backup format. Use sql for MySQL dump, json for Django dumpdata.",
        )
        parser.add_argument(
            "--upload-supabase",
            action="store_true",
            help="Upload the backup file to Supabase Storage.",
        )
        parser.add_argument(
            "--bucket",
            default="",
            help="Supabase Storage bucket name. Falls back to SUPABASE_STORAGE_BUCKET or SUPABASE_BUCKET.",
        )
        parser.add_argument(
            "--path-prefix",
            default="db-backups",
            help="Folder path inside the bucket.",
        )
        parser.add_argument(
            "--no-compress",
            action="store_true",
            help="Disable gzip compression for the backup file.",
        )

    def handle(self, *args, **options):
        backup_format = options["format"]
        upload_supabase = options["upload_supabase"]
        bucket = options["bucket"] or os.getenv("SUPABASE_STORAGE_BUCKET") or os.getenv("SUPABASE_BUCKET")
        path_prefix = options["path_prefix"].strip("/").strip()
        compress = not options["no_compress"]

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(settings.BASE_DIR) / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)

        extension = "sql" if backup_format == "sql" else "json"
        backup_file = backup_dir / f"db_backup_{timestamp}.{extension}"

        if backup_format == "sql":
            try:
                self._create_sql_dump(backup_file)
                self.stdout.write(self.style.SUCCESS(f"SQL backup created: {backup_file}"))
            except CommandError as exc:
                self.stdout.write(self.style.WARNING(f"SQL backup failed: {exc}"))
                self.stdout.write(self.style.WARNING("Falling back to JSON backup."))
                backup_file = backup_dir / f"db_backup_{timestamp}.json"
                self._create_json_dump(backup_file)
                self.stdout.write(self.style.SUCCESS(f"JSON backup created: {backup_file}"))
        else:
            self._create_json_dump(backup_file)
            self.stdout.write(self.style.SUCCESS(f"JSON backup created: {backup_file}"))

        final_file = backup_file
        if compress:
            final_file = self._gzip_file(backup_file)
            self.stdout.write(self.style.SUCCESS(f"Compressed backup: {final_file}"))

        if upload_supabase:
            if not bucket:
                raise CommandError("Missing Supabase bucket. Set --bucket or SUPABASE_STORAGE_BUCKET.")
            object_name = f"{path_prefix}/{final_file.name}" if path_prefix else final_file.name
            self._upload_to_supabase(final_file, bucket=bucket, object_name=object_name)
            self.stdout.write(self.style.SUCCESS(f"Uploaded to Supabase: {bucket}/{object_name}"))

        self.stdout.write(self.style.SUCCESS(f"Backup complete: {final_file}"))

    def _create_sql_dump(self, output_file: Path):
        db = settings.DATABASES["default"]
        engine = db.get("ENGINE")
        if engine == "django.db.backends.mysql":
            self._create_mysql_dump(output_file, db)
        elif engine == "django.db.backends.postgresql":
            self._create_postgres_dump(output_file, db)
        else:
            raise CommandError("SQL backup currently supports MySQL and PostgreSQL only.")

    def _create_mysql_dump(self, output_file: Path, db: dict):
        mysqldump_cmd = shutil.which("mysqldump")
        if not mysqldump_cmd:
            raise CommandError("mysqldump command not found in PATH.")

        command = [
            mysqldump_cmd,
            "-h",
            str(db.get("HOST") or "localhost"),
            "-P",
            str(db.get("PORT") or "3306"),
            "-u",
            str(db.get("USER") or "root"),
            "--single-transaction",
            "--skip-lock-tables",
            "--routines",
            "--triggers",
            str(db.get("NAME")),
        ]

        env = os.environ.copy()
        db_password = str(db.get("PASSWORD") or "")
        if db_password:
            env["MYSQL_PWD"] = db_password

        self._run_dump_command(command, output_file, env)

    def _create_postgres_dump(self, output_file: Path, db: dict):
        pg_dump_cmd = shutil.which("pg_dump")
        if not pg_dump_cmd:
            raise CommandError("pg_dump command not found in PATH.")

        command = [
            pg_dump_cmd,
            "-h",
            str(db.get("HOST") or "localhost"),
            "-p",
            str(db.get("PORT") or "5432"),
            "-U",
            str(db.get("USER") or "postgres"),
            "-d",
            str(db.get("NAME") or "postgres"),
            "--no-owner",
            "--no-privileges",
        ]

        env = os.environ.copy()
        db_password = str(db.get("PASSWORD") or "")
        if db_password:
            env["PGPASSWORD"] = db_password

        self._run_dump_command(command, output_file, env)

    def _run_dump_command(self, command: list[str], output_file: Path, env: dict):
        with output_file.open("wb") as out_file:
            result = subprocess.run(
                command,
                stdout=out_file,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )

        if result.returncode != 0:
            error_text = (result.stderr or b"").decode("utf-8", errors="ignore").strip()
            raise CommandError(error_text or "SQL dump command failed.")

    def _create_json_dump(self, output_file: Path):
        with output_file.open("w", encoding="utf-8") as out_file:
            call_command(
                "dumpdata",
                "--natural-foreign",
                "--natural-primary",
                "--exclude=contenttypes",
                "--exclude=auth.permission",
                "--indent=2",
                stdout=out_file,
            )

    def _gzip_file(self, file_path: Path) -> Path:
        gz_path = file_path.with_suffix(file_path.suffix + ".gz")
        with file_path.open("rb") as source, gzip.open(gz_path, "wb") as target:
            shutil.copyfileobj(source, target)
        file_path.unlink(missing_ok=True)
        return gz_path

    def _upload_to_supabase(self, file_path: Path, bucket: str, object_name: str):
        supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

        if not supabase_url:
            raise CommandError("Missing SUPABASE_URL.")
        if not supabase_key:
            raise CommandError("Missing SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_ANON_KEY).")

        encoded_object = quote(object_name)
        endpoint = f"{supabase_url}/storage/v1/object/{bucket}/{encoded_object}"
        content_type = "application/gzip" if file_path.suffix == ".gz" else "application/octet-stream"

        data = file_path.read_bytes()
        request = Request(
            endpoint,
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {supabase_key}",
                "apikey": supabase_key,
                "Content-Type": content_type,
                "x-upsert": "true",
            },
        )

        try:
            with urlopen(request, timeout=60) as response:
                status = getattr(response, "status", 200)
                if status not in (200, 201):
                    raise CommandError(f"Supabase upload failed with status {status}.")
        except Exception as exc:  # noqa: BLE001
            raise CommandError(f"Supabase upload failed: {exc}") from exc
