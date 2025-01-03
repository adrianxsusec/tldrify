# tldrIFY: _short on time, TALL ON NEEDS_

## Link to Demo
You can find the HuggingFace Space that hosts the demo of the application here: https://huggingface.co/spaces/shallowunlearning/tldrify-ui

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

Thus, using the `latest api` endpoint of `NewsData.io`, we fetch news articles published in a given country with a specific category that were released at most 12 hours ago. The countries for which we fetch the news articles are: `India`, `Australia`, `USA`, `Nigeria`, and `UK`. The categories for which we fetch the news articles are: `business`, `entertainment`, `technology`, `politics`, `sports`. Thus, one request made to the `NewsData.io` API might look like this: `api_client.latest_api(country="in", category="sports", timeframe=12, language="en")`. This request would fetch news articles published in the last 12 hours by Indian news sources in English that were under the category `sports`. Thus, in total, 25 such requests are made: one for each (country, category) pair. It is possible for an article to have multiple categories, for example: `business, sports`. To make things easier when it comes to filtering the articles by a specific criteria, we made the decision to _overwrite_ the category returned for a news article by the category _used_ to make the request which returned said article. For instance, if we made an API request to fetch `sports` articles, and if a returned article had categories `sports, business`, then the final category for this article will be `sports`.

After fetching the news articles in this way, we do some pre-processing before storing these articles for use in inference. First, we put the fetched articles in a data-frame and we only select a subset of the columns that seemed relevenat to us for our task, which are: `article_id`, `title`, `link`, `description`, `content`, `pubDate`, `source_id`, `country`, `category`. Then, we drop information about any row from the data-frame that had `NULL` values in it using the `dropna` method. Finally, we only select the first 5 news articles for each (country, category) pair. Currently, there is no specific criteria with which we pick the "first 5" news articles. However, this is something that can be refined in the future. The reason for picking the first 5 articles instead of picking them all is to limit the amount of time that is spent in the inference step: since we use Github actions to automate these processes, we did not want to risk exceeding our execution limits before the day of the demo.

After pre-processing the fetched data as described above, we store the data-frame containing the news for the day in the Hopsworks feature group titled `news_articles_raw`: using the `article_id` as the primary key. The code-file responsible for these steps is `daily-feature-pipeline.py` and can be found in the root of this repository. The execution of the code in `daily-feature-pipeline.py` is automated with the help of Github actions, with the workflow file called `feature.yml` under `.github/workflows` doing the work.

## Daily Inference
TODO: Write about the daily inference file and how/what we do, end with the brief description of the workflow file that we run to automate the task of generating summaries, and how that needs to run _after_ the articles of the day have been fetched (this is obvious, but would be good to point out)

## The Hugging Face Space
To demonstrate the results of the summarization, we utilize a Gradio UI that is hosted on HuggingFace Spaces. The Gradio UI can be found at [this](https://huggingface.co/spaces/shallowunlearning/tldrify-ui) location. The UI allows users to filter news summaries based on the country in which the news was published, or the category of the news. Both these filtering options are displayed in separate tabs, and the users can click on check-boxes to specify their filtering criteria.

For instance, clicking on the tab "Filter by Country" and checking only the box for "India" would display news summaries across _all_ 5 categories published by Indian news sources on the day. Clicking on the checkbox for "India" and "USA" would display summaries of news across _all_ 5 categories published by Indian _or_ USA news sources for the day. Similar rule applies for the "Filter by Categories" tab: where countries are ignored and only the categories are considered for filtering. 

However, sometimes, clicking on checkboxes is not fun. Not only that, sometimes we might need more advanced filter criterias: that span multiple columns on which to filter. For instance, we might want to filter news summaries to get only those published in India _or_ USA but only under category of business. The tabular UI discussed earlier does not allow for these complex queries. 

Thus, we decided to create an incredibly simple "query" language: which is the purpose served by the 3rd tab in our Gradio UI. The "language" has a simple syntax: filter-criteria-1=value-1,value-2,...,value-m & ... & filter-criteria-n=value-1_. For instance, if `country=USA,India & category=business,sports` is the query used, then the result will be summaries for articles that are either from USA or India, AND are in the category business or sports. Currently, the only `filter-criteria` supported are `country` and `category`, however this is something that can be expanded in the future. It is important to note that this querying option currently does not do much in terms of error-checking, however this is something that can be expanded upon in future iterations.

The HuggingFace Spaces needs to be restarted on a daily basis so that the work done by the feature-fetch and the inference pipelines daily can be made available on the Gradio UI. To this end, we use the code in the `hf_space_restart.py` file, to programmatically restart the HF Space using the HF API. The code in this file is executed automatically on a daily basis, and is executed **LAST** in the sequence of `feature-fetch --> inference --> space-restart`. The automation of the execution is done through a GitHub Action, the code for which can be found in the `hf_restart.yml` file under `.github/worklows` directory. The code for this HF Space can be found here: https://huggingface.co/spaces/shallowunlearning/tldrify-ui/tree/main. The directory `hf_space` in this repository just points to the HF directory. This was done to ensure that there is only a single source of truth for the UI of this project.

A thing to note: The HuggingFace space is restarted at around 6:20pm UTC everyday -- thus if visited _before_ this time, the news summaries displayed on the Gradio UI would be for the _previous_ day. 

## Demo
The following is a demo of how the HuggingFace Space described above in action


https://github.com/user-attachments/assets/9ff2c830-97cd-48d4-8a1a-e104010e7339




## Results
Given the fact that we used our own fine-tuned model to create summaries instead of pre-built LLMs, we are **reasonably happy** with the results we have obtained. Of course, the summaries created by our fine-tuned LLM are not perfect, far from it. Some noticeable drawbacks seem to be that the model appears to get "stuck" in some instances. For instance, in the demo video above, a summary can be seen with successive `-` at the end of the summary. Another summary was noticed to have multiple occurrences of `£4` in the summary, even though it did not make sense in the context. It appears that the LLM is not able to get "out" of using such characters once it starts using them, which can create summaries that are not very informative. 

Another phenomenon we noticed was that the returned article content from NewsData.io seemed to have information about things that were not necessarily relevant to the article at hand: such as information about social media handles. This could also lead to "polluting" the text that is used by our fine-tuned LLM to generate summaries. However, given the resources at hand, we still feel that, if nothing else, we were able to create a servicable "proof-of-concept" that is able to demonstrate how such a system could be showcased if an even better LLM is used for generating summaries. 

## How to Run
As a prereq: to be able to run _all_ the code for this project, you would need:
- A Hopsworks.ai account
- A HuggingFace Account
- A Google account (to run the fine-tuning on Colab)
- A NewsData.io account and a subscription to the "Basic" plan (at time of writing: $150/month): this was necessary to be able to get full article content to summarize

The `T5_Finetuning_Summarization.ipynb` fine-tuning notebook can be run on Google Colab using the T4 GPU for fine-tuning. In `push_to_hub`, the HF API token we used was a "Write" type API token. Pushing your model in this way after fine-tuning should create a model with the name `outputs-project-id2223` under your HF user.

For the python code associated with the daily-feature-fetch, inference, and HF restart, we believe it would be best to fork this repository and then proceed. After the repository has been forked, to enable the execution of these things throguh GitHub itself, you would want to `Enable` the forked workflows in your forked repo. Additionally, since the workflows ran automatically at around the same time each day, you can comment out the 2-lines following `schedule` at the top of the yml file for each of these workflows (for eg: line 4-5 in [this](https://github.com/adrianxsusec/tldrify/blob/main/.github/workflows/feature.yml#L4) exmaple).



Then, if not being run automatically, the sequence of execution should be: `daily-feature-pipeline.py` --> `inference.py` --> `hf_space_restart.py`. However, to restart a HF space, we first need to get one! This should be possible by duplicating the HF Space: https://huggingface.co/spaces/shallowunlearning/tldrify-ui/tree/main (click on the "three dots", select `Duplicate this Space`). 

Finally, we will need to add the correct serets to be able to run these files properly. 3 Secrets were used by for this project on GitHub: `HOPSWORKS_API_KEY`, `NEWSDATA_API_KEY`, and `HF_API_KEY`. On HF Spaces, only one secret was used: `HOPSWORKS_API_KEY`. After this, the thing that remains is changing the names so that they're consistent with your requirements. If you wish to use your own fine-tune model (which you obtained by using the notebook above, for instance) instead of the one used for this project by us, you should change the name of the model [here](https://github.com/adrianxsusec/tldrify/blob/main/inference.py#L61). Similarly, you should change the name of the HF Space you want to restart [here](https://github.com/adrianxsusec/tldrify/blob/main/hf_space_restart.py#L7). 

So, the order of operations that seem to make the most sense to us are: `daily-feature-pipeline` --> `inference` --> `duplicate hf space` --> `code for restarting hf space`. 

## Future Work and Ideas
We have alluded to some areas that could be worked on in the future at different points in the report. Here, we discuss briefly some of our suggestions

### Using Larger Base Models (eg: T5-Large)
Instead of relying on T5-small, if there are no immediate constraints on the resources (such as time or the availability of compute), then one could consider using a larger base LLM to perform the fine-tuning on: such as the T5-Large. Larger models, since they have more parameters, could be good candidates to be able to discern more complex relationships between data-points and thus could generate more accurate summaries. The downside here is the fine-tuning and inference time could also increase. So, it is a delicate balance that needs to be looked and decided upon after a careful consideration of the resources at hand.

### Adding more Filter Criteria
Instead of having only 2 filter criterias (country and category), we can add more criterias to allow users to pick articles based on even more options. For instance, one easy criteria to add could be the source of the news, the length of the content that is being summarized, etc. A "meta" criteria could be the sentiment of the news (positive, neutral, negative): where we can use sentiment analysis tools to gather the sentiment of the _content_ of the news being summarized, and then allow users to pick what "kind" of news they'd like to read. 

### Richer Querying Language with Error Handling
The Querying Language at the moment just supports conjunctions between different filter-criterias (ie, get me news that has critera-A AND criteria-B). One other improvement that can be done to make the querying more rich is the addition of `or` between filter criterias (which can be denoted symbolically by `|` for instance). This would then likely also require for the addition of support for parenthesis and "order of operations" -- in cases where `|` and `&` are used in the same query. The querying language can also get more rich in terms of returning errors to display to the user when, for instance, they use a symbol not recognized by our querying-language. 

TODO: Add some more future-work things related to inference maybe? 
