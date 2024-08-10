import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_REPO = os.getenv(
        "GITHUB_REPO", "https://api.github.com/repos/nitdraig/roger"
    )


config = Config()
