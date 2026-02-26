def classify_query(query):
    """
    Classify query as Normal query or Summary query.

    Args:
        query (str): Question given by the user.

    Returns:
        Literal:
        ['summary', 'normal']:
        Classify query type as Summary query or Normal query

    """


    query= query.lower()

    if any(word in query for word in ['summarize', 'summary', 'overview']):
        return "summary"
    
    return "normal"