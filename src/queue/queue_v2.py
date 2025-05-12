import asyncio
import time
import logging
from fastapi import APIRouter
from src.api.client import APIClient
from src.api.models import Transcript
from src.processing import summarizer, extractor, analyzer
from src.processing.summarizer import Summarizer
from src.processing.extractor import Extractor
from src.processing.analyzer import Analyzer

...

summarizer_instance = Summarizer()
extractor_instance = Extractor()
analyzer_instance = Analyzer()

router = APIRouter()

# Configuration
QUEUE_CONCURRENCY = 20
MAX_QUEUE_SIZE = 2000
MAX_TRANSCRIPTS = 1000

# Globals
queue = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)
processing_durations = []

client = APIClient(
    base_url="https://relaxing-needed-vulture.ngrok-free.app",
    api_key="candidate-api-key-f873f865"
)



async def process_transcript(transcript: Transcript):
    start = time.time()
    summary = await summarizer_instance.summarize(transcript)
    structured_data = await extractor_instance.extract(transcript)
    analysis = await analyzer_instance.analyze(transcript)
    duration = time.time() - start
    processing_durations.append(duration)

    return {
        "transcript_id": transcript.transcript_id,
        "summary": summary,
        "structured_data": structured_data,
        "analysis": analysis
    }

async def worker():
    while True:
        transcript = await queue.get()
        try:
            result = await process_transcript(transcript)
            await client.submit_result(result)
        except Exception as e:
            logging.error(f"Error processing transcript {transcript.transcript_id}: {e}")
        finally:
            queue.task_done()

async def fill_queue():
    count = 0
    async for transcript in client.get_transcripts():
        if count >= MAX_TRANSCRIPTS:
            break
        await queue.put(transcript)
        count += 1

@router.on_event("startup")
async def start_queue_processing():
    asyncio.create_task(start_workers())

async def start_workers():
    logging.info("Starting workers and filling queue")
    # Fill the queue
    await fill_queue()

    # Start workers
    workers = [asyncio.create_task(worker()) for _ in range(QUEUE_CONCURRENCY)]

    # Wait for completion
    await queue.join()
    for w in workers:
        w.cancel()

    if processing_durations:
        logging.info(f"All transcripts processed.")
        logging.info(f"Max transcript processing time: {max(processing_durations):.2f}s")
        logging.info(f"Total time (bounded by slowest): {max(processing_durations):.2f}s")
    else:
        logging.warning("No transcripts were processed.")

@router.get("/queue/health")
async def health_check():
    return {
        "status": "running",
        "queue_size": queue.qsize(),
        "max_processing_time_sec": max(processing_durations) if processing_durations else 0.0
    }
