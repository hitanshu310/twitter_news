from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from feed.utils import *
from django.template import loader
from .formfile import TokenForm


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
    return HttpResponse("Hello there")


def authorize(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
    if form.is_valid():
        token = form.cleaned_data['token']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        rt = request.session['request_token']
        del request.session['request_token']
        auth.request_token = rt
        a, b = auth.get_access_token(token)
        auth.set_access_token(a, b)
        api = tweepy.API(auth)
        public_tweets = api.home_timeline()
        context = {
            'api': api,
            'pt': public_tweets,
        }
        template = loader.get_template('feed/tweets.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/feed/')




