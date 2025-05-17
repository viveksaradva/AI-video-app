# def get_ad_script_prompt(user_prompt: str) -> dict:
#     """
#     Returns the system and user prompts for the ad script generation.

#     Args:
#         user_prompt: The campaign idea provided by the user

#     Returns:
#         The formatted prompt to send to the LLM
#     """
#     system_prompt = "You are an expert ad scriptwriter."

#     user_prompt_template = f"""
# Your task is to help a client transform their campaign idea into a **unique and imaginative** 30-second(or whatever length the client wants) video script.

# This video should stand out — use bold visuals, a compelling story arc (even if it's just 4-5 scenes), and integrate the brand **organically** into the narrative, not as a hard sell.
# Think cinematic, emotional, funny, surreal, or metaphorical — whatever brings the brand to life in a **fresh and memorable** way.

# For each scene, in addition to the usual fields, **provide an array of the top most prioritized search‑focused keywords** that best capture the visual concept (short, noun‑based, 1–2 words each) so we can use them directly to query stock video APIs. Avoid including uncommon or abstract terms like 'montage', 'cinematic', 'emotion', or 'aesthetic' — use words likely to appear as tags in stock video libraries like locations, actions, objects, people, or nature terms.”

# Your output should be in JSON format with 2–4 creative scenes (total duration ≈15 seconds), following this structure:

# [
#   {{"scene": 1,
#     "duration": "e.g. 5s",
#     "visual_description": "Describe what the viewer sees — set the scene with mood, movement, and atmosphere.",
#     "dialogue": "Voice-over or character dialogue. Use tone to match the idea: witty, emotional, bold, mysterious, etc.",
#     "on_screen_text": "Any text appearing on screen: taglines, punchlines, product names, etc.",
#     "search_query": "concise, noun‑based phrase (2–4 words) ideal for querying stock video libraries"
#   }},
#   ...
# ]

# **Important:** The `search_query` should be a **single, highly relevant phrase**, composed of terms likely found as tags in stock‑video APIs. Avoid abstract or artistic words (e.g., “montage”, “cinematic”, “emotion”).

# Client's campaign idea: "{user_prompt}"
# """

#     return {
#         "system_prompt": system_prompt,
#         "user_prompt": user_prompt_template
#     }


def get_video_finder_prompts(scene_description: str, video_info_text: str = None) -> dict:
    """
    Returns the prompts for the video finder agent.

    Args:
        scene_description: Natural language description of the scene
        video_info_text: Optional text containing information about videos to rank

    Returns:
        Dictionary containing the search_terms_prompt and rank_videos_prompt
    """
    # Prompt for generating search terms
    search_terms_prompt = f"""
    I need to find ONE perfect video clip that precisely matches this scene description:

    "{scene_description}"

    Generate 3 highly specific search queries I should use to find this exact video on Pixabay.
    Focus on the most distinctive visual elements, actions, and settings that would be present.
    Be precise and concrete rather than abstract or conceptual.

    List only the search terms, each on a new line, without numbering or additional explanations.
    """

    # Prompt for ranking videos (only used if video_info_text is provided)
    rank_videos_prompt = None
    if video_info_text:
        rank_videos_prompt = f"""
        I need to find THE SINGLE BEST video clip that perfectly matches this scene description:

        "{scene_description}"

        Here are potential video options from Pixabay:

        {video_info_text}

        Analyze each video's tags and attributes carefully. Consider how well each video would visually represent the scene.

        Return ONLY the number of the single best video (e.g., "3"). Do not return multiple numbers or any other text.
        """

    return {
        "search_terms_prompt": search_terms_prompt,
        "rank_videos_prompt": rank_videos_prompt
    }

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from utils.models import ScriptOutput

script_parser = PydanticOutputParser(pydantic_object=ScriptOutput)

script_prompt = PromptTemplate(
    template="""
You are an expert ad scriptwriter.

Your task is to help a client transform their campaign idea into a **unique and imaginative** 30-second (or whatever length the client wants) video script.

This video should stand out — use bold visuals, a compelling story arc (even if it's just 4-5 scenes), and integrate the brand **organically** into the narrative, not as a hard sell.
Think cinematic, emotional, funny, surreal, or metaphorical — whatever brings the brand to life in a **fresh and memorable** way.

For each scene, in addition to the usual fields, **provide an array of the top most prioritized search‑focused keywords** that best capture the visual concept (short, noun‑based, 1–2 words each) so we can use them directly to query stock video APIs. Avoid including uncommon or abstract terms like 'montage', 'cinematic', 'emotion', or 'aesthetic' — use words likely to appear as tags in stock video libraries like locations, actions, objects, people, or nature terms.

Your output should be in JSON format with 2–4 creative scenes (total duration ≈15 seconds), following this structure:

[
  {{
    "scene": 1,
    "duration": "e.g. 5s",
    "visual_description": "Describe what the viewer sees — set the scene with mood, movement, and atmosphere.",
    "dialogue": "Voice-over or character dialogue. Use tone to match the idea: witty, emotional, bold, mysterious, etc.",
    "on_screen_text": "Any text appearing on screen: taglines, punchlines, product names, etc.",
    "search_query": "concise, noun‑based phrase (2–4 words) ideal for querying stock video libraries"
  }},
  ...
]

**Important:** The `search_query` should be a **single, highly relevant phrase**, composed of terms likely found as tags in stock‑video APIs. Avoid abstract or artistic words (e.g., “montage”, “cinematic”, “emotion”).

{format_instructions}

Client's campaign idea: {user_prompt}
""",
    input_variables=["user_prompt"],
    partial_variables={"format_instructions": script_parser.get_format_instructions()}
)