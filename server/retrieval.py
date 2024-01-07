### Given a text string, chunk and index.
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from completion import get_completion
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from sentence_transformers import CrossEncoder

### Given a text string, chunk and index the same as db.
def index_documents_to_db(text, collection_name = "default"):
    chunks = _divide_text_into_chunks(text)
    tokens = _convert_chunks_to_tokens(chunks)        
    collection = _create_index_from_tokens(tokens, collection_name)
    return collection

### Given a text string and embedding, search over the index.
def retrieve_additional_context(text, collection_name, n_docs = 5, query_expansion = 0, n_top = 10):
    collection = chromadb.PersistentClient("../assets/chromadb/").get_collection(collection_name)
    query_list = _get_expanded_queries(text, query_expansion)
    results = collection.query(query_texts=query_list, n_results=n_docs)
    retrieved_documents = list(set([document for querywise_documents in results["documents"] for document in querywise_documents]))
    if query_expansion > 0:
        retrieved_documents = _rerank_results_cross_encoder(retrieved_documents, text, n_top)
    return '\n'.join(retrieved_documents)

### deletes collection and frees up space.
def delete_collection_from_local_storage(collection_name):
    collection = chromadb.PersistentClient("../assets/chromadb/")
    collection.delete_collection(collection_name)

def _get_expanded_queries(text, expansion_factor = 0):
    expanded_query = [text]
    if expansion_factor > 0:
        response = get_completion(f"Write {expansion_factor} ways to rephrase the query: {text}, response should be separated by escape and there should be no other text preceding or after it")
        expanded_query.extend(response.generations[0][0].text.split('\n'))
    return expanded_query       


def _divide_text_into_chunks(text):
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ", ", " ", ""],
        chunk_size = 1000
    )
    chunks = character_splitter.split_text(text)
    return chunks

def _convert_chunks_to_tokens(chunks):
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
    tokens = []
    for chunk in chunks:
        tokens += token_splitter.split_text(chunk)
    return tokens

def _create_index_from_tokens(tokens, collection_name):
    ids = [str(i) for i in range(len(tokens))]
    embedding_function = SentenceTransformerEmbeddingFunction()
    client = chromadb.PersistentClient("../assets/chromadb/")
    collection = client.create_collection(collection_name, embedding_function=embedding_function)
    collection.add(ids = ids, documents = tokens)    
    return collection

def _rerank_results_cross_encoder(retrieved_documents, original_query, top_n = 10):
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    inference_pairs = [[original_query, doc] for doc in retrieved_documents]
    inference_scores = cross_encoder.predict(inference_pairs)
    retrieved_documents_with_scores = list(zip(retrieved_documents, inference_scores))
    sorted_doc_with_scores = sorted(retrieved_documents_with_scores, key=lambda x:-x[1])
    top_docs = [a[0] for a in sorted_doc_with_scores[0:top_n]]
    return top_docs