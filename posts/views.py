import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import PostFrom

from .models import Post

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_page(request, *args, **kwargs):
    return render(request, "pages/main.html", context={}, status=200)

def post_create_view(request, *arg, **kwargs):
    form = PostFrom(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # Saving to DF
        if request.is_ajax():
            return JsonResponse({}, status=201) # 201 for created items || wanna replace {} with serialize from models.py, but got error 500
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = PostFrom()
    return render(request, 'components/form.html', context={"form": form})


def post_list_view(request, *args, **kwargs):
    """
    REST API View
    Consumed by JavaScript
    return json data
    """
    qs = Post.objects.all()
    posts_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 120), "reposts": random.randint(0, 10)} for x in qs] #{"id": x.id, "content": x.content, "likes": random.randint(0, 120), "reposts": random.randint(0, 10) }/x.serialize()
    data = {
        "isUser": False,
        "response": posts_list
    }
    return JsonResponse(data) #, save=False

def post_detail_id(request, post_id, *args, **kwargs):
    """
    REST API View
    Consumed by JavaScript
    return json data
    """
    data = {
        "id": post_id,
    }
    status = 200
    try:
        obj = Post.objects.get(id=post_id)
        data['content'] = obj.content
    except:
        data['message'] = "not found"
        status = 404

    return JsonResponse(data, status=status) #json.dumps content_type='application/json'


    # looking ro mentor in JS & Python cause sometimes i need fresh look for code!