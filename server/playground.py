import asyncio
from completion import stream_completion
from ingestion import prepare_text
from retrieval import index_documents_to_db, delete_collection_from_local_storage, retrieve_additional_context

async def print_completion():
    async for x in stream_completion("Write a poem on America in 50 words or less"):
        print(x)

if __name__ == "__main__":
    
    # exp-1: streaming completion.
    #asyncio.run(print_completion())
    
    # exp-2: extracting text from doc.
    #print(prepare_text("../assets/mock_input/Professional_Resume.pdf", extension='.pdf'))
    #text = prepare_text("../assets/mock_input/loss_functions.pdf", extension='.pdf', data_type='image')
    
    # exp-3: index documents to collection.
    #collection = index_documents_to_db(text, "vector-check")
    #print(f"count: {collection.count()}")
    
    # exp-4: delete documents from collection.
    # delete_collection_from_local_storage("vector-check")
    
    # exp-5: querying additional context.
    #content = retrieve_additional_context("What is sigmoid loss function", "example")
    #print(content)
    
    # exp-6: querying additional context with re-ranking.
    content = retrieve_additional_context("What is sigmoid loss function", "example", query_expansion=2)
    print(f"content: {content}")