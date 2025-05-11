from django.shortcuts import redirect
from .models import Profile

class LicenseKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:  # Check if the user is logged in
            try:
                profile = Profile.objects.get(user=request.user)
                print(profile.license)
                if not profile.license:  # Check if the license key exists
                    return redirect('/register?showLicenseRequired=true')  # Redirect to license activation page
            except Profile.DoesNotExist:
                return redirect('/register?showProfileDoesNotExist=true')  # Redirect if no profile exists
        return self.get_response(request)