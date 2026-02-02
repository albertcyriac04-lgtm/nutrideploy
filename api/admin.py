from django.contrib import admin
from .models import UserProfile, FoodItem, ConsumptionLog, WeightRecord, WaterLog, DailyMealLog, SubscriptionPlan, Transaction


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'weight', 'target_weight', 'activity_multiplier', 'created_at']
    list_filter = ['gender', 'activity_multiplier', 'created_at']
    search_fields = ['name']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'calories', 'protein', 'carbs', 'fats', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(ConsumptionLog)
class ConsumptionLogAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'date', 'meal_type', 'food_item', 'quantity', 'total_calories', 'created_at']
    list_filter = ['meal_type', 'date', 'created_at']
    search_fields = ['user_profile__name', 'food_item__name']
    date_hierarchy = 'date'


@admin.register(WeightRecord)
class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'date', 'weight', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['user_profile__name']
    date_hierarchy = 'date'


@admin.register(WaterLog)
class WaterLogAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'date', 'amount_glasses', 'target_glasses']
    list_filter = ['date']

@admin.register(DailyMealLog)
class DailyMealLogAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'date', 'total_calories_consumed']
    list_filter = ['date']

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'updated_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user_profile', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['transaction_id', 'user_profile__name']
    readonly_fields = ['transaction_id', 'created_at']
