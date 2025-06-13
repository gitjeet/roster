import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

load_dotenv()


genai.configure(api_key=os.getenv("GEMINIKEY"))
model = genai.GenerativeModel("gemini-2.0-flash")  

def extract_structured_data(text: str) -> dict:
    prompt = f"""
You are a machine assistant that returns only valid JSON. Do not include markdown, explanation, or comments. Include employer information, such as clients, collaborators, companies, brands, or individuals the talent has worked with, even if not explicitly labeled
Extract structured talent profile data from the text below.

TEXT:
{text[:4000]}

Respond with JSON only:
{{
  "username": "string",
  "name": "string",
  "bio": "string",
  "email": "string",
  "employers": [
    {{
      "name": "string",
      "videos": [{{ "url": "string" }}]
    }}
  ]
}}
"""

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        # Remove any markdown formatting if present
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        # Try to parse it as JSON
        return json.loads(content)

    except json.JSONDecodeError as e:
        print("Gemini raw response:\n", content)
        raise Exception("Gemini returned non-JSON content.")
    except Exception as e:
        raise Exception(f"Gemini data extraction failed: {e}")

def process_website(url: str) -> dict:
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        text_content = soup.get_text(separator=" ", strip=True)

        data = extract_structured_data(text_content)

        return {
            "username": data.get("username") or "user",  
            "name": data.get("name", "Unknown Name"),
            "bio": data.get("bio", "No bio provided"),
            "email": data.get("email") or f"{data.get('username', 'user')}@example.com",
            "website": url,
            "employers": data.get("employers", [])
        }


    except Exception as e:
        raise Exception(f"Error scraping website: {e}")
