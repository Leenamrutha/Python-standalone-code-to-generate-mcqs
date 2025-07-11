import hashlib
import os
import json
import pdfplumber
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


# Set API Key
genai.configure(api_key="AIzaSyDkmAcu3dXXxl83Ll1Vb3DxIHVsd2N-zvc")  # Replace with your Gemini API key

#print("\n[INFO] Available models:")
#for model in genai.list_models():
#    print(f"- {model.name}")


# Setup cache
base_dir = os.getcwd()
CACHE_DIR = os.path.join(base_dir, "mcq_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
print(f"[INFO] Cache directory: {CACHE_DIR}")

def extract_text_from_pdf(pdf_path):
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception as e:
        print(f"[ERROR] Failed to extract text from PDF: {e}")
    return full_text.strip()

def create_prompt(text_content, difficulty='medium', num_questions=5):
    return f"""
You are an expert biology teacher.

Given the following content:

{text_content}

Please generate {num_questions} multiple-choice questions (MCQs) based on this content.

- 4 options (A, B, C, D)
- Mark correct answer
- Provide a short explanation or reference
- Difficulty: {difficulty}

Return the result as a JSON array:
[
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "A",
    "reference": "..."
  }}
]
"""

def hash_content(text, difficulty):
    combined = text.strip() + difficulty.strip().lower()
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()

def cache_exists(hash_key):
    return os.path.exists(os.path.join(CACHE_DIR, f"{hash_key}.json"))

def read_cache(hash_key):
    with open(os.path.join(CACHE_DIR, f"{hash_key}.json"), 'r', encoding='utf-8') as f:
        return json.load(f)

def write_cache(hash_key, data):
    with open(os.path.join(CACHE_DIR, f"{hash_key}.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def generate_mcqs_with_cache(text, difficulty='medium'):
    hash_key = hash_content(text, difficulty)

    if cache_exists(hash_key):
        print("[CACHE HIT] Loaded from cache.\n")
        return read_cache(hash_key)

    print("[CACHE MISS] Calling Gemini...\n")
    prompt = create_prompt(text, difficulty)

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        print("[DEBUG] Raw response:")
        print(response)

    # Extract the JSON string from the response
        if hasattr(response, 'candidates') and response.candidates:
            response_text = response.candidates[0].content.parts[0].text
            # Remove the code block formatting
            response_text = response_text.strip("```json\n").strip("```")
        else:
            print("[ERROR] No candidates found in the response.")
            return []

        # Parse the JSON
        mcqs = json.loads(response_text)
        write_cache(hash_key, mcqs)
    
        return mcqs
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parsing failed: {e}")
        print("[DEBUG] Response text was:\n", response_text)
        return []
    except Exception as e:
        print(f"[ERROR] Gemini API call failed: {e}")
        return []


def main(pdf_path, difficulty='medium'):
    if not os.path.isfile(pdf_path):
        print(f"[ERROR] File not found: {pdf_path}")
        return

    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("[ERROR] No text found in the PDF.")
        return

    mcqs = generate_mcqs_with_cache(text, difficulty)

    for i, q in enumerate(mcqs, start=1):
        print(f"Q{i}: {q['question']}")
        for opt_key, opt_val in q['options'].items():
            print(f"   {opt_key}. {opt_val}")
        print(f"Answer: {q['correct_answer']}")
        print(f"Reference: {q['reference']}\n")

if __name__ == "__main__":
    main("biology_chapter1.pdf", difficulty='medium')
