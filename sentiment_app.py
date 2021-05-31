import tweepy
from textblob import TextBlob
import preprocessor
import statistics
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()
consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_SECRET_KEY")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

def get_tweets(vaccine):
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=vaccine, tweet_mode= 'extended', lang= 'en').items(10):
        all_tweets.append(tweet.full_text)
        
    return all_tweets

def clean_tweets(all_tweets):
    cleaned_tweets = []
    for tweet in all_tweets:
        cleaned_tweets.append(preprocessor.clean(tweet))
    
    return cleaned_tweets

def get_sentiment(all_tweets):
    sentiment_scores = []
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)

    return sentiment_scores

def generate_average_sentiment_score(vaccine):
    tweets = get_tweets(vaccine)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)
    
    average_score = statistics.mean(sentiment_scores)
    return average_score

if __name__ == "__main__":
    print("Vaccine One:")
    first_vaccine=input()
    print("VS")
    second_vaccine=input()
    
    first_score = generate_average_sentiment_score(first_vaccine)
    second_score = generate_average_sentiment_score(second_vaccine)

    if (first_score > second_score):
        print(f"The public prefers {first_vaccine}")
    else:
        print(f"The public prefers {second_vaccine}")


