from django.http import Http404
from django.shortcuts import render,redirect

from .forms import ProfileForm
from .models import Profile
def profile_update_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/login?next=/profile/update')
    user = request.user
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }
    profile = user.profile
    form = ProfileForm(request.POST or None, instance=profile, initial=user_data)
    if form.is_valid():
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        profile_obj.save()
    context = {
        "form": form,
        "btn_label": "Save",
        "title": "Update Profile",
    }
    return render(request, 'profiles/form.html', context)
def profile_detail_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username__iexact=username)
    if not qs.exists():
        raise Http404("User not found")
    profile_obj = qs.first()
    is_following = False
    if request.user.is_authenticated:
        user = request.user
        is_following = user in profile_obj.followers.all()
    context = {
        "username": username,
        "profile": profile_obj,
        "is_following": is_following,
    }
    return render(request, 'profiles/detail.html',context)
def activate_view(request, *args, **kwargs):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.license_active = True  # Activate the license
        profile.save()  # Save the changes
        return redirect('/')  # Redirect to the homepage
    return render(request, 'profiles/activate_license.html')