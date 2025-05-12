from openai import AsyncOpenAI
from typing import Dict, Any
import json
from ..api.models import Transcript

class Extractor:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def extract(self, transcript: Transcript) -> Dict[str, Any]:
        """
        Extract structured data using COSTAR method prompt engineering
        Returns: Dict containing visitor details and questionnaire completion
        """
        prompt = self._build_costar_prompt(transcript)
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        return self._parse_extraction_response(response.choices[0].message.content)

    def _build_costar_prompt(self, transcript: Transcript) -> str:
        return f"""
        [CONTEXT]
        You are a data extraction specialist for Mount Doom tourism services. Extract structured 
        information from customer service transcripts.

        [OBJECTIVE]
        Identify and extract specific details about visitor preparedness and questionnaire completion.

        [STYLE]
        Use precise, unambiguous language. Structure output in strict JSON format.

        [TONE]
        Factual and objective.

        [AUDIENCE]
        Database system and downstream analytics applications.

        [RESPONSE FORMAT]
        {{
            "visitor_details": {{
                "ring_bearer": bool,
                "gear_prepared": bool,
                "hazard_knowledge": "limited/moderate/extensive",
                "fitness_level": "low/moderate/high",
                "permit_status": "none/pending/approved"
            }},
            "questionnaire_completion": {{
                "purpose_of_visit": bool,
                "experience_level": bool,
                "risk_acknowledgment": bool,
                "gear_assessment": bool,
                "item_disposal_intent": bool
            }},
            "metadata_accuracy": float (0-1)
        }}

        [TRANSCRIPT]
        {json.dumps(transcript.model_dump(), indent=2)}
        """

    def _parse_extraction_response(self, response: str) -> Dict[str, Any]:
        try:
            data = json.loads(response)
            # Validate required fields
            if not all(k in data for k in ["visitor_details", "questionnaire_completion"]):
                raise ValueError("Missing required fields")
            return data
        except (json.JSONDecodeError, ValueError) as e:
            return {
                "error": f"Extraction failed: {str(e)}",
                "raw_response": response
            }