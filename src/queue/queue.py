import asyncio
import logging
from redis import asyncio as aioredis
from src.api.client import APIClient  
from src.processing.summarizer import Summarizer
from src.processing.extractor import Extractor
from src.processing.analyzer import Analyzer

...

\
from src.api.models import Transcript  # Import the Transcript class
api_client = APIClient(
    base_url="https://relaxing-needed-vulture.ngrok-free.app",
    api_key="candidate-api-key-f873f865"
)

logger = logging.getLogger(__name__)

class QueueManager:
    def __init__(self, redis_url, api_client):
        self.redis = aioredis.from_url(redis_url)
        
        self.summarizer = Summarizer()
        self.extractor = Extractor()
        self.analyzer = Analyzer()
        
       
        
    async def process_transcript(self, transcript):
        summary = await self.summarizer.summarize(transcript)
        structured_data = await self.extractor.extract(transcript)
        analysis = await self.analyzer.analyze(transcript)
        
        return {
            "transcript_id": transcript.transcript_id,
            "summary": summary,
            "structured_data": structured_data,
            "analysis": analysis
        }
        
    async def run_worker(self):
        while True:
            transcript_data = await self.redis.lpop("transcripts")
            if transcript_data:
                transcript = Transcript.model_validate_json(transcript_data)
                result = await self.process_transcript(transcript)
                await api_client.submit_result(result)