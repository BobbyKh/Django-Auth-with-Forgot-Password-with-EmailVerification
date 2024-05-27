import random
import string
import uuid
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash


from base.forms import ForgotPasswordForm, PasswordChangeForm, UserForm
from base.models import PasswordValidationCode



# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form = UserForm(request.POST)
                form.add_error(None, 'Invalid email or password.')
        except User.DoesNotExist:
            form = UserForm(request.POST)
            form.add_error(None, 'Invalid email or password.')
            
    else:
        form = UserForm()
    return render(request, 'registration/login.html', {'form': form})
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'registration/login.html')
            except IntegrityError:
                form.add_error('username', 'Username already exists. Please choose another one.')
    else:
        form = UserForm()
    return render(request, 'registration/signup.html',{"form":form})


def logoutView(request):
    logout(request)
    return render(request, 'registration/login.html')
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            if user is not None:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                user.validation_code = PasswordValidationCode.objects.create(user=user, validation_code=code)
                user.save()
                subject = 'Validation Code for Password Reset'
                message = render_to_string('registration/resetpasswordemail.html', {
                    'user': user,
                    'code': code,
                })
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                try:
                    send_mail(subject, message, from_email, recipient_list)
                    return render(request, 'registration/forgotpassword.html', {
                        'message': 'Validation code sent to your email.'
                    })
                except Exception as e:
                    print(e)
                    form = ForgotPasswordForm(request.POST)
                    form.add_error(None, 'Error sending email.')
            else:
                form = ForgotPasswordForm(request.POST)
                form.add_error(None, 'Email does not exist. Please try another.')
        except User.DoesNotExist:
            form = ForgotPasswordForm(request.POST)
            form.add_error(None, 'Email does not exist. Please try another.')
            
    else:
        form = ForgotPasswordForm()
    return render(request, 'registration/forgotpassword.html', {'form': form})

def verify_token(request ):
    if request.method == 'POST':
        token = request.POST['token']
        try:
            user = PasswordValidationCode.objects.get(validation_code=token)
            user.user.is_verified = True
            user.user.save()
            user.delete()
            return redirect('user_details_edit', user.user.id)
        except User.DoesNotExist:
            return render(request, 'registration/verify_token.html', {
                'message': 'Invalid token. Please try again.'
            })
    else:
        return render(request, 'registration/verify_token.html')

def user_details_edit(request, id):
    # Retrieve the user object or return a 404 error if not found
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        # Create a PasswordChangeForm instance with the user's data and request POST data
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            # Save the new password securely
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            # Redirect to the login page after changing the password
            return redirect('login')
    else:
        # If it's a GET request, create a PasswordChangeForm instance with the user's data
        form = PasswordChangeForm(user)

    # Render the template with the form
    return render(request, 'registration/edit_password.html', {"form": form})







    