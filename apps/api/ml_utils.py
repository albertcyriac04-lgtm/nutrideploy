from datetime import timedelta
from django.utils import timezone
from .models import WeightRecord

def predict_weight_trend(user_profile, days_ahead=7):
    """
    Predicts the user's weight using simple linear regression (pure Python).
    Returns:
        prediction (dict): {
            'predicted_weight': float or None,
            'confidence_score': float, (r-squared equivalent)
            'trend': 'Upward', 'Downward', or 'Stable',
            'slope': float,
            'intercept': float,
            'message': str
        }
    """
    records = WeightRecord.objects.filter(user_profile=user_profile).order_by('date')
    n = records.count()
    
    if n < 3:
        return {
            'predicted_weight': None,
            'confidence_score': 0,
            'trend': 'Insufficient Data',
            'slope': 0,
            'intercept': 0,
            'message': "Need at least 3 weight records to predict trends."
        }

    first_date = records.first().date
    x_list = [(r.date - first_date).days for r in records]
    y_list = [r.weight for r in records]

    # Simple Linear Regression: y = mx + b
    sum_x = sum(x_list)
    sum_y = sum(y_list)
    sum_xy = sum(x * y for x, y in zip(x_list, y_list))
    sum_xx = sum(x * x for x in x_list)

    denominator = (n * sum_xx - sum_x**2)
    if denominator == 0:
        return {
            'predicted_weight': y_list[-1],
            'confidence_score': 1.0,
            'trend': 'Stable',
            'slope': 0,
            'intercept': y_list[-1],
            'message': "Data is perfectly vertical or single-point equivalent."
        }

    m = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - m * sum_x) / n

    # Simple R-squared calculation
    y_mean = sum_y / n
    ss_tot = sum((y - y_mean)**2 for y in y_list)
    if ss_tot == 0:
        r_squared = 1.0
    else:
        ss_res = sum((y - (m * x + b))**2 for x, y in zip(x_list, y_list))
        r_squared = 1 - (ss_res / ss_tot)

    today_days = (timezone.now().date() - first_date).days
    target_day = today_days + days_ahead
    predicted_weight = m * target_day + b
    
    attainment_date = None
    target_weight = user_profile.target_weight
    if abs(m) > 0.001:
        target_days_from_start = (target_weight - b) / m
        if target_days_from_start > today_days:
            attainment_date = first_date + timedelta(days=int(target_days_from_start))
    
    if m > 0.05:
        trend = "Upward"
        message = f"Trending slightly up. Predicted weight in {days_ahead} days: {predicted_weight:.1f}kg."
    elif m < -0.05:
        trend = "Downward"
        message = f"Trending down. Great progress! Predicted weight in {days_ahead} days: {predicted_weight:.1f}kg."
    else:
        trend = "Stable"
        message = f"Weight is stable. Predicted weight in {days_ahead} days: {predicted_weight:.1f}kg."

    return {
        'predicted_weight': round(float(predicted_weight), 2),
        'attainment_date': attainment_date.strftime('%Y-%m-%d') if attainment_date else "Not projected",
        'confidence_score': round(float(r_squared), 2),
        'trend': trend,
        'slope': round(float(m), 3),
        'intercept': round(float(b), 2),
        'message': message
    }
