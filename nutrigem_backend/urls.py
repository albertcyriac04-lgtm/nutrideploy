"""
URL configuration for nutrigem_backend project.
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from api.views_frontend import (
    landing, index, login_view, logs_view, coach_view, settings_view,
    add_consumption_log, add_weight_record, logout_view, register_view,
    ai_coach_api, get_diet_plan, export_report_api, add_water_api,
    log_meal_api, remove_meal_api, billing_view, process_payment_api,
    resend_otp_api
)
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', landing, name='landing'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('', include(tf_urls)),  # This includes the default two-factor auth views
    path('mfa/', include('mfa.urls')),  # Passkey support
    path('dashboard/', index, name='index'),
    path('logs/', logs_view, name='logs'),
    path('coach/', coach_view, name='coach'),
    path('settings/', settings_view, name='settings'),
    path('logout/', logout_view, name='logout'),
    path('api/add-log/', add_consumption_log, name='add_log'),
    path('api/add-weight/', add_weight_record, name='add_weight'),
    path('api/add-water/', add_water_api, name='add_water'),
    path('api/log-meal/', log_meal_api, name='log_meal'),
    path('api/remove-meal/', remove_meal_api, name='remove_meal'),
    path('api/coach/', ai_coach_api, name='ai_coach_api'),
    path('diet/', get_diet_plan, name='diet_plan'),
    path('billing/', billing_view, name='billing'),
    path('api/process-payment/', process_payment_api, name='process_payment'),
    path('api/resend-otp/', resend_otp_api, name='resend_otp'),
    path('export/report/', export_report_api, name='export_report'),
    
    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


