import os
import asyncio
import logging
import urllib.request
import json
from typing import Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

class AgentGateway:
    """
    Asynchronous AI Agent Gateway with dynamic multi-provider failover.
    Attempts primary model; on rate-limit (429) or error, cascades automatically.
    """
    def __init__(self, primary_provider: str = "gemini"):
        self.primary = primary_provider
        self.providers = ["gemini", "anthropic", "openai"]
        if self.primary in self.providers:
            self.providers.remove(self.primary)
            self.providers.insert(0, self.primary)

    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        last_error = None
        for provider in self.providers:
            try:
                logging.info(f"Dispatching request to provider: {provider.upper()}")
                if provider == "gemini":
                    return await self._call_gemini(prompt, system_prompt)
                elif provider == "anthropic":
                    return await self._call_anthropic(prompt, system_prompt)
                elif provider == "openai":
                    return await self._call_openai(prompt, system_prompt)
            except Exception as e:
                logging.warning(f"Provider {provider.upper()} failed: {e}. Cascading to next provider...")
                last_error = e
                await asyncio.sleep(0.5)

        raise RuntimeError(f"All gateway providers failed. Last exception: {last_error}")

    async def _call_gemini(self, prompt: str, system_prompt: Optional[str]) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        body = {"contents": [{"parts": [{"text": prompt}]}]}
        if system_prompt:
            body["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'})
        loop = asyncio.get_event_loop()
        def _fetch():
            with urllib.request.urlopen(req, timeout=15) as res:
                return json.loads(res.read().decode('utf-8'))
        data = await loop.run_in_executor(None, _fetch)
        return data["candidates"][0]["content"]["parts"][0]["text"]

    async def _call_anthropic(self, prompt: str, system_prompt: Optional[str]) -> str:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured.")
        url = "https://api.anthropic.com/v1/messages"
        body = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            body["system"] = system_prompt
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        })
        loop = asyncio.get_event_loop()
        def _fetch():
            with urllib.request.urlopen(req, timeout=15) as res:
                return json.loads(res.read().decode('utf-8'))
        data = await loop.run_in_executor(None, _fetch)
        return data["content"][0]["text"]

    async def _call_openai(self, prompt: str, system_prompt: Optional[str]) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured.")
        url = "https://api.openai.com/v1/chat/completions"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        body = {"model": "gpt-4o-mini", "messages": messages}
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        loop = asyncio.get_event_loop()
        def _fetch():
            with urllib.request.urlopen(req, timeout=15) as res:
                return json.loads(res.read().decode('utf-8'))
        data = await loop.run_in_executor(None, _fetch)
        return data["choices"][0]["message"]["content"]
