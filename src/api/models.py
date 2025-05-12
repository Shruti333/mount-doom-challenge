from pydantic import BaseModel
from typing import List, Dict, Optional

class TranscriptParticipant(BaseModel):
    speaker: str
    text: str
    timestamp: str

class TranscriptMetadata(BaseModel):
    questionnaire: Dict[str, bool]
    visitor_interest_level: str
    potential_issue: str
    mount_doom_permit_status: str
    language: str

class Transcript(BaseModel):
    transcript_id: str
    session_id: str
    timestamp: str
    agent_type: str
    duration_seconds: int
    participants: Dict[str, str]
    transcript_text: List[TranscriptParticipant]
    metadata: TranscriptMetadata

class ProcessedResult(BaseModel):
    transcript_id: str
    summary: str
    structured_data: Dict
    analysis: Dict
    processing_timestamp: Optional[str] = None