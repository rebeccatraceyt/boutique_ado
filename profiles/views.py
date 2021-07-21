from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

def profile(request):
    """ Display user profile """
    profile = get_object_or_404(UserProfile, user=request.user)

    # if user changes information on profile page:
    if request.method == 'POST':
        # create new instance of the user profile form using post data
        form = UserProfileForm(request.POST, instance=profile)

        # checks if form is valid
        if form.is_valid():
            # valid = save and send success message
            form.save()
            messages.success(request, 'Profile updated successfully')


    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)
