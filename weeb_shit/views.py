from typing import Text
from django.db import reset_queries
from django.db.models import query
from django.db.models.fields import NullBooleanField
from django.http import HttpResponse,JsonResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core import serializers
import requests
import csv
import re
from weeb_shit.models import Profile, fivestars, list_of_anime, auto_complete, anime_database, fourstars, threestars, twostars, onestars
from .forms import ProfileForm, UserForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .viewsfunctions import seen, addanime, watched, createuser, updatewatchedgenre, reccanime
from .recc import AnimeRecommender
# Create your views here.

def index(request):
    all_anime = {}
    if request.method == 'POST':
        recommend = request.POST.get('recommend', False)
        if recommend:
            currentuser = Profile.objects.get(user=request.user)
            allwatchedgenres = currentuser.watchedgenre_set.all().order_by('count')
            favgenre = [allwatchedgenres[0], allwatchedgenres[1], allwatchedgenres[2]]
            q = anime_database.objects.filter(genre__icontains=favgenre[0].name).filter(genre__icontains=favgenre[1].name).filter(genre__icontains=favgenre[2].name).exclude(score__iexact="Unknown").order_by('-score')
            print (q)
            return render(request, 'recommend.html',{'q':q})
        else:
            name = request.POST['name']
            
            all_anime = anime_database.objects.filter(name__icontains=name, score__gte='6', numofep__gte='0').order_by('-id')
            return redirect('/list_of_anime?name=' + name)
    else:
        return render(request, 'index3.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else: 
            messages.info(request,'Credentials invalid')
            return redirect('/login')
    else:
        return render(request, 'login2.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password = password)
                user.save()
                createuser(user)
                return redirect('/login')
        else:
            messages.info(request, 'Password is not the same')
            return redirect('register')
    else:
        return render(request, 'register2.html')

def lists(request):
    all_anime = {}
    if request.method == 'POST':
        name = request.POST['name']
        all_anime = anime_database.objects.filter(name__icontains=name, score__gte='6', numofep__gte='0').order_by('-id')
    obj = anime_database.objects.all()
    
    return render(request, 'list_of_anime2.html', {'all_anime':all_anime, 'obj':obj})


def animes(request, id):
    recc = AnimeRecommender.get_instance()
    if request.user.is_authenticated:
        currentuser = Profile.objects.get(user=request.user)
        anime = anime_database.objects.get(id=id)
        anime_id = id
        if request.method == 'POST':
            add = request.POST.get('submit', False)
            delete = request.POST.get('delete', False)
            change = request.POST.get('Change', False)
            print()
            if add:
                rating = request.POST.get('rating')
                addanime(currentuser, rating, anime_id)
                currentuser.favgenre()
                print(currentuser.fav)
                return redirect('/animes/'+ anime_id)

            elif delete:
                currentuser.fivestars.animes.remove(anime)
                currentuser.fourstars.animes.remove(anime)
                currentuser.threestars.animes.remove(anime)
                currentuser.twostars.animes.remove(anime)
                currentuser.onestars.animes.remove(anime)
                return redirect('/animes/'+anime_id)
        
            elif change:
                currentuser.fivestars.animes.remove(anime)
                currentuser.fourstars.animes.remove(anime)
                currentuser.threestars.animes.remove(anime)
                currentuser.twostars.animes.remove(anime)
                currentuser.onestars.animes.remove(anime)
                updatewatchedgenre(anime_id, currentuser, "remove")
                rating = request.POST['rating']
                addanime(currentuser, rating, anime_id)
                return redirect('/animes/'+anime_id)

        saw = watched(currentuser, anime_id)
    else:
        saw = {}
    
    anime_example = anime_database.objects.get(id=id)
    similar_anime_MAL_IDs = recc.get_recommendations(anime_example.MAL_ID, 5)
    similar_anime_examples = []
    for m_id in similar_anime_MAL_IDs:
        similar_anime_examples.append(anime_database.objects.get(MAL_ID=m_id))
    #print(anime_example)
    return render(request, 'individual_anime2.html',{'anime_example':anime_example, 'saw':saw, 'similar_anime_examples': similar_anime_examples})

@login_required
@transaction.atomic
def profile(request):
   
    currentuser = Profile.objects.get(user=request.user)
    watchedanime = seen(currentuser)
    five = watchedanime['5']
    four = watchedanime['4']
    three = watchedanime['3']
    two = watchedanime['2']
    one = watchedanime['1']

    all_anime = {}
    if request.method == 'POST':
        print(request.POST['name'])
        name = request.POST['name']
        all_anime = anime_database.objects.filter(name__icontains=name, score__gte='6', numofep__gte='0').order_by('-id')
        return redirect('/list_of_anime?name=' + name)
    else:
        obj = anime_database.objects.all()
        return render(request, 'profile3.html', {'obj':obj, 'five':five, 'four': four, 'three': three, 'two':two, 'one':one})

def search(request):
    name = request.GET.get('name')
    results = []
    if name:
        related = anime_database.objects.filter(name__icontains=name)

        for search in related:
            results.append(search)

        search_result = [ob.as_json() for ob in results]
                  
    return JsonResponse({'status':200, 'data':search_result})

@login_required
@transaction.atomic
def update(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('/profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'update2.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
