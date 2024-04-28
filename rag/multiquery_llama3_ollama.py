
#### INDEXING ####

EMBEDDING_MODEL = "all-minilm"
LLM_MODEL = "llama3"

# Load blog post
import bs4
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
blog_docs = loader.load()

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300, 
    chunk_overlap=50)

# Make splits
splits = text_splitter.split_documents(blog_docs)

# Index
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
vectorstore = Chroma.from_documents(documents=splits, 
                                    embedding=OllamaEmbeddings(model=EMBEDDING_MODEL))

retriever = vectorstore.as_retriever()

### PROMPT
from langchain_community.llms import Ollama
llm = Ollama(model=LLM_MODEL, temperature=0)
from langchain.prompts import ChatPromptTemplate

# Multi Query: Different Perspectives
template = """You are an AI language model assistant. Your task is to generate five
different versions of the given user question to retrieve relevant documents from a vector 
database. Provide these alternative questions separated by newlines.
Your response should consist only of the versions of the questions, with no preambles or additional information.
Original question: {question}"""
prompt_perspectives = ChatPromptTemplate.from_template(template)

from langchain_core.output_parsers import StrOutputParser

def strip_blank_queries(queries):
    return [q for q in queries if q != ""]

generate_queries = (
    prompt_perspectives 
    | llm 
    | StrOutputParser() 
    | (lambda x: x.split("\n"))
    | strip_blank_queries
)

from langchain.load import dumps, loads

def get_unique_union(documents: list[list]):
    """ Unique union of retrieved docs """
    # Flatten list of lists, and convert each Document to string
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    # Get unique documents
    unique_docs = list(set(flattened_docs))
    # Return
    return [loads(doc) for doc in unique_docs]

# Retrieve
question = "List methods of prompt engineering."
retrieval_chain = generate_queries | retriever.map() | get_unique_union


# MULTI QUERY

from langchain_core.runnables import RunnablePassthrough

# RAG
template = """Answer the following question based on the context:

{context}

Question: {question}
Provide only the answer to the question. Do not mention the provided context in your response.
"""

prompt = ChatPromptTemplate.from_template(template)

final_rag_chain = (
    {"context": retrieval_chain, 
     "question": RunnablePassthrough() } 
    | prompt
    | llm
    | StrOutputParser()
)

print("=========")
print(final_rag_chain.invoke({"question":question}))
print("=========")

