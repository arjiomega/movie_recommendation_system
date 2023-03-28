from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import HttpResponse


from .models import UserRating,MovieInfo,UserInfo
import requests
import json
import os

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
from config import *

tmdb_api_key = TMDB_API_KEY
base_url = 'https://api.themoviedb.org/3/'
rs_url = RS_URL

def loadUserData(user_id,get=['user_data']):

    user_data = {}

    #USER DATA INFO
    if 'user_data' in get:
        user_data['movies_watched'] = []
        loadUserRating = UserRating.objects.filter(user_id=int(user_id))
        for movie_info in loadUserRating:
            # get movie title from tmdb_id
            movie = movie_info.tmdb_id
            url = f"{base_url}/movie/{movie}?api_key={tmdb_api_key}&language=en-US"
            response = requests.get(url)
            movie_detail = json.loads(response.text)
            user_data['movies_watched'].append({"tmdb_id":movie_info.tmdb_id,
                                                "title":movie_detail['original_title'],
                                                "rating":int(movie_info.rating)
                                                })

    #MOVIE INFO
    if 'movie_info' in get:
        url = f'{base_url}/genre/movie/list?api_key={tmdb_api_key}&language=en-US'
        response = requests.get(url)
        genre_json = json.loads(response.text)

        genre_list = []
        genre_ids = []
        for i in genre_json['genres']:
            genre_list.append(i['name'])
            genre_ids.append(i['id'])

        user_data['get_genre_id'] = {genre_list[i]: genre_ids[i] for i in range(len(genre_list))}

    return user_data

def home_view(request):
    context = {}
    home_cache = cache.get('home')
    recommend_cache = cache.get('recommend')

    if 'user_id' in request.session:
        context['session'] = True
        context['user_id'] = request.session.get('user_id')
        user_data = request.session['user_data']
        context['movies_watched'] = [movie['tmdb_id'] for movie in user_data['movies_watched']]
        if not recommend_cache:
            response =requests.post(url=rs_url,
                                    json={
                                        "user_id": context['user_id'],
                                        "movie_list": context['movies_watched']
                                    })
            output_ = json.loads(response.text)

            recommend_id_list = [movie['id'] for movie in output_['data']['predict']['recommended_movies']]

            context['recommend_poster'] = []
            for tmdb_id in recommend_id_list:
                url = f'{base_url}/movie/{tmdb_id}?api_key={tmdb_api_key}&language=en-US'
                response = requests.get(url)
                output_ = json.loads(response.text)
                context['recommend_poster'].append(output_['poster_path'])

            # keep for 5 minutes. after that, update recommend for user again
            cache.set('recommend', context['recommend_poster'], timeout=60*5)
        else:
            context['recommend_poster'] = recommend_cache

    else:
        context['session'] = False

    if not home_cache:
        # popular movies request (Get 10 image links)
        url = f'{base_url}/movie/popular?api_key={tmdb_api_key}&language=en-US&page=1'
        response = requests.get(url)
        popular_data = json.loads(response.text)

        # Load Top 10 Movies for Romance 10749, Comedy 35, Science Fiction 878
        context['romance_poster'] = []
        context['comedy_poster'] = []
        context['scifi_poster'] = []
        context['pop_poster'] = []
        context['pop_backdrop'] = []
        title = []

        rom_url = f'{base_url}/discover/movie?api_key={tmdb_api_key}&with_genres=10749'
        response = requests.get(rom_url)
        rom_data = json.loads(response.text)

        com_url = f'{base_url}/discover/movie?api_key={tmdb_api_key}&with_genres=35'
        response = requests.get(com_url)
        com_data = json.loads(response.text)

        scifi_url = f'{base_url}/discover/movie?api_key={tmdb_api_key}&with_genres=878'
        response = requests.get(scifi_url)
        scifi_data = json.loads(response.text)

        for i in range(12):
            context['romance_poster'].append(rom_data['results'][i]['poster_path'])
            context['comedy_poster'].append(com_data['results'][i]['poster_path'])
            context['scifi_poster'].append(scifi_data['results'][i]['poster_path'])
            context['pop_poster'].append(popular_data['results'][i]['poster_path'])
            context['pop_backdrop'].append(popular_data['results'][i]['backdrop_path'])
            title.append(popular_data['results'][i]['original_title'])

        cache.set('home',
                    {
                        'pop_poster':       context['pop_poster'],
                        'pop_backdrop':     context['pop_backdrop'],
                        'romance_poster':   context['romance_poster'],
                        'comedy_poster':    context['comedy_poster'],
                        'scifi_poster':     context['scifi_poster']
                    },
                    timeout=1800
                    )
    else:
        context['pop_poster'] = cache.get('home')['pop_poster']
        context['pop_backdrop'] = cache.get('home')['pop_backdrop']
        context['romance_poster'] = cache.get('home')['romance_poster']
        context['comedy_poster'] = cache.get('home')['comedy_poster']
        context['scifi_poster'] = cache.get('home')['scifi_poster']

    return render(request, 'home.html',context)

def userrating_list(request):

    user_id = request.GET.get('user_id')
    rating = UserRating.objects.filter(user_id=user_id)
    movie_name_obj = [y.title for x in rating for y in MovieInfo.objects.filter(tmdb_id=x.tmdb_id)]

    context = {}

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['session'] = True
    else:
        context['session'] = False

    context['current_user'] = user_id

    context['poster_path'] = []
    poster_list = []
    for movie in rating:
        url = f'{base_url}/movie/{movie.tmdb_id}?api_key={tmdb_api_key}&language=en-US'
        response = requests.get(url)
        output_ = json.loads(response.text)
        poster_list.append(output_['poster_path'])

    context['rating'] = [{'title':title,'rating':rating, 'poster_path':poster_path} for i,(title,rating,poster_path) in enumerate(zip(movie_name_obj,[float(x.rating) for x in rating],poster_list))]

    paginator = Paginator(context['rating'],per_page=5)
    page_number = request.GET.get('page',1)

    context['page_obj'] = paginator.page(page_number)

    return render(request, 'userrating_list.html', context)

def register(request):
    context = {}

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['session'] = True
        print('session available')
    else:
        context['session'] = False
        print('session not available')

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_pass = request.POST.get('user_pass')

        if not user_id:
            context['error'] = 'Dont leave it blank'
        elif int(user_id) < 300000:
            context['error'] = 'New user id must be greater than 300000'
        elif int(user_id) > 999999:
            context['error'] = 'User id limited to 6 digits only'
        elif UserInfo.objects.filter(user_id=user_id).exists():
            context['error'] = f'User ID {user_id} already exists'
        elif not user_pass:
            context['error'] = 'You need to enter a password'
        elif len(str(user_pass)) < 6:
            context['error'] = 'Password length must have a character count of 6 or greater'
        else:
            new_user = UserInfo(user_id = int(user_id),user_password=str(user_pass))
            new_user.save()
            context['success'] = f'User {user_id} added successfully'

    return render(request, "register.html", context)

def loginPage(request):

    context = {}

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['session'] = True

        return HttpResponse("User already logged in")

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_password = request.POST.get('user_password')
        if not UserInfo.objects.filter(user_id=int(user_id)).exists():
            context['error'] = f'User ID {user_id} does not exists'
        elif not UserInfo.objects.filter(user_id=int(user_id)).first().user_password == user_password:
            context['error'] = f'Wrong password for user id {user_id}'
        else:
            context['success'] = f'User ID {user_id} logged in!'
            context['user_id'] = user_id
            context['session'] = True
            request.session['user_id'] = user_id
            request.session['user_password'] = user_password
            request.session['user_data'] = loadUserData(user_id,get=['user_data','movie_info'])

        return redirect('home_view')

    return render(request, "login.html", context)

def logoutPage(request):

    if 'user_id' in request.session:
        logout(request)
        return redirect('home_view')
    else:
        return HttpResponse("No user currently logged in")



def update_MyUser(request):

    context = {}

    user_data = request.session.get('user_data')

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['session'] = True
        print('session available')
    else:
        context['session'] = False
        print('session not available')

    # List of genres
    get_genre_id = user_data['get_genre_id']

    year = ""
    load_genres = ""
    context['genres_text'] = ''
    context['year'] = ''

    if request.method == 'GET':
        print("\n---------------------GET------------------------\n")

        chosen_genres = request.GET.getlist('genres[]')
        year = request.GET.get('datepicker')
        context['year'] = year

        chosen_genres_id = [get_genre_id[genre] for genre in chosen_genres]
        load_genres = ",".join(str(x) for x in chosen_genres_id)
        context['genres_text'] = ", ".join(str(x) for x in chosen_genres)

        if 'user_id' in request.session:
            user_id = request.session.get('user_id')
            user_data = request.session.get('user_data')

            context['movies_watched'] = [movie['tmdb_id'] for movie in user_data['movies_watched']]
            context['movie_names'] = [movie['title'] for movie in user_data['movies_watched']]


        print("\n------------------------------------------------\n")

    if request.method == 'POST':
        print("------------------POST-------------------------")
        select_movie = request.POST.getlist('select_movie')
        user_id = request.session.get('user_id')

        if select_movie:
            for tmdb_id in select_movie:
                #CHECK IF MOVIE_ID ALREADY EXISTS FOR THE USER_ID
                if not UserRating.objects.filter(user_id=int(user_id),tmdb_id=int(tmdb_id)).exists():
                    add_movie = UserRating(user_id = int(user_id),tmdb_id=int(tmdb_id))
                    print(f"ADD TO USERRATING MODEL> USER ID: {add_movie.user} MOVIE_ID: {add_movie.tmdb_id}")
                    add_movie.save()
                    context['success'] = f"ADD TO USER ID: {add_movie.user} MOVIE_IDs: {select_movie}"
                else:
                    context['error'] = f'Movie ID {select_movie} for User ID {user_id} already exists'
                    print(f'Movie ID {tmdb_id} for User ID {user_id} already exists')

        user_data = loadUserData(user_id)

        context['movies_watched'] = [movie['tmdb_id'] for movie in user_data['movies_watched']]
        context['movie_names'] = [movie['title'] for movie in user_data['movies_watched']]

        request.session['user_data'] = user_data

        print("-----------------------------------------------")
        return redirect(request.path)

    url = f'{base_url}discover/movie?api_key={tmdb_api_key}&language=en-US&sort_by=popularity.desc&primary_release_year={year}&with_genres={load_genres}&page=1?'
    response = requests.get(url)
    movies = json.loads(response.text)
    context['movies'] = movies['results']

    return render(request,"recommend.html",context)

def addMovie2DB():
    ...

def edit_user(request):
    context = {}

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')

        user_data = request.session['user_data']
        context['movies_watched'] = [movie['tmdb_id'] for movie in user_data['movies_watched']]
        context['session'] = True
        print('session available')
    else:
        context['session'] = False
        print('session not available')

    rating = UserRating.objects.filter(user_id=context['user_id'])

    # add to database if tmdb_id and movie_id not exist
    for movie in rating:
        if not MovieInfo.objects.filter(tmdb_id=movie.tmdb_id).exists():
            url = f'{base_url}/movie/{movie.tmdb_id}?api_key={tmdb_api_key}&language=en-US'
            response = requests.get(url)
            movies = json.loads(response.text)

            add_movie = MovieInfo(tmdb_id = movie.tmdb_id,title=movies['title'])
            add_movie.save()

    movie_name_obj = [y.title for x in rating for y in MovieInfo.objects.filter(tmdb_id=x.tmdb_id)]


    context['current_user'] = context['user_id']

    context['poster_path'] = []
    poster_list = []
    for movie in rating:
        url = f'{base_url}/movie/{movie.tmdb_id}?api_key={tmdb_api_key}&language=en-US'
        response = requests.get(url)
        output_ = json.loads(response.text)
        poster_list.append(output_['poster_path'])


    context['rating'] = [{'title':title,'rating':rating, 'poster_path':poster_path,'tmdb_id':tmdb} for i,(title,rating,poster_path,tmdb) in enumerate(zip(movie_name_obj,[x.rating for x in rating],poster_list,[x.tmdb_id for x in rating]))]

    paginator = Paginator(context['rating'],per_page=5)
    page_number = request.GET.get('page',1)

    context['page_obj'] = paginator.page(page_number)

    print("page_obj",context['page_obj'])
    #####################

    if request.method == 'POST':

        if request.POST['form_name'] == 'formUpdateMovie':
            tmdb_id = request.POST.get('tmdb_id')
            rating = request.POST.get('rating')

            update_rating = get_object_or_404(UserRating,user_id = context['user_id'], tmdb_id = tmdb_id)
            update_rating.rating=rating
            update_rating.save()
            context['current_url'] = request.path
            print(context['current_url'])
            return redirect(request.build_absolute_uri())

        if request.POST['form_name'] == 'formDeleteMovie':
            tmdb_id = request.POST.get('tmdb_id')
            delete_movie = get_object_or_404(UserRating,user_id = context['user_id'], tmdb_id = tmdb_id)
            delete_movie.delete()
            context['current_url'] = request.path
            print(context['current_url'])
            return redirect(request.build_absolute_uri())


    return render(request,'edit_user.html',context)