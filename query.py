from imports import *

openai_mm_llm = OpenAIMultiModal(
    model="gpt-4o",  # Use the correct model identifier
    api_key=os.getenv("OPENAI_API_KEY"),
    max_new_tokens=300
)

def query(query_str, index):
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
    gemini = Gemini(model = "models/gemini-pro")
    gpt35 = OpenAI(temperature=0, model="gpt-3.5-turbo")

    # LLM (gpt-4)
    gpt4 = OpenAI(temperature=0, model="gpt-4-turbo")

    # gpt-4
    step_decompose_transform = StepDecomposeQueryTransform(llm=gpt4, verbose=True)

    # gpt-3
    step_decompose_transform_gpt3 = StepDecomposeQueryTransform(
        llm=gpt35, verbose=True
    )
    step_decompose_transform_gemini = StepDecomposeQueryTransform(
        llm=gemini, verbose=True
    )
    index_summary = "Used to answer questions about a research paper"

    # query_engine = index.as_query_engine(
    #     llm=llm, text_qa_template=qa_tmpl
    # )
    
    # response = query_engine.query(query_str)
    query_engine = index.as_query_engine(
    llm=openai_mm_llm
    )
    query_engine = MultiStepQueryEngine(
        query_engine=query_engine,
        query_transform=step_decompose_transform_gemini,
        index_summary=index_summary,
    )
    response = query_engine.query(
        query_str
    )

    return str(response)


# def query(query_str, index, llm):
#     qa_tmpl_str = (
#     "Context information is below.\n"
#     "---------------------\n"
#     "{context_str}\n"
#     "---------------------\n"
#     "Given the context information and not prior knowledge, "
#     "answer the query.\n"
#     "Query: {query_str}\n"
#     "Answer: "
#     )

#     qa_tmpl = PromptTemplate(qa_tmpl_str)

#     query_engine = index.as_query_engine(
#         llm=llm, text_qa_template=qa_tmpl
#     )


#     system = """You are an expert at converting user questions into database queries. \
#     You have access to a database of tutorial videos about a software library for building LLM-powered applications. \

#     Perform query expansion. If there are multiple common ways of phrasing a user question \
#     or common synonyms for key words in the question, make sure to return multiple versions \
#     of the query with the different phrasings.

#     If there are acronyms or words you are not familiar with, do not try to rephrase them.

#     Return at least 3 versions of the question."""
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", system),
#             ("human", "{question}"),
#         ]
#     )
#     llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
#     llm_with_tools = llm.bind_tools([ParaphrasedQuery])
#     query_analyzer = prompt | llm_with_tools | PydanticToolsParser(tools=[ParaphrasedQuery])

#     queries = query_analyzer.invoke(query)
#     final_response = ""
    
#     for i in queries:
#         response = query_engine.query(i.paraphrased_query)
#         final_response += response.response

#     return final_response
