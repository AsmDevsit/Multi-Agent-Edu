import os
from dotenv import load_dotenv
def load_environment():
    load_dotenv(".env")
    os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
