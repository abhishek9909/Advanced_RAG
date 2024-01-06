import os
from langchain_community.llms.ctransformers import CTransformers

def post_completion(prompt, temperature = 0.0, context_len = 4000):
    model_id = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
    os.environ['XDG_CACHE_HOME'] = '../assets/'
    config = { 'temperature': temperature, 'context_length': context_len, "stream": False }
    llm = CTransformers(
        model = model_id,
        model_type = "mistral",
        config = config,
    )
    print(llm.generate([prompt]))
 