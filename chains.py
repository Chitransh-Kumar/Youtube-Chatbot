from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def format_text(retrieved_docs):
    """
    Convert retrieved documents into a single context string.

    Joins the page content of retrieved documents using double newlines to produce a readable context block for prompting.

    Args:
        retrieved_docs (list[Document]): Documents returned by a retriever.

    Returns:
        str: Combined text content of all retrieved documents.
    """
    context_text= "\n\n".join(doc.page_content for doc in retrieved_docs)

    return context_text

def build_chain(retriever):
    """
    Build a retrieval-augmented question-answering chain.

    The chain retrieves relevant documents, formats them into a context string, injects the context into a prompt, and generates an answer using a chat model.

    Args:
        retriever: A LangChain retriever used to fetch relevant documents.

    Returns:
        Runnable: A composed RAG chain that accepts a question string as input and returns a generated response.
    """
    prompt= PromptTemplate(
        template= """
            You are a helpful assistant. Answer only from the provided context.
            If insufficient context, say don't know.

            {context}
            Question: {question}
        """,
        input_variables= ['context', 'question']
    )

    parallel_chain= RunnableParallel({
        'context': retriever | RunnableLambda(format_text),
        'question': RunnablePassthrough()
    })

    llm= ChatOpenAI(
        model= 'gpt-4o-mini',
        temperature= 0.5
    )

    parser= StrOutputParser()

    main_chain= parallel_chain | prompt | llm | parser

    return main_chain

def build_summary_chain():
    """
    Build a text summarization chain.

    Creates a chain that prompts a language model to summarize input text in fewer than 100 words.

    Returns:
        Runnable: A chain that accepts a text string and
        returns a concise summary.
    """
    prompt= PromptTemplate(
        template= """
            Summarize the following text provided in less than 100 words
            {text}
        """,
        input_variables= ['text']
    )

    llm= ChatOpenAI(
        model= 'gpt-4o-mini',
        temperature= 1
    )

    parser= StrOutputParser()

    summary_chain= prompt | llm | parser

    return summary_chain