import os 
from PyPDF2 import PdfReader
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

xp = 0
level = 1
streak = 0
