import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("CF_DIST_ID"))