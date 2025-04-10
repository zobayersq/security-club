from django.shortcuts import render
from .models import Event

# Create your views here.
def upcoming_events(request):
    events = Event.objects.filter(date__gt=timezone.now()).order_by('date')
    return render(request, 'events/upcoming_events.html', {'events': events})

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
