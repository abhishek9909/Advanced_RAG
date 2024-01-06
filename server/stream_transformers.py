from functools import partial
from typing import Any, AsyncIterator, List, Optional
from langchain_community.llms.ctransformers import CTransformers
from langchain_core.callbacks.manager import AsyncCallbackManagerForLLMRun
from langchain_core.outputs import GenerationChunk

class StreamCTransformers(CTransformers):
    async def _astream(self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[GenerationChunk]:
        text_callback = None
        if run_manager:
            text_callback = partial(run_manager.on_llm_new_token, verbose=self.verbose)
        
        for token in self.client(prompt, stop=stop, stream=True):
            token_chunk = GenerationChunk(text=token)
            if text_callback:
                await text_callback(token)
            yield token_chunk