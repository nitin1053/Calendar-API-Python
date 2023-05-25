from django.urls import path
from calendar_app.views import GoogleCalendarInitView, GoogleCalendarRedirectView



app_name = 'calendar_app'  # Replace 'calendar_app' with your app name

urlpatterns = [
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='google-calendar-init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='google-calendar-redirect'),
]



