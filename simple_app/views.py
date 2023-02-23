from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator
# Create your views here.

from .models import UserRating
from .forms import userForm



def home_view(request):
    return render(request, 'base.html')

def userrating_list(request):
 
    user_id = request.GET.get('user_id')
    rating = UserRating.objects.filter(user_id=user_id)#.first()

    context = {}
    context['current_user'] = user_id
    context['rating'] = rating

    paginator = Paginator(context['rating'],per_page=10)
    page_number = request.GET.get('page',1)

    context['page_obj'] = paginator.page(page_number)

    return render(request, 'userrating_list.html', context)


def testing(request):
    context = {}
    context['current_page'] = request.GET.get('page',1)
    return render(request,'testing.html',context)

# def create_view(request):
#     context = {}

#     form = simpleForm(request.POST or None)
#     if form.is_valid():
#         form.save()

#     context['form'] = form

#     return render(request, "create_view.html", context)

# def list_view(request):
#     # dictionary for initial data with
#     # field names as keys
#     context ={}

#     # add the dictionary during initialization
#     context["dataset"] = Userrating.objects.all()

#     return render(request, "list_view.html", context)
# # pass id attribute from urls
# def detail_view(request, id):
#     # dictionary for initial data with
#     # field names as keys
#     context ={}

#     # add the dictionary during initialization
#     context["data"] = get_object_or_404(UserRating,rating_id = id)

#     return render(request, "detail_view.html", context)

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