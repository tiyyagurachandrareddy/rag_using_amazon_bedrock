import boto3
import streamlit as st
from langchain_community.llms import Bedrock
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
region_name = os.getenv("region_name")


prompt_template = """

Human: Use the following pieces of context to provide a
concise answer to the question at the end but use atleast summarize with
250 words with detailed explanations. If you don't know the answer,
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>

Question: {question}

Assistant:"""


# Bedrock client
bedrock_client = boto3.client(
    service_name = "bedrock-runtime",
     aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key,
    region_name= region_name
)

# Get embedding model from bedrock
bedrock_embedding = BedrockEmbeddings(
    model_id= "amazon.titan-embed-text-v1",
    client = bedrock_client
)

def get_documents():
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()
    text_spliter = RecursiveCharacterTextSplitter(
                                            chunk_size = 1000,
                                            chunk_overlap = 500)
    docs = text_spliter.split_documents(documents)
    return docs

def get_vector_store(docs):
    vectorstore_faiss = FAISS.from_documents(
        docs,
        bedrock_embedding
    )
    vectorstore_faiss.save_local("faiss_local")


def get_llm():
    llm = Bedrock(
        model_id = "mistral.mistral-7b-instruct-v0:2",
        client = bedrock_client
    )
    return llm


PROMPT = PromptTemplate(
    template= prompt_template,
    input_variables=["context", "question"]
)

def get_llm_response(llm, vectorstore_faiss, query):
    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = "stuff",
        retriever = vectorstore_faiss.as_retriever(
            search_type = "similarity",
            search_kwargs = {"k": 3}
        ),
        return_source_documents = True,
        chain_type_kwargs = {"prompt": PROMPT}
    )

    response = qa({"query": query})
    return response['result']


def main():
    st.set_page_config("RAG WITH BEDROCK")
    st.header("End to end RAG using Bedrock")

    user_question = st.text_input("Ask a question from the PDF file")

    with st.sidebar:
        st.title("Update & create vector store")

        if st.button("Store Vector"):
            with st.spinner("Processing..."):
                docs = get_documents()
                get_vector_store(docs)
                st.success("Done")

        if st.button("Send"):
            with st.spinner("Processing..."):
                faiss_index = FAISS.load_local("faiss_local", bedrock_embedding, allow_dangerous_deserialization= True)
                llm = get_llm()
                st.write(get_llm_response(llm,faiss_index, user_question))


if __name__ == "__main__":
    main()