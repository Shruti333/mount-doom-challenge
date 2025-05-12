from openai import AsyncOpenAI
from typing import Dict, Any
import json
from ..api.models import Transcript

class Analyzer:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def analyze(self, transcript: Transcript) -> Dict[str, Any]:
        """
        Analyze transcript using COSTAR method prompt engineering
        Returns: Dict containing sentiment analysis, risk assessment, and action items
        """
        prompt = self._build_costar_prompt(transcript)
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        return self._parse_analysis_response(response.choices[0].message.content)

    def _build_costar_prompt(self, transcript: Transcript) -> str:
        return f"""
        [CONTEXT]
        You are a senior safety analyst for Mount Doom tourism services. Analyze customer service 
        transcripts to assess visitor risk and recommend appropriate actions.

        [OBJECTIVE]
        Extract sentiment, risk factors, and generate specific action items from the transcript.

        [STYLE]
        Use professional but concise language. Structure findings in JSON format.

        [TONE]
        Serious and safety-focused, but not alarmist.

        [AUDIENCE]
        Mount Doom safety team and customer service supervisors.

        [RESPONSE FORMAT]
        {{
            "sentiment": {{
                "score": float (0-1),
                "label": "positive/neutral/negative",
                "key_phrases": list[str]
            }},
            "risk_assessment": {{
                "level": "low/medium/high",
                "factors": list[str],
                "immediate_concerns": bool
            }},
            "action_items": list[str]
        }}

        [TRANSCRIPT]
        {json.dumps(transcript.model_dump(), indent=2)}
        """

    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse analysis response",
                "raw_response": response
            }