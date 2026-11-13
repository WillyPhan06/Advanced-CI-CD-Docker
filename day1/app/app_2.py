import os
from dotenv import load_dotenv 

load_dotenv()

print("Application:", os.getenv("APP_NAME"))
print("Secret:", os.getenv("SECRET", "I don't know the secret!"))