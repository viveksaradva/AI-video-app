import os
import json
import requests
from typing import List, Dict
from dotenv import load_dotenv
from urllib.parse import quote_plus
from module.script import generate_ad_script
from sentence_transformers import SentenceTransformer, util

load_dotenv()

class VideoFinderAgent:
    
    def __init__(self, api_key: str, per_page: int = 10):
        self.api_key = api_key
        self.per_page = per_page
        self.base_url = "https://pixabay.com/api/videos/"
        self.embed_model = SentenceTransformer('all-mpnet-base-v2')

    def search_videos(self, query: str) -> List[Dict]:
        # Only key and q parameters for broad matching
        url = f"{self.base_url}?key={self.api_key}&q={quote_plus(query)}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json().get('hits', [])

    def rank_candidates(self, description: str, videos: List[Dict]) -> Dict:
        scene_emb = self.embed_model.encode(description, convert_to_tensor=True)
        best_candidate = max(
            (video for video in videos if video.get('tags')),
            key=lambda v: util.cos_sim(
                scene_emb,
                self.embed_model.encode(v['tags'], convert_to_tensor=True)
            ).item(),
            default=videos[0]
        )
        return best_candidate

    def get_best_file(self, video: Dict) -> Dict:
        """
        Select the highest resolution file from the video entry.
        """
        return max(
            video.get('videos', {}).values(),
            key=lambda f: f.get('width', 0) * f.get('height', 0),
            default={}
        )
    
    def find_best_clip(self, scene: Dict) -> Dict:
        """
        Use scene-provided 'search_query' to fetch and pick the best clip.
        """
        query = scene.get('search_query', '') 
        candidates = self.search_videos(query)
        if not candidates:
            return {'error': 'no_videos_found', 'query': query}

        # Re‑rank returned candidates by semantic similarity
        best_video = self.rank_candidates(
            scene.get('visual_description', ''),
            candidates
        )
        best_file = self.get_best_file(best_video)

        return {
            'scene_query': query,
            'pixabay_video_id': best_video.get('id'),
            'page_url': best_video.get('pageURL'),
            'duration_s': best_video.get('duration'),
            'tags': best_video.get('tags'),
            'thumbnail_url': best_file.get('thumbnail'),
            'video_file_url': best_file.get('url'),
            'resolution': f"{best_file.get('width')}x{best_file.get('height')}",
            'file_size': best_file.get('size')
        }

    def process_script(self, script: List[Dict]) -> Dict[int, Dict]:
        """
        For each scene dict (with 'search_query' field), find and return best-clip info.
        """
        return {
            scene.get('scene'): self.find_best_clip(scene)
            for scene in script
        }


if __name__ == '__main__':

    prompt = "Promote a short Europe travel spot highlighting no-quarantine rules."
    script = generate_ad_script(prompt)
    print(f"The generated script: {script}")

    agent = VideoFinderAgent(api_key=os.getenv('PIXABAY_API_KEY'), per_page=50)
    # ipdb.set_trace()
    clips = agent.process_script(script)

    print(f"\nThe clips found: {json.dumps(clips, indent=2, ensure_ascii=False)}")