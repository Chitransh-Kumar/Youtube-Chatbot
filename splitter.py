from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

def split_text(text):
    """
    Takes video transcript and splits it into various chunks using Semantic Chunker.

    Returns LangChain Document objects.

    Args:
        text (str): YouTube video transcript.

    Returns:
        list[Documents]: Several chunks of the transcript splitted using Semantic Chunker.
    
    """


    embedding_model= OpenAIEmbeddings(
        model= 'text-embedding-3-small'
    )

    splitter= SemanticChunker(
        embedding_model,
        breakpoint_threshold_type= 'percentile'
    )

    docs= splitter.create_documents([text])

    return docs

