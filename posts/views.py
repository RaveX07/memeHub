from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse

from .models import Post
from .forms import PostForm

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request=request, template_name="pages/home.html", context={})

def post_create_view(request, *args, **kwargs):
    form = PostForm(request.POST or None)
    if form.is_valid():
        obj= form.save(commit=False)
        obj.save()
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