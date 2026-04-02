import os 
from PyPDF2 import PdfReader
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

xp = 0
level = 1
streak = 0

def check_Level(xp):
  return xp // 100 + 1

def save_progress(xp, level, streak):
  data = {"xp": xp, "level": level, "streak": streak}
  with open("progress.json", "w") as f:
    json.dump(data, f)

def load_progress():
  try:
    with open("progress.json", "r") as f:
            return json.load(f)
    except:
        return {"xp": 0, "level": 1, "streak": 0}

progress = load_progress()
xp = progress["xp"]
level = progress["level"]
streak = progress["streak"]

#Pdf text extraction

def extract_text_from_pdf(file_path):
  reader = PdfReader(file_path)
  text = ""

  for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
      text += page_text + "\n"
  return text

# AI questions generator 
def generate_question_ai(text):
    prompt = f"""
Create one {difficulty} quiz question based on the text below.

Randomly choose ONE type:
- Multiple choice (A, B, C, D)
- True/False
- Short answer

Format EXACTLY like this:
Type: ...
Question: ...
Answer: ...
Explanation: ...

Text:
{text[:1500]}
"""
    response = client.chat.completions.create(
      model="gpt-4.1-mini",
      messages=[{"role": "user", "content": prompt}]
    )
  
    return response.choices[0].message.content

#Parse responses
def parse_response(ai_text):
    lines = ai_text.split("\n")

    q, a, e = "", "", ""

    for line in lines:
        if line.lower().startswith("type"):
            t = line.split(":", 1)[1].strip()
        elif line.lower().startswith("question"):
            q = line.split(":", 1)[1].strip()
        elif line.lower().startswith("answer"):
            a = line.split(":", 1)[1].strip()
        elif line.lower().startswith("explanation"):
            e = line.split(":", 1)[1].strip()
          
    return t, q, a, e
#input system
print("AI quiz system")
print("Type 'pdf' to upload a file or 'text' to paste notes:")
choice = input("> ").lower()

if choice =="pdf":
  path = input("enter pdf path here: ")
  text = extract_text_from_pdf(path)

 if not text.strip():
        print("⚠️ No text found in PDF.")
        exit()

else:
  print("Paste your notes (press ENTER twice to finish):")

  lines = []
  while True:
    line = input()
    if line == "":
      break
    lines.append(line)

  text = "\n".join(lines)

# Quiz Setup

num_questions = int(input("How many questions? "))

print("\n--- Generating Quiz ---\n")
#Quiz Loop

for i in range(num_questions):

    print("\n" + "="*50)
    print(f"QUESTION {i+1}")
    print("="*50)

  try:
        difficulty = "easy"
        if level >= 3:
            difficulty = "medium"
        if level >= 5:
            difficulty = "hard"

    ai_output = generate_question_ai(text, difficulty)
    question, answer, explanation = parse_response(ai_output)

        print(f"Type: {q_type}")
        print(f"Q: {question}")
        user_answer = input("Your answer: ")

        if check_answer(user_answer.strip(), answer):
            print("Correct!")
            xp += 10
            streak += 1

            if streak >= 2:
                xp += 5
                print("Streak bonus!")

        else:
            print("❌ Incorrect!")
            print("Correct answer:", answer)
            streak = 0
          
        print("Explanation:", explanation)
   # Level system
        new_level = check_level(xp)
        if new_level > level:
            level = new_level
            print(f LEVEL UP! You are now Level {level}")

        print(f"XP: {xp} | Level: {level} | Streak: {streak}")
        print("-" * 50)

         # Save progress
        save_progress(xp, level, streak)
        except Exception as e:
        print("Error generating question.")
        print(e)

print("\n FINAL RESULTS")
print(f"XP: {xp}")
print(f"Level: {level}")
print("Quiz complete!")
