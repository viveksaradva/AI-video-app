"""
This module contains the prompt templates used for generating ad scripts.
"""

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

Client's campaign idea: "{user_prompt}"
"""
    
    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt_template
    }
