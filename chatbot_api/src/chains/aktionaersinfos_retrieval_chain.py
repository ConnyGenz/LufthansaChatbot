import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

# Model for text QA as specified in the .env file
LUFTHANSA_QA_MODEL = os.getenv("LUFTHANSA_QA_MODEL")

# Create vectorstore from data in local directory
aktionaersinfos_vector_db = Chroma(persist_directory="chroma_aktionaersinfos/",
                                   embedding_function=OpenAIEmbeddings())

# Create retriever from vectorstore
aktionaersinfo_retriever = aktionaersinfos_vector_db.as_retriever(k=10)

## Create the retrieval chain for text QA

# prompt elements for the chain:

text_qa_template = """Your are a helpful chatbot who works for the German airline Lufthansa. 
You use shareholder information documents to answer questions about Lufthansa. Use
the following context to answer questions. Be as detailed as possible, but
don't make up any information that's not from the context. If you don't know
an answer, say you don't know. Write your answers in German.
{context}
"""

text_qa_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"], template=text_qa_template)
)

text_qa_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [text_qa_system_prompt, text_qa_human_prompt]

text_qa_prompt = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)

# the chain itself:

text_qa_vector_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model=LUFTHANSA_QA_MODEL, temperature=0),
    chain_type="stuff", # tells the chain to pass all of the retrieved chunks to the prompt
    retriever=aktionaersinfo_retriever,
)

# Give the prompt to the chain
text_qa_vector_chain.combine_documents_chain.llm_chain.prompt = text_qa_prompt
