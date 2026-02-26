import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_DIR= 'faiss_indexes'

def build_vector_stores(docs, index_name):
    """
    Create or load a FAISS vector store for a document collection.

    If an index with the given name already exists on disk, it is loaded. Otherwise, a new FAISS index is built from the provided documents and saved locally for reuse.

    Args:
        docs (list[Document]): Documents to embed and index.
        index_name (str): Name of the FAISS index directory.

    Returns:
        FAISS: Loaded or newly created FAISS vector store.
    """


    embedding= OpenAIEmbeddings(
        model= 'text-embedding-3-small'
    )

    index_path= os.path.join(INDEX_DIR, index_name)

    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR)

    if os.path.exists(index_path):
        
        vector_store= FAISS.load_local(
            index_path, embedding, allow_dangerous_deserialization= True
        )

    else:

        vector_store= FAISS.from_documents(docs, embedding)

        vector_store.save_local(index_path)

    return vector_store
