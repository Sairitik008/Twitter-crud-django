from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .models import Twitter
from .forms import TweetForm, UserRegistrationForm


# -------------------------
# TWEET LIST (HOME)
# -------------------------
def tweet_list(request):
    tweets = Twitter.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})


# -------------------------
# CREATE TWEET
# -------------------------
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()

    return render(request, 'tweet_form.html', {'form': form})


# -------------------------
# EDIT TWEET
# -------------------------
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(
        Twitter,
        pk=tweet_id,
        user=request.user
    )

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})


# -------------------------
# DELETE TWEET
# -------------------------
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(
        Twitter,
        pk=tweet_id,
        user=request.user
    )

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')

    return render(
        request,
        'tweet_confirm_delete.html',
        {'tweet': tweet}
    )


# -------------------------
# USER REGISTRATION
# -------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()   # ✅ password handled by UserCreationForm
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )
