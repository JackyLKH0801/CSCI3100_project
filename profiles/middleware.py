from django.shortcuts import redirect
from django.urls import resolve
from .models import Profile

class LicenseKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_urls = ['/activate', '/register', '/login']
        current_url = resolve(request.path_info).url_name
        if request.path in excluded_urls or current_url in ['activate', 'register', 'login']:
            return self.get_response(request)
        if request.user.is_authenticated:  # Check if the user is logged in
            try:
                profile = Profile.objects.get(user=request.user)
                print(profile.real_license, profile.license_active)
                if profile.license_active == False:  # Check if the license key exists
                    return redirect('/activate')  # Redirect to license activation page
            except Profile.DoesNotExist:
                return redirect('/register')  # Redirect if no profile exists
        return self.get_response(request)