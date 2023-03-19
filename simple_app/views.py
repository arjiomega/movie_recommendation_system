from django.shortcuts import render, get_object_or_404, HttpResponseRedirect,redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from .models import UserRating,MovieInfo,UserInfo
#from .forms import userForm,myUserForm
import requests
import json
import os

tmdb_api_key = os.environ.get('TMDB_API_KEY')
base_url = 'https://api.themoviedb.org/3/'
rs_url = os.environ.get('RS_URL')

def home_view(request):

    # popular movies request (Get 10 image links)
    url = f'{base_url}/movie/popular?api_key={tmdb_api_key}&language=en-US&page=1'
    response = requests.get(url)
    popular_data = json.loads(response.text)
    context = {}
    pop_list = []
    backdrop = []
    title = []

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['movies_watched'] = request.session.get('movies_watched')

        #####
        payload = {
                "user_id": context['user_id'],
                "movie_list": context['movies_watched']
        }
        response = requests.post(url=rs_url, json=payload)
        output_ = json.loads(response.text)

        recommend_id_list = [movie['id'] for movie in output_['data']['predict']['recommended_movies']]

        context['recommend_poster'] = []
        for tmdb_id in recommend_id_list:
            url = f'{base_url}/movie/{tmdb_id}?api_key={tmdb_api_key}&language=en-US'
            response = requests.get(url)
            output_ = json.loads(response.text)
            context['recommend_poster'].append(output_['poster_path'])
        print(context['recommend_poster'])
        #####

        context['session'] = True
        print('session available')
    else:
        context['session'] = False
        print('session not available')



    for i in range(12):
        pop_list.append(popular_data['results'][i]['poster_path'])
        backdrop.append(popular_data['results'][i]['backdrop_path'])
        title.append(popular_data['results'][i]['original_title'])

    context['pop_poster'] = pop_list
    context['pop_backdrop'] = backdrop

    # Load Top 10 Movies for Romance 10749, Comedy 35, Science Fiction 878
    romance_poster = []
    comedy_poster = []
    scifi_poster = []
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
        romance_poster.append(rom_data['results'][i]['poster_path'])
        comedy_poster.append(com_data['results'][i]['poster_path'])
        scifi_poster.append(scifi_data['results'][i]['poster_path'])

    context['romance_poster'] = romance_poster
    context['comedy_poster'] = comedy_poster
    context['scifi_poster'] = scifi_poster

    # USER RECOMMENDATION
    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        print(context['user_id'])
    ########################################################

    return render(request, 'base.html',context)

def userrating_list(request):

    user_id = request.GET.get('user_id')
    rating = UserRating.objects.filter(user_id=user_id)
    movie_name_obj = [y.title for x in rating for y in MovieInfo.objects.filter(tmdb_id=x.tmdb_id)]

    context = {}

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['session'] = True
        print('session available')
    else:
        context['session'] = False
        print('session not available')

    context['current_user'] = user_id

    context['poster_path'] = []
    poster_list = []
    for movie in rating:
        print("tmdb_id: ",movie.tmdb_id)
        url = f'{base_url}/movie/{movie.tmdb_id}?api_key={tmdb_api_key}&language=en-US'
        response = requests.get(url)
        output_ = json.loads(response.text)
        poster_dict =   {
                        "tmdb_id":movie.tmdb_id,
                        "poster_path":output_['poster_path']
                        }
        poster_list.append(output_['poster_path'])

    #print(context['poster_path'])


    context['rating'] = [{'title':title,'rating':rating, 'poster_path':poster_path} for i,(title,rating,poster_path) in enumerate(zip(movie_name_obj,[float(x.rating) for x in rating],poster_list))]

    paginator = Paginator(context['rating'],per_page=5)
    page_number = request.GET.get('page',1)

    context['page_obj'] = paginator.page(page_number)

    print("page_obj",context['page_obj'])

    return render(request, 'userrating_list.html', context)


def add_MyUser(request):
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

    return render(request, "Enter.html", context)


def logoutPage(request):
    logout(request)
    return redirect('home_view')


def update_MyUser(request):

    context = {}

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['session'] = True
        print('session available')
    else:
        context['session'] = False
        print('session not available')

    for key,value in request.session.items():
        print(key,value)
    # List of genres
    url = f'{base_url}/genre/movie/list?api_key={tmdb_api_key}&language=en-US'
    response = requests.get(url)
    genre_json = json.loads(response.text)

    genre_list = []
    genre_ids = []
    for i in genre_json['genres']:
        genre_list.append(i['name'])
        genre_ids.append(i['id'])
    context['genres'] = genre_list
    context['id'] = genre_ids
    get_genre_id = {context['genres'][i]: context['id'][i] for i in range(len(context['genres']))}

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

            ###### GET MOVIE ID ############
            # GET LIST OF MOVIES USER WATCHED
            user_rating = UserRating.objects.filter(user_id=int(user_id))
            context['movies_watched'] = [rating.tmdb_id for rating in user_rating]
            request.session['movies_watched'] = context['movies_watched']

            movie_names = []
            for movie in context['movies_watched']:
                # get movie title from tmdb_id
                url = f"{base_url}/movie/{movie}?api_key={tmdb_api_key}&language=en-US"
                response = requests.get(url)
                movie_detail = json.loads(response.text)
                movie_names.append(movie_detail['original_title'])
            context["movie_names"] = movie_names
            request.session['movie_names'] = movie_names
            print(context["movie_names"])

            ################################

        print("\n---------------------END GET------------------------\n")

    

    if request.method == 'POST':
        print("------------------POST-------------------------")
        # LOGIN
        

        # Check if the user is already logged in

        if 'user_id' in request.session:
            user_id = request.session.get('user_id')
            user_password = request.session.get('user_password')
            context['user_logged'] = int(user_id)
        else:
            user_id = request.POST.get('user_id')
            user_password = request.POST.get('user_password')

        ## REPLACE THIS TO PROPER NAMING
        select_movie = request.POST.getlist('select_movie')
        print("select movie ",select_movie)

        # CHECK IF USER ID IS ENTERED
        if not user_id:
            context['error'] = 'You need to input your user id'
        # CHECK IF USER ID IS VALID (USER_ID > 300000)
        elif int(user_id) < 300000:
            context['error'] = 'User id must be greater than 300000'
        # CHECK IF USER ID IS VALID (USER_ID LENGTH OF 6)
        elif int(user_id) > 999999:
            context['error'] = 'User id limited to 6 digits only'
        # CHECK IF USER_ID DOES NOT EXIST IN USER_INFO
        elif not UserInfo.objects.filter(user_id=int(user_id)).exists():
            context['error'] = f'User ID {user_id} does not exists'

        elif user_id:
            request.session['user_id'] = user_id
            request.session['user_password'] = user_password
            context['user_logged'] = int(user_id)
        #else:
            if not user_password:
                context['error'] = 'Do not leave the password input blank'
            elif not UserInfo.objects.filter(user_id=int(user_id)).first().user_password == user_password:
                context['error'] = f'Wrong password for user id {user_id}'

            if select_movie:
                for tmdb_id in select_movie:
                    #CHECK IF MOVIE_ID ALREADY EXISTS FOR THE USER_ID
                    if not UserRating.objects.filter(user_id=int(user_id),tmdb_id=int(tmdb_id)).exists():
                        ############# ADD TO USER #####################
                        print(f"user_id {type(user_id)} {user_id}")
                        print("LOAD TO USER: ",user_id,int(tmdb_id))
                        add_movie = UserRating(user_id = int(user_id),tmdb_id=int(tmdb_id))
                        print(f"ADD TO USERRATING MODEL> USER ID: {add_movie.user_id} MOVIE_ID: {add_movie.tmdb_id}")
                        add_movie.save()
                        context['success'] = f"ADD TO USERRATING MODEL> USER ID: {add_movie.user_id} MOVIE_ID: {add_movie.tmdb_id}"
                        ###############################################
                    else:
                        #context['error'] = f'Movie ID {select_movie} for User ID {user_id} already exists'
                        print(f'Movie ID {tmdb_id} for User ID {user_id} already exists')

        user_rating = UserRating.objects.filter(user_id=int(user_id))
        context['movies_watched'] = [rating.tmdb_id for rating in user_rating]
        request.session['movies_watched'] = context['movies_watched']

        movie_names = []
        for movie in context['movies_watched']:
            # get movie title from tmdb_id
            url = f"{base_url}/movie/{movie}?api_key={tmdb_api_key}&language=en-US"
            response = requests.get(url)
            movie_detail = json.loads(response.text)
            movie_names.append(movie_detail['original_title'])
        context["movie_names"] = movie_names
        request.session['movie_names'] = movie_names

        print("------------------END POST-------------------------")
        #return HttpResponseRedirect("")

    url = f'{base_url}discover/movie?api_key={tmdb_api_key}&language=en-US&sort_by=popularity.desc&primary_release_year={year}&with_genres={load_genres}&page=1?'

    response = requests.get(url)
    movies = json.loads(response.text)


    context['movies'] = movies['results']

    # PRINT
    print("\n---------------------FINAL------------------------\n")
    print("USER LOGGED: ",request.session['user_id'])
    print("CHOSEN YEAR: ",context['year'])
    print("CHOSEN GENRES: ",context['genres_text'])
    print("CURRENT URL: ",url)
    print("ADDED MOVIES: ",context['temp_list'])
    #print("ADD TO USER_RATING: ",add_movie)
    print("\n--------------------END FINAL----------------------\n")
    ###################################################

    return render(request,"recommend.html",context)

def edit_user(request):
    context = {}

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['movies_watched'] = request.session['movies_watched']
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
    test = [(x.tmdb_id) for x in rating]
    print(movie_name_obj)
    context = {}

    if 'user_id' in request.session:
        context['user_id'] = request.session.get('user_id')
        context['session'] = True
        print('session available')
    else:
        context['session'] = False
        print('session not available')

    context['current_user'] = context['user_id']

    context['poster_path'] = []
    poster_list = []
    for movie in rating:
        print("tmdb_id: ",movie.tmdb_id)
        url = f'{base_url}/movie/{movie.tmdb_id}?api_key={tmdb_api_key}&language=en-US'
        response = requests.get(url)
        output_ = json.loads(response.text)
        poster_dict =   {
                        "tmdb_id":movie.tmdb_id,
                        "poster_path":output_['poster_path']
                        }
        poster_list.append(output_['poster_path'])


    #print(context['poster_path'])

    print('before insert:')
    print(len(movie_name_obj),len([x.rating for x in rating]),len(poster_list),len([x.tmdb_id for x in rating]))

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
            return HttpResponseRedirect('')

        if request.POST['form_name'] == 'formDeleteMovie':
            tmdb_id = request.POST.get('tmdb_id')
            delete_movie = get_object_or_404(UserRating,user_id = context['user_id'], tmdb_id = tmdb_id)
            delete_movie.delete()
            context['current_url'] = request.path
            print(context['current_url'])
            return HttpResponseRedirect('')



    return render(request,'edit_user.html',context)

def update_test(request):
    logout(request)
    return redirect('edit_user')




# # update view for details
# def update_view(request, id):
#     # dictionary for initial data with
#     # field names as keys
#     context ={}
 
#     # fetch the object related to passed id
#     obj = get_object_or_404(simpleModel, id = id)
 
#     # pass the object as instance in form
#     form = simpleForm(request.POST or None, instance = obj)
 
#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect("detail/"+id)
 
#     # add form dictionary to context
#     context["form"] = form
 
#     return render(request, "update_view.html", context)

# # delete view for details
# def delete_view(request, id):
#     # dictionary for initial data with
#     # field names as keys
#     context ={}
 
#     # fetch the object related to passed id
#     obj = get_object_or_404(simpleModel, id = id)
 
#     if request.method =="POST":
#         # delete object
#         obj.delete()
#         # after deleting redirect to
#         # home page
#         return HttpResponseRedirect("/")
 
#     return render(request, "delete_view.html", context)