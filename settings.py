import os
from os import path
from dotenv import load_dotenv

load_dotenv(path.expanduser("~/img-trading-etl/.env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")