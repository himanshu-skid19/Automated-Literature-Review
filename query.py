from imports import *

def query(query_str, index, llm):
    qa_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
    )

    qa_tmpl = PromptTemplate(qa_tmpl_str)

    query_engine = index.as_query_engine(
        llm=llm, text_qa_template=qa_tmpl
    )
    
    response = query_engine.query(query_str)

    return str(response)
