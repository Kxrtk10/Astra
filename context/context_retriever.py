from context.context_vector_store import search_similar


def retrieve_context(query):

    results = search_similar(query)

    return results