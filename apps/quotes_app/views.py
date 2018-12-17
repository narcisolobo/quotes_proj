from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import User, Quote
import bcrypt

def login(request):
    if 'logged' not in request.session:
        request.session['logged'] = False
    return render(request, 'quotes_app/index.html')

def process_login(request):
    errors = User.objects.password_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        request.session['logged'] = True
        user = User.objects.filter(email=request.POST['login-email'])
        request.session['user_id'] = user[0].id
        return redirect('/quotes')

def process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        pword = request.POST['password']
        hashed = bcrypt.hashpw(pword.encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first-name'], last_name=request.POST['last-name'], email=request.POST['email'], pwhash=hashed.decode())
        user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = user[0].id
        request.session['logged'] = True
        return redirect('/quotes')

def quotes(request):
    user = User.objects.get(id=request.session['user_id'])
    all_quotes = Quote.objects.all()
    context = {
        'user':user,
        'all_quotes':all_quotes
    }
    return render(request, 'quotes_app/quotes.html', context)

def process_like(request):
    quote = Quote.objects.get(id=request.POST['quote-id'])
    quote.likes += 1
    quote.liked_by.add(User.objects.get(id=request.session['user_id']))
    quote.save()
    print(request.session['user_id'])
    return redirect('/quotes')

def process_quote(request):
    errors = Quote.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        user = User.objects.get(id=request.session['user_id'])
        Quote.objects.create(author=request.POST['author'], quote_body=request.POST['quote-body'], poster=user)
        return redirect('/quotes')

def user(request, id):
    user = User.objects.get(id=id)
    context = {
        'user':user,
    }
    return render(request, 'quotes_app/user.html', context)

def myaccount(request, id):
    user = User.objects.get(id=id)
    context = {
        'user':user,
    }
    return render(request, 'quotes_app/myaccount.html', context)

def edit_user(request):
    user = User.objects.get(id=request.session['user_id'])
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/myaccount/'+str(user.id))
    else:
        user = User.objects.get(id=request.session['user_id'])
        user.first_name = request.POST['first-name']
        user.last_name = request.POST['last-name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'Account successfully updated!')
        return redirect('/user/'+str(user.id))

def logout(request):
    request.session.clear()
    return redirect('/login')