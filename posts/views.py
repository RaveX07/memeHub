from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings


from .models import Post
from .forms import PostForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request=request, template_name="pages/home.html", context={})

def post_create_view(request, *args, **kwargs):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        next_url = request.POST.get("next") or None

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            
            if next_url != None and url_has_allowed_host_and_scheme(next_url, allowed_hosts=ALLOWED_HOSTS):
                return redirect(next_url)

            form = PostForm()

        return render(request, 'components/form.html', context={"form": form})

def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    post_list = [{"id": x.id, "content": x.content, "imageURL": str(x.image), "likes": str(x.likes)} for x in qs]

    data = {
        "response": post_list
    }

    return JsonResponse(data=data)

def post_detail_view(request, post_id, *args, **kwargs):

    data = {
        "id": post_id,  
    }
    status = 200

    try:
        post = Post.objects.get(id=post_id)
        imageURL = "media/" + str(post.image)

        data['content'] = post.content
        data['imageURL'] = str(post.image)
        data['likes'] = str(post.likes)
    except:
        data['message'] = "Not found"
        status = 400
    

    return JsonResponse(data, status=status)