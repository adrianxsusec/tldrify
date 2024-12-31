import hopsworks
import sys
import pandas as pd

from datetime import datetime, timezone, timedelta
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

date_format = '%Y-%m-%d'


def fetch_todays_articles(fs):
    news_articles_hopsworks = fs.get_feature_group(
        name="news_articles_raw",
        version=1
    )

    news_articles_df = news_articles_hopsworks.read()
    news_articles_df['pubdate'] = pd.to_datetime(news_articles_df['pubdate']).dt.strftime(date_format)
    today = datetime.now(timezone.utc).strftime(date_format)
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime(date_format)

    mask = news_articles_df['pubdate'] == yesterday
    return news_articles_df[mask]


def summarize_and_push_articles_to_fs(fs, articles, model, tokenizer):
    articles['summary'] = ''

    # Process each article
    for idx, row in articles.iterrows():
        print(f'summarizing row {idx}')
        inputs = tokenizer(row['content'], truncation=True, max_length=1024, return_tensors="pt")
        summary_ids = model.generate(inputs['input_ids'], max_length=150, min_length=40)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        articles.at[idx, 'summary'] = summary

    for idx, row in articles.iterrows():
        print(f"\n{'=' * 100}w")
        print(f"Row {idx}")
        print(f"\nSUMMARY:\n{row['summary']}")
        print(f"\nCONTENT:\n{row['content']}")
        print(f"\n{'=' * 100}")

    # news_articles_hopsworks = fs.get_or_create_feature_group(
    #     name="news_articles_summarized",
    #     version=1,
    #     primary_key=['article_id'],
    #     description="Summarized articles from news_articles_raw"
    # )
    #
    # print("------------- Inserting summarized articles -------------")
    # news_articles_hopsworks.insert(articles)
    # print("----------------- Successfully inserted DF Into Hopsworks! -------------------")


if __name__ == "__main__":
    project = hopsworks.login()
    fs = project.get_feature_store()

    model_name = "rishivijayvargiya/outputs-project-id2223"
    tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    todays_articles = fetch_todays_articles(fs)
    summarize_and_push_articles_to_fs(fs=fs, articles=todays_articles, model=model, tokenizer=tokenizer)
