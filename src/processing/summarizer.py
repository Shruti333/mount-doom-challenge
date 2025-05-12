from openai import AsyncOpenAI
from typing import Dict, Any
import json
from ..api.models import Transcript

class Summarizer:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def summarize(self, transcript: Transcript) -> str:
        """
        Generate summary using COSTAR method prompt engineering
        Returns: Concise yet comprehensive summary text
        """
        prompt = self._build_costar_prompt(transcript)
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            response_format={"type": "json_object"},
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()

    def _build_costar_prompt(self, transcript: Transcript) -> str:
        return f"""
        [CONTEXT]
        You are a senior customer service analyst for Mount Doom tourism services. Create executive 
        summaries of customer interactions.

        [OBJECTIVE]
        Produce a 3-paragraph summary highlighting key points from the conversation.

        [STYLE]
        Professional business writing with bullet points for key action items.

        [TONE]
        Neutral but slightly cautious when discussing safety concerns.

        [AUDIENCE]
        Customer service managers and safety supervisors.

        [RESPONSE REQUIREMENTS]
        1. First paragraph: Overview of customer's intent and interest level
        2. Second paragraph: Key safety concerns and agent assessment
        3. Third paragraph: Recommended actions and follow-up items
        4. Bullet points: Specific action items extracted from conversation

        [TRANSCRIPT]
        {json.dumps(transcript.model_dump(), indent=2)}

        [EXAMPLE OUTPUT]
        The customer expressed strong interest in visiting Mount Doom as a tourist attraction...
        
        The agent identified several safety concerns including...
        
        Recommended next steps include...
        - Send safety information packet
        - Schedule follow-up call in 3 days
        - Verify permit application status
        """