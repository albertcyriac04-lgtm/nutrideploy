# DELETE_THESE_FILES.ps1
# Run this script once in PowerShell from d:\nutridiet to permanently remove
# all files that were cleaned up / merged / deprecated.
# 
# Usage:  cd d:\nutridiet ; .\DELETE_THESE_FILES.ps1

$toDelete = @(
    # Empty Django-generated stubs (content is in api/models.py and api/admin.py)
    "apps\admin_app\models.py",
    "apps\admin_app\views.py",
    "apps\user_app\models.py",
    "apps\user_app\admin.py",

    # Merged into api/views.py (backwards-compat re-export only)
    "apps\api\views_frontend.py",

    # Merged into nutrigem_backend/settings_base.py
    "nutrigem_backend\settings_local.py",

    # One-off dev utility scripts / logs
    "test_smtp.py",
    "otp_error_log.txt",

    # Stale backup / IDE metadata / redundant docs
    "backups\db_backup_20260307_185520.json",
    "docs\project_structure.md",
    "metadata.json",
    "project_details.txt",
    "nutridiet_technical_guide.pdf"
)

foreach ($f in $toDelete) {
    $full = Join-Path $PSScriptRoot $f
    if (Test-Path $full) {
        Remove-Item $full -Force
        Write-Host "Deleted: $f"
    } else {
        Write-Host "Not found (skipped): $f"
    }
}

# Remove now-empty directories
@("backups", "docs") | ForEach-Object {
    $dir = Join-Path $PSScriptRoot $_
    if ((Test-Path $dir) -and -not (Get-ChildItem $dir)) {
        Remove-Item $dir -Force
        Write-Host "Removed empty dir: $_"
    }
}

Write-Host "`nCleanup complete."
