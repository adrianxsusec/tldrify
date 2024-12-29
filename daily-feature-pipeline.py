import hopsworks
import os
from newsdataapi import NewsDataApiClient
import pandas as pd


def fetch_and_store_articles():
    project = hopsworks.login()
    fs = project.get_feature_store()

    newsdata_api_key = os.environ["NEWSDATA_API_KEY"]
    news_client = NewsDataApiClient(apikey=newsdata_api_key)

    # We will be fetching articles from the following countries in the following categories
    # countries: India (in), Australia (au), USA (us), Nigeria (ng), and UK (gb)
    # categories: business, entertainment, technology, politics, sports
    # Thus, in total, we will make |countries| x |categories| = 5 x 5 = 25 queries. 
    # The articles will be fetched daily with a time-frame of 12 hours (ie, articles published at most 12 hours
    # before the query is made).
    # In each query, we get 50 news articles. We will ONLY consider the first 5 results for generating summaries.

    # countries = {"India": "in", "Australia": "au", "USA": "us", "Nigeria": "ng", "UK": "gb"}
    countries = {"India": "in"}
    # categories = ['business', 'entertainment', 'technology', 'politics', 'sports']
    categories = ['business']

    fetched_articles_df = []

    print("------------ FETCHING NEWS ARTICLES -------------------")
    for country_name in countries.keys():
        country_code = countries[country_name]
        for category in categories:
            response = news_client.latest_api(country=country_code, category=category, timeframe=12, language="en")

            if req_successful(response):
                print("Fetched", str(len(response['results'])), "articles for", country_name, "and", category)
                # Store the articles fetched along with the country and the category used for the query
                # Only need to process articles if AT LEAST one of them was fetched
                if len(response['results']) > 0:
                    processed_df = get_processed_articles_df(response['results'], country_name, category)
                    fetched_articles_df.append(processed_df)
            else:
                print("Unable to retrieve data:", response.get('message', 'Unknown Error'))
    
    print("--------------- FINISHED FETCHING OF NEWS ARTICLES ------------------")
    combined_df = pd.concat(fetched_articles_df, ignore_index=True)
    print("-------------- PRINTING COMBINED DF ---------------------")
    print(combined_df)
    print("-------------- FINISHED PRINTING COMBINED DF ---------------------")

    # Put articles in feature store
    news_articles_hopsworks = fs.get_or_create_feature_group(
        name="news_articles_raw",
        version=1,
        primary_key=['article_id'],
        description="Raw news articles retrieved from NewsDataApi"
    )

    print("------------- Commencing insert of DF in to Hopsworks -------------------- ")
    news_articles_hopsworks.insert(combined_df)
    print("----------------- Successfully inserted DF Into Hopsworks! -------------------")
    
    


# fetched_news: LIST of 5 news articles returned by NewsDataApi with the same schema (except for possibly category)
# fetched_country: STRING specifying the country used to make the query to NewsDataApi
def update_country(fetched_news, fetched_country):
    for article in fetched_news:
        article['country'] = fetched_country
    return fetched_news
    

# fetched_news: LIST of 5 news articles returned by NewsDataApi with the same schema (except for possibly country)
# fetched_category: STRING specifying the catrgory used to make the query to NewsDataApi
def update_category(fetched_news, fetched_category):
    for article in fetched_news:
        article['category'] = fetched_category
    return fetched_news

# Determine if a request to NewsDataApi was successful
def req_successful(response): 
    return 'status' in response and response['status'] == 'success'

# Get the first 5 articles for the (country, category) pair as a dataframe after some processing
def get_processed_articles_df(fetched_news, country, category):
    articles_after_country_category = update_category(update_country(fetched_news, country), category)

    # Use dataframe for some processing (selecting relevant columns, dropping null values, etc)
    df = pd.DataFrame(articles_after_country_category)
    df = df[['article_id', 'title', 'link', 'description', 'content', 'pubDate', 'source_id', 'country', 'category']]
    df = df.dropna()

    # Only keep the date field of the datetime column, remove the TIME
    df['pubDate'] = pd.to_datetime(df['pubDate']).dt.date.astype("string")

    # Only want the first 5 processed articles for each (country, category) pair
    return df.head(5)


if __name__ == "__main__":
    fetch_and_store_articles()
