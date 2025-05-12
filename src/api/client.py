import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from .models import Transcript, ProcessedResult

class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.token = None
        self.client = httpx.AsyncClient(timeout=30.0)
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def authenticate(self):
        response = await self.client.post(
            f"{self.base_url}/auth",
            json={"api_key": self.api_key}
        )
        response.raise_for_status()
        self.token = response.json().get("token")
        return self.token
        
    async def get_transcripts(self):
        if not self.token:
            await self.authenticate()
            
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        async with self.client.stream(
            "GET",
            f"{self.base_url}/v1/transcripts/stream",
            headers=headers
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    yield Transcript.model_validate_json(line)
                    
    async def submit_result(self, result: ProcessedResult):
        if not self.token:
            await self.authenticate()
            
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        response = await self.client.post(
            f"{self.base_url}/v1/transcripts/process",
            headers=headers,
            json=result.model_dump()
        )
        response.raise_for_status()
        return response.json()