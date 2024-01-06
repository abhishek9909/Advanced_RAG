import os
from langchain.llms import CTransformers

model_id = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
os.environ['XDG_CACHE_HOME'] = '../assets/'
llm = CTransformers(
    model = model_id,
    model_type = "mistral",
)