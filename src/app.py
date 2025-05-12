import asyncio
import logging
from .api.client import APIClient
from .queue.queue import QueueManager
from .storage.db import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    api_client = APIClient(
        base_url="https://relaxing-needed-vulture.ngrok-free.app",
        api_key="candidate-api-key-f873f865"
    )
    db = Database("postgresql+asyncpg://user:password@localhost/mountdoom")
    queue_manager = QueueManager("redis://localhost", api_client)
    
    # Start multiple workers
    workers = [queue_manager.run_worker() for _ in range(5)]
    
    # Process stream
    async for transcript in api_client.get_transcripts():
        await queue_manager.redis.lpush("transcripts", transcript.model_dump_json())
    
    await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())