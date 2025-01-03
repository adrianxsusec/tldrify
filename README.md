# tldrIFY: _short on time, TALL ON NEEDS_

## General Idea
For the project for course [ID2223](https://www.kth.se/student/kurser/kurs/ID2223?l=en), we decided to create `tldrIFY`: an application that summarizes recent news articles from different regions of the world. The goal is for the program to create digestable 1-2 sentence summaries of news articles so that readers can get a quick digest of the happenings around the world without having to parse through multiple news articles themselves. 

For completing this project, we had to accomplish several tasks: such as finding an adequate real-time data source which would provide us the content of the news articles, fine-tuning our own model which was used to summarize the contents of the news articles, or creating a HuggingFace UI to show the results of our project. In this report, we will briefly go through the major steps accomplished by us in order to create `tldrIFY`.  

## Fine Tuning the T5 Model
The main task of `tldrIFY` is to summarize news articles. For the summarization task, we decided to use an LLM. However, we did not simply use a vanilla version of a publicly available LLM. Instead we decided to fine-tune an LLM so that the model we used would be better at the specific task that we wanted to perform: summarization. 

The base publicly-available LLM we deicded to use was the [T5-small](https://huggingface.co/google-t5/t5-small) model, and we used the [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/summarization.ipynb) available in the description of [this YouTube video](https://youtu.be/PyRbP9d27sk?si=OVBnmkRWMLq0r1Ml) to fine tune the T5-small model on Google Colab's T4-GPU. The notebook seems to be available at [this HuggingFace Github Repo](https://github.com/huggingface/notebooks/blob/main/examples/summarization.ipynb) as well. We decided to go with the T5-small model apart from some of the other T5 alternatives (such as [T5-base](https://huggingface.co/google-t5/t5-base) or [T5-large](https://huggingface.co/google-t5/t5-large)) because it was our understanding that it would take less amount of time to fine-tune a smaller model as opposed to larger models. Since we believe T5-small to be a "smaller" model, we felt that it would be adequate for the project. We utilized the [XSum Dataset](https://huggingface.co/datasets/EdinburghNLP/xsum) for the purposes of fine-tuning the T5-small LLM. Thus, the XSum Dataset also served as the **historical data-set** that was required as a part of the ID2223 project. We fine-tuned the T5-small LLM for 10-epochs (with pauses in between epochs as we evaluated how the model behaved with fewer epochs as well) using training and validation sets: meaning that the fine-tuning did take a non-trivial amount of time. Thus, in order to save our progress between epochs, we saved the progress of the fine-tuning of the model every 100 steps in Google Drive. Apart from epochs and saving-specific hyperparameters, we largely used the same hyperparameters that were present in the base notebook. 

The fine-tuned version of the T5-small model can be found here: https://huggingface.co/rishivijayvargiya/outputs-project-id2223

## The Real Time Dataset

## Daily Inference

## The Hugging Face Space

## Demo

## Future Work and Ideas

### Using Larger Base Models (eg: T5-Large)

