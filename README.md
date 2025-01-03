# tldrIFY: _short on time, TALL ON NEEDS_

## General Idea
For the project for course [ID2223](https://www.kth.se/student/kurser/kurs/ID2223?l=en), we decided to create `tldrIFY`: an application that summarizes recent news articles from different regions of the world. The goal is for the program to create digestable 1-2 sentence summaries of news articles so that readers can get a quick digest of the happenings around the world without having to parse through multiple news articles themselves. 

For completing this project, we had to accomplish several tasks: such as finding an adequate real-time data source which would provide us the content of the news articles, fine-tuning our own model which was used to summarize the contents of the news articles, or creating a HuggingFace UI to show the results of our project. In this report, we will briefly go through the major steps accomplished by us in order to create `tldrIFY`.  

## Fine Tuning the T5 Model
The main task of `tldrIFY` is to summarize news articles. For the summarization task, we decided to use an LLM. However, we did not simply use a vanilla version of a publicly available LLM. Instead we decided to fine-tune an LLM so that the model we used would be better at the specific task that we wanted to perform: summarization. 

The base publicly-available LLM we deicded to use was the [T5-small](https://huggingface.co/google-t5/t5-small) model, and we used the [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/summarization.ipynb) available in the description of [this YouTube video](https://youtu.be/PyRbP9d27sk?si=OVBnmkRWMLq0r1Ml) to fine tune the T5-small model on Google Colab's T4-GPU. The notebook seems to be available at [this HuggingFace Github Repo](https://github.com/huggingface/notebooks/blob/main/examples/summarization.ipynb) as well. We decided to go with the T5-small model apart from some of the other T5 alternatives (such as [T5-base](https://huggingface.co/google-t5/t5-base) or [T5-large](https://huggingface.co/google-t5/t5-large)) because it was our understanding that it would take less amount of time to fine-tune a smaller model as opposed to larger models. Since we believe T5-small to be a "smaller" model, we felt that it would be adequate for the project. 

We utilized the [XSum Dataset](https://huggingface.co/datasets/EdinburghNLP/xsum) for the purposes of fine-tuning the T5-small LLM. Thus, the XSum Dataset also served as the **historical data-set** that was required as a part of the ID2223 project. We fine-tuned the T5-small LLM for 10-epochs (with pauses in between epochs as we evaluated how the model behaved with fewer epochs as well) using training and validation sets: meaning that the fine-tuning did take a non-trivial amount of time. Thus, in order to save our progress between epochs, we saved the progress of the fine-tuning of the model every 100 steps in Google Drive. Apart from epochs and saving-specific hyperparameters, we largely used the same hyperparameters that were present in the base notebook. 

The fine-tuned version of the T5-small model can be found here: https://huggingface.co/rishivijayvargiya/outputs-project-id2223. The code for the fine-tuning can be found under the root directory of this repository at [this location](https://github.com/adrianxsusec/tldrify/blob/main/T5_Finetuning_Summarization.ipynb).

## The Real Time Dataset
In order to summarize recent news, we need the content of the news articles to summarize. Finding a good data source for this that was cheap/free was a task that was more difficult than we anticipated. There were some datasets that were free but which seem to return trimmed news content only (such as [TheNewsApi](https://www.thenewsapi.com/documentation)) or some that we felt would be too expensive (such as the [NewsAPI](https://newsapi.org/)). We also tried applying for the [News Catcher API](https://www.newscatcherapi.com/free-news-api), which was free of cost. However, we were not able to hear back from them in time -- possibly because requests were paused around the time we applied due to some improvements being implemented in the API. 

Eventually, we decided to go with [NewsData.io](https://newsdata.io/) for our news API. The free version did not seem to contain the content of the article. So, we decided to opt for the cheapest paid version -- which was around $150/month. With this, we got access not only to the content of news articles, but also to the category of the news article, but it also allowed us to fetch news articles in a given time-frame. 

Thus, using the `latest api` endpoint of `NewsData.io`, we fetch news articles published in a given country with a specific category that were released at most 12 hours ago. The countries for which we fetch the news articles are: `India`, `Australia`, `USA`, `Nigeria`, and `UK`. The categories for which we fetch the news articles are: `business`, `entertainment`, `technology`, `politics`, `sports`. Thus, one request made to the `NewsData.io` API might look like this: `api_client.latest_api(country="in", category="sports", timeframe=12, language="en")`. This request would fetch news articles published in the last 12 hours by Indian news sources in English that were under the category `sports`. Thus, in total, 25 such requests are made: one for each (country, category) pair. 

After fetching the news articles in this way, we do some pre-processing before storing these articles for use in inference. First, we put the fetched articles in a data-frame and we only select a subset of the columns that seemed relevenat to us for our task, which are: `article_id`, `title`, `link`, `description`, `content`, `pubDate`, `source_id`, `country`, `category`. Then, we drop information about any row from the data-frame that had `NULL` values in it using the `dropna` method. Finally, we only select the first 5 news articles for each (country, category) pair. Currently, there is no specific criteria with which we pick the "first 5" news articles. However, this is something that can be refined in the future. The reason for picking the first 5 articles instead of picking them all is to limit the amount of time that is spent in the inference step: since we use Github actions to automate these processes, we did not want to risk exceeding our execution limits before the day of the demo.

After pre-processing the fetched data as described above, we store the data-frame containing the news for the day in the Hopsworks feature group titled `news_articles_raw`: using the `article_id` as the primary key. The code-file responsible for these steps is `daily-feature-pipeline.py` and can be found in the root of this repository. The execution of the code in `daily-feature-pipeline.py` is automated with the help of Github actions, with the workflow file called `feature.yml` under `.github/workflows` doing the work.

## Daily Inference

## The Hugging Face Space


## Demo

## Future Work and Ideas

### Using Larger Base Models (eg: T5-Large)

