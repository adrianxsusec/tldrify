import os
from huggingface_hub import HfApi

def restart_space():
    token = os.environ["HF_API_KEY"]
    api = HfApi(token=token)
    api.restart_space(repo_id="shallowunlearning/tldrify-ui")

if __name__ == "__main__":
    restart_space()