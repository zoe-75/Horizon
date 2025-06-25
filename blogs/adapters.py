from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Explicitly ensure the user is not staff/superuser
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

# your_app/adapters.py


from allauth.socialaccount.helpers import render_authentication_error
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return False  # force redirect to username form

    def save_user(self, request, sociallogin, form=None):
        # Only store the sociallogin temporarily in the session
        request.session['socialaccount_sociallogin'] = sociallogin.serialize()
        return redirect('complete_social_signup')
