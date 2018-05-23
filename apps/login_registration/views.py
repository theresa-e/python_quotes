from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'login_registration/index.html')

def register(request):
    print('-'*30+'> ' 'The registration form was submitted.')
    errors = User.objects.basic_validator(request.POST)

    # Validate form, check if email already exists in database.
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print('-'*30+'> ', 'Errors: ', errors)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        # Save user info to form input
        if 'first_name' not in request.session:
            request.session['first_name'] = request.POST['first_name']  
        request.session['first_name'] = request.POST['first_name']  
        if 'last_name' not in request.session:
            request.session['last_name'] = request.POST['last_name']
        request.session['last_name'] = request.POST['last_name']
        if 'email' not in request.session:
            request.session['email'] = request.POST['email']
        request.session['email'] = request.POST['email']
        if 'welcome_msg' not in request.session:
            request.session['welcome_msg'] = 'You\'re now a registered user.'
        request.session['welcome_msg'] = 'You\'re now a registered user.'
        if 'userid' not in request.session:
            request.session['userid'] = user.id
        print('-'*30+'> ', 'A new user was created!')
        print('-'*30+'> ', 'Current users:\n', User.objects.all())
        return redirect('/success')

def login(request):
    # Save login email to form input
    if 'login_email' not in request.session:
        request.session['login_email'] = request.POST['login_email']
    request.session['login_email'] = request.POST['login_email']

    # Validate user input, make sure form is complete and filled out.
    # Check to see if user exists and password is valid.
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print('-'*30+'> ', 'Errors: ', errors)
        return redirect('/')

    else:
        user = User.objects.get(email=request.POST['login_email'])
        if 'first_name' not in request.session:
            request.session['first_name'] = user.first_name 
        request.session['first_name'] = user.first_name 
        if 'welcome_msg' not in request.session:
            request.session['welcome_msg'] = 'You\'ve logged in successfully.'
        request.session['welcome_msg'] = 'You\'ve logged in successfully.'
        if 'userid' not in request.session:
            request.session['userid'] = user.id
        request.session['userid'] = user.id
        print('-'*30+'> ', 'The user id is', request.session['userid'])
        print('-'*30+'> ', 'Password is correct!')
        print('-'*30+'> ', 'User logged in successfully. ')
        return redirect('/success')

def success(request):
    if 'userid' in request.session:
        context = {
            'users' : User.objects.all(),
            'quotes' : Quote.objects.all()
        }
        print('-'*30+'> ', 'User has been logged in.')
        return render(request, 'login_registration/quotes.html', context)
    else:
        print('-'*30+'> ', 'Someone tried to access /success without logging in.')
        return redirect('/')

def logout(request):
    request.session.flush()
    print('-'*30+'> ', 'User has been logged oout.')
    return redirect('/')

def process_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print('-'*30+'> ', 'Errors: ', errors)
        return redirect('/success')
    else:
        return redirect('/success')

def delete_quote(request):
    quote_to_delete = Quote.objects.get(id=request.POST['quote_id'])
    quote_to_delete.delete()
    return redirect('/success')

def user_info(request, id):
    user = User.objects.get(id=id)
    quotes = Quote.objects.filter(uploaded_by=id)
    context = {
        'user': user,
        'quotes': quotes
    }
    return render(request, 'login_registration/userinfo.html', context)

def update_info(request, id):
    if 'userid' in request.session:
        user = User.objects.get(id=id)
        context = {
            'user' : user
        }
        return render(request, 'login_registration/edituser.html', context)
    else:
        print('Noooooooooooooo')
        return redirect('/')

def process_update(request):
    errors = User.objects.update_info_validator(request.POST)
    update_user = User.objects.get(id=request.POST['userid'])
    print(id)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print('-'*30+'> ', 'Errors: ', errors)
        return redirect(reverse('edit_user', kwargs={'id' : update_user.id}))
    else:
        update_user.first_name=request.POST['first_name']
        update_user.last_name=request.POST['last_name']
        update_user.email=request.POST['email']
        update_user.save()
        request.session['first_name'] = update_user.first_name 
        return redirect('/success')

def like_quote(request):
    user = User.objects.get(id=request.POST['userid'])
    quote = Quote.objects.get(id=request.POST['quote_id'])
    user.liked_quotes.add(quote)
    return redirect ('/success')