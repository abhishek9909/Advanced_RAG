### Flask app containing these endpoints:
### 1. CRUD index/DB provided document_stream, name, hyperparameters (chunk_size)
### 2. Query index provided name, query, hyperparameters(n_top, n_query_expansion)

from completion import stream_completion
from flask import Flask, request
from ingestion import prepare_text
from retrieval import delete_collection_from_local_storage, index_documents_to_db, find_all_collections, retrieve_additional_context

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/indexes", methods=['GET'])
def get_all_indexes():
    return find_all_collections()

@app.route("/index/<index_id>", methods=['DELETE'])
def delete_index(index_id):
    try:
        delete_collection_from_local_storage(index_id)
        return True
    except:
        return False
    
@app.route("/index", methods=['POST'])
def create_index():
    request_data = request.json()
    response = {}
    try:
        file_path, name, pform = request_data['path'], request_data['name'], request_data['pform']
        text = prepare_text(file_path=file_path, data_type=pform)
        collection = index_documents_to_db(text, name)
        response = {'text': f'A collection created with name: {name} and count: {collection.count()}'}
    except Exception as e:
        response = { 'text': 'Error in creating collection', 'info': str(e) }
    return response

@app.route("/rag", methods=['POST'])
async def stream_response():
    request_data = request.json()
    query, collection_name = request_data['query'], request_data['collection_name']
    information = retrieve_additional_context(query, collection_name)
    full_query = f"Query: {query}, information: {information}"
    return stream_completion(full_query)