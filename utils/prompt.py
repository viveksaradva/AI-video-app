def get_ad_script_prompt(user_prompt: str) -> str:
    """
    Returns the system and user prompts for the ad script generation.
    
    Args:
        user_prompt: The campaign idea provided by the user
        
    Returns:
        The formatted prompt to send to the LLM
    """
    system_prompt = "You are an expert ad scriptwriter."
    
    user_prompt_template = f"""
You are a world-class creative ad scriptwriter with a talent for storytelling, visual poetry, and bold branding. 
Your task is to help a client transform their campaign idea into a **unique and imaginative** 30-second(or whatever length the client wants) video script.

This video should stand out — use bold visuals, a compelling story arc (even if it's just 4-5 scenes), and integrate the brand **organically** into the narrative, not as a hard sell. 
Think cinematic, emotional, funny, surreal, or metaphorical — whatever brings the brand to life in a **fresh and memorable** way.

For each scene, in addition to the usual fields, **provide an array of the top most prioritized search‑focused keywords** that best capture the visual concept (short, noun‑based, 1–2 words each) so we can use them directly to query stock video APIs. Avoid including uncommon or abstract terms like 'montage', 'cinematic', 'emotion', or 'aesthetic' — use words likely to appear as tags in stock video libraries like locations, actions, objects, people, or nature terms.”

Your output should be in JSON format with 2–4 creative scenes (total duration ≈15 seconds), following this structure:

[
  {{"scene": 1,
    "duration": "e.g. 5s",
    "visual_description": "Describe what the viewer sees — set the scene with mood, movement, and atmosphere.",
    "dialogue": "Voice-over or character dialogue. Use tone to match the idea: witty, emotional, bold, mysterious, etc.",
    "on_screen_text": "Any text appearing on screen: taglines, punchlines, product names, etc.",
    "search_query": "concise, noun‑based phrase (2–4 words) ideal for querying stock video libraries"
  }},
  ...
]

**Important:** The `search_query` should be a **single, highly relevant phrase**, composed of terms likely found as tags in stock‑video APIs. Avoid abstract or artistic words (e.g., “montage”, “cinematic”, “emotion”).  

Client's campaign idea: "{user_prompt}"
"""

    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt_template
    }
