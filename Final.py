import os 
from PyPDF2 import PdfReader
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

xp = 0
level = 1
streak = 0

def Check_Level(xp):
  return xp // 100 + 1

def extract_text_from_pdf(file_path):
  reader = PdfReader(file_path)
  text = ""

  for page in reader.page:
    page_text = page.extract_text()
    if page_text:
      text += page_text + "\n"
  return text
