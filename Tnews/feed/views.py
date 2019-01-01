from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from feed.utils import *
from django.template import loader
from django.urls import reverse
from .formfile import TokenForm


def checkAuth(request):
    access_token_temp = request.session.get('access_token', None)
    access_token_secret_temp = request.session.get('access_token_secret', None)
    if access_token_temp is None or access_token_secret_temp is None:
        return redirect('/auth/authorize/')
    else:
        return redirect(reverse('hashTag'))


def autho(request):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        return HttpResponse('Error! Failed to get request token.')
    request.session['request_token'] = auth.request_token
    template = loader.get_template('feed/basic.html')
    form = TokenForm()
    context = {
        'url': redirect_url,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def hello(request):
    return HttpResponse("hello")


def authorize(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
    if form.is_valid():
        token = form.cleaned_data['token']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        rt = request.session['request_token']
        del request.session['request_token']
        auth.request_token = rt
        try:
            a, b = auth.get_access_token(token)
        except tweepy.TweepError:
            return HttpResponse("invalid token")
        auth.set_access_token(a, b)
        request.session['access_token'] = a
        request.session['access_token_secret'] = b
        return redirect(reverse('feed'))
    else:
        return redirect(reverse('index'))


def feed(request):
    api = completeAuth(request)
    public_tweets = api.home_timeline()
    context = {
        'api': api,
        'pt': public_tweets,
    }
    template = loader.get_template('feed/tweets.html')
    return HttpResponse(template.render(context, request))


def hashtagFeed(request):
    api = completeAuth(request)
    res = requests.get('https://ipinfo.io/')
    res_json = res.json()
    coords = res_json['loc'].split(',')
    text = api.trends_closest(coords[0], coords[1])
    pid = text[0]['woeid']
    hashtags = api.trends_place(pid)[0]['trends']
    context = {
        'hashtags': hashtags,
    }
    template = loader.get_template('feed/trending_tags.html')
    return HttpResponse(template.render(context, request))


def logout(request):
    request.session.flush()
    return redirect(reverse('index'))






