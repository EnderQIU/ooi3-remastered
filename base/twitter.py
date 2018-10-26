import click
import tweepy

from app import app


class TwitterAPI:
    """
    Twitter API
    """
    consumer_api_key = app.config['API_KEY']  #'YmYSBd13s2d2uJQuAytFwQbfP'
    consumer_secret_key = app.config['SECRET_KEY']  #'H5KHaGDiqzPT5nzBoSb8JKkhYlWfL8Fe1WZy1ja7vD6sUyWdPD'
    access_token = app.config['ACCESS_TOKEN']  #'909587479-Ifa3YUPV7cRNMlhpsXH0QBQ4qtIpPQUqrxnLhxib'
    access_token_secret = app.config['TOKEN_SECRET']  #'PlYaPZrbGOMpgFRvAaxS7DG3sIHwi6EiWrmcdIyfqyghA'

    auth = tweepy.OAuthHandler(consumer_api_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)


    def get_official_20tweets(self):
        """
        Get previous 20 tweets
        :return:
        """
        r = {'message': 'ok', 'data': []}
        tweets = []
        try:
            public_tweets = self.api.user_timeline('KanColle_STAFF')
        except tweepy.error.TweepError as e:
            click.echo(e, err=True)
            r['message'] = "Error: Could not fetch tweets from Kancolle Staff's twitter."
            return r
        for tweet in public_tweets:
            tweets.append({
                'created_at': tweet.created_at.strftime("%b %d %H:%M") + " +0000",
                'text': tweet.text,
            })
        r['data'] = tweets
        return r
