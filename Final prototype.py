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

def generate_question_ai(text):
    prompt = f"""
Create one quiz question based on the text below.

Format EXACTLY like this:
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
  
    return response.chioces[0[.message.content


def parse_response(ai_text):
    lines = ai_text.split("\n")

    q, a, e = "", "", ""

    for line in lines:
        if line.lower().startswith("question"):
            q = line.split(":", 1)[1].strip()
        elif line.lower().startswith("answer"):
            a = line.split(":", 1)[1].strip()
        elif line.lower().startswith("explanation"):
            e = line.split(":", 1)[1].strip()

    return q, a, e

print("AI quiz system")
print("Type 'pdf' to upload a file or 'text' to paste notes:")
choice = input("> ").lower()

if choice =="pdf":
  path = input("enter pdf path here: ")
  text = extract_text_from_pdf(path)

else:
  print("Paste your notes (press ENTER twice to finish):")

  lines = []
  while True:
    line = input()
    if line == "":
      break
    lines.append(line)

  text = "\n".join(lines)

print("\n--- Generating Quiz ---\n")
  
for i in range(3):

  try:
    ai_output = generate_question_ai(text)
        question, answer, explanation = parse_response(ai_output)

        print(f"Q{i+1}: {question}")
        user_answer = input("Your answer: ")

        if user_answer.strip().lower() == answer.lower():
            print("✅ Correct!")
            xp += 10
            streak += 1

            if streak >= 2:
                xp += 5
                print("🔥 Streak bonus!")

        else:
            print("❌ Incorrect!")
            print("Correct answer:", answer)
            streak = 0
          
        print("Explanation:", explanation)

        new_level = check_level(xp)

        if new_level > level:
            level = new_level
            print(f"🎉 LEVEL UP! You are now Level {level}")

        print(f"XP: {xp} | Level: {level} | Streak: {streak}")
        print("-" * 50)

    except Exception as e:
        print("⚠️ Error generating question.")
        print(e)

print("\n✅ Quiz complete!")
