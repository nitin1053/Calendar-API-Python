from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.views import View
from google_auth_oauthlib.flow import Flow
from httplib2 import RedirectLimit

from cal_intern import settings

class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CONFIG['web'],
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        # Save the state to session for validation in the redirect view
        request.session['oauth_state'] = state

        return RedirectLimit(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        state = request.GET.get('state', None)
        code = request.GET.get('code', None)

        if state != request.session.get('oauth_state'):
            return HttpResponseBadRequest('Invalid state parameter')

        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CONFIG['web'],
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
        )

        # Exchange authorization code for access token
        flow.fetch_token(code=code)

        # Get the access token
        credentials = flow.credentials
        access_token = credentials.token

        # Use the access token to fetch the list of events from the user's calendar
        # Implement your logic here to fetch the events using the Google Calendar API

        return HttpResponse('Events fetched successfully')



