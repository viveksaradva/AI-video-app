import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# ——— CONFIG ———
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)  

# ——— SCRIPT GENERATOR ———
def generate_ad_script(prompt: str) -> list:
    """
    Sends the user prompt to Groq's mistral-saba-24b model and returns
    a list of scene dicts:
    [
      {
        "scene": 1,
        "duration": "5s",
        "visual_description": "...",
        "dialogue": "...",
        "on_screen_text": "..."
      },
      ...
    ]
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an expert ad scriptwriter."},
            {
                "role": "user",
                "content": f"""
You are a world-class creative ad scriptwriter with a talent for storytelling, visual poetry, and bold branding. 
Your task is to help a client transform their campaign idea into a **unique and imaginative** 15-second(or whatever length the client wants) video script.

This video should stand out — use bold visuals, a compelling story arc (even if it's just 2–3 scenes), and integrate the brand **organically** into the narrative, not as a hard sell. 
Think cinematic, emotional, funny, surreal, or metaphorical — whatever brings the brand to life in a **fresh and memorable** way.

Your output should be in JSON format with 2–4 creative scenes (total duration ≈15 seconds), following this structure:

[
  {{"scene": 1,
    "duration": "e.g. 5s",
    "visual_description": "What the viewer sees — set the scene with mood, movement, and atmosphere.",
    "dialogue": "Voice-over or character dialogue. Use tone to match the idea: witty, emotional, bold, mysterious, etc.",
    "on_screen_text": "Any text appearing on screen: taglines, punchlines, product names, etc."
  }},
  ...
]

Client’s campaign idea: "{prompt}"
""",
            },
        ],
        "temperature": 0.7,
        "max_tokens": 800,
    }

    resp = requests.post(GROQ_API_URL, headers=headers, json=payload)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]

    # Parse out the JSON array
    try:
        script = json.loads(content)
    except json.JSONDecodeError:
        # If the model returns extra text, try to extract the JSON substring
        start = content.find("[")
        end = content.rfind("]") + 1
        script = json.loads(content[start:end])

    return script


# ——— USAGE ———
if __name__ == "__main__":
    user_prompt = input("Enter your campaign idea: ")
    ad_script = generate_ad_script(user_prompt)
    print(json.dumps(ad_script, indent=2))
