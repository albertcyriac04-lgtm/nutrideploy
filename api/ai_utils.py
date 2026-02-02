import google.generativeai as genai
from django.conf import settings
import json
from .models import DailyDietPlan, ConsumptionLog, WeightRecord

def generate_indian_diet(user_profile, date):
    """
    Generates a personalized Indian diet plan using Gemini.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return None
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    diet_pref = user_profile.dietary_preference
    context = f"User: {user_profile.name}, Age: {user_profile.age}, Gender: {user_profile.gender}, " \
              f"Weight: {user_profile.weight}kg, Target: {user_profile.target_weight}kg, " \
              f"Dietary Preference: {diet_pref} (Indian Cuisine)."
              
    prompt = f"{context}\n\n" \
             f"Generate a healthy 1-day Indian diet plan. Format the output as a valid JSON object with the following keys: " \
             f"'breakfast', 'breakfast_calories', 'lunch', 'lunch_calories', 'dinner', 'dinner_calories', 'snacks', 'snacks_calories', 'summary'. " \
             f"Ensure the food items are common in Indian households and respect the {diet_pref} preference. " \
             f"Calorie values should be estimated numbers based on typical portions."
             
    try:
        response = model.generate_content(prompt)
        # Pull JSON from response text (handling potential markdown)
        resp_text = response.text
        if "```json" in resp_text:
            resp_text = resp_text.split("```json")[1].split("```")[0].strip()
        elif "```" in resp_text:
            resp_text = resp_text.split("```")[1].split("```")[0].strip()
            
        diet_data = json.loads(resp_text)
        
        # Save to database
        plan, created = DailyDietPlan.objects.update_or_create(
            user_profile=user_profile,
            date=date,
            defaults={
                'breakfast': diet_data.get('breakfast', ''),
                'breakfast_calories': float(diet_data.get('breakfast_calories', 0)),
                'lunch': diet_data.get('lunch', ''),
                'lunch_calories': float(diet_data.get('lunch_calories', 0)),
                'dinner': diet_data.get('dinner', ''),
                'dinner_calories': float(diet_data.get('dinner_calories', 0)),
                'snacks': diet_data.get('snacks', ''),
                'snacks_calories': float(diet_data.get('snacks_calories', 0)),
                'summary': diet_data.get('summary', '')
            }
        )
        return plan
    except Exception as e:
        print(f"DIET GEN ERROR: {e}")
        return None

def generate_report_summary(user_profile, start_date, end_date):
    """
    Generates a high-level health report summary using Gemini.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return "API key not configured."
        
    logs = ConsumptionLog.objects.filter(user_profile=user_profile, date__range=[start_date, end_date])
    weights = WeightRecord.objects.filter(user_profile=user_profile, date__range=[start_date, end_date])
    
    total_cals = sum(log.total_calories for log in logs)
    avg_weight = sum(w.weight for w in weights) / weights.count() if weights.count() > 0 else user_profile.weight
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"Summarize the health progress for {user_profile.name} from {start_date} to {end_date}.\n" \
             f"Total Calories Consumed: {total_cals}\n" \
             f"Average Weight: {avg_weight}kg\n" \
             f"Goal Weight: {user_profile.target_weight}kg\n\n" \
             f"Provide a 3-4 sentence professional health summary with advice for the upcoming period."
             
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate summary: {e}"
