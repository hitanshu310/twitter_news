import tweepy
import requests

consumer_key = "AxZVY6e2rAw2jxEVxULPjvRf3"
consumer_secret = "Ejg0TJIhnbJlP31k9WI4hiX5x9KcBXpm8WXMZn90pQV6S15yfi"


# to be called only when access token and access token secret are available
def completeAuth(request):
    access_token = request.session['access_token']
    access_token_secret = request.session['access_token_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


