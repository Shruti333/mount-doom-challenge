# Challenge details

<!-- Add detailed description here -->
# Mount Doom Transcript Processing System



A scalable system for processing voice agent transcripts with LLM-based analysis, designed to handle ~1,000 transcripts in 5-10 minutes.

## Features

- High-throughput processing with adaptive queuing
- LLM-powered analysis using GPT-4o-mini
- Three queue implementations for different scaling needs
- Real-time monitoring of processing metrics
- Resilient architecture with retry mechanisms
- Containerized deployment with Docker

## System Components

### Core Modules

| Module | Purpose |
|--------|---------|
| `api/` | API client and data models |
| `processing/` | LLM analysis pipelines |
| `queue/` | Queue implementations |
| `storage/` | Database operations |
| `app.py` | Main application entry |

### Queue Implementations

1. ## Redis Queue ## (`queue/queue.py`)  
   - Production-grade persistent queue
   - Maximum throughput (~10K ops/sec)

2. ## Adaptive Memory Queue ##  (`queue/queue_v2.py`)  
   - Self-tuning batch processing
   - No external dependencies


## Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/mount-doom-challenge.git
cd mount-doom-challenge

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env