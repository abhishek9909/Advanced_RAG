import os
from stream_transformers import StreamCTransformers

async def stream_completion(prompt, temperature = 0.0, context_len = 4000):
    model_id = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
    os.environ['XDG_CACHE_HOME'] = '../assets/'
    config = { 'temperature': temperature, 'context_length': context_len, 'stream': True }
    llm = StreamCTransformers(
        model = model_id,
        model_type = 'mistral',
        config = config,
    )
    async for x in llm.astream(prompt):
        yield x
    
