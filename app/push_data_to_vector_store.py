import asyncio
import glob
import os

import pinecone
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index_name = "quizbot-index-test"

# Create index if it doesn't exist
if index_name not in [idx.name for idx in client.list_indexes()]:
    print("Initializing index")
    spec = ServerlessSpec(cloud="aws", region="us-east-1")
    client.create_index(name=index_name, dimension=1536, metric="cosine", spec=spec)
else:
    print("Index already initialized")
index = client.Index(index_name)

embeddings = OpenAIEmbeddings()
vector_store = PineconeVectorStore(index=index, embedding=embeddings)


async def read_data(filename: str):
    loader = TextLoader(filename)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
        ],
    )
    return text_splitter.atransform_documents(documents)


async def push_data_to_store(documents):
    # vector_store.from_documents(documents, embedding=embeddings, index=index_name)
    return vector_store.aadd_documents(documents, index_name=index_name)


async def add_data_to_store(filename):
    print(f"Adding file: {filename}")
    data = await read_data(filename)
    res = await push_data_to_store(data)
    print(f"File {filename} added in ids: {res}")
    return 1


def test_similarity_search(text):
    client = PineconeVectorStore(index=index, embedding=embeddings)
    return client.similarity_search(query=text, k=5)


async def data_loading():
    input_filepath = "../playground-llm/data/wikipedia/*.txt"
    for file in glob.glob(input_filepath):
        await add_data_to_store(file)


def get_number_of_records():
    return index.describe_index_stats()["total_vector_count"]


def push_data():
    print(f"Current number of records: {get_number_of_records()}")
    asyncio.run(data_loading())
    print("All tasks done!")
    print(f"New number of records: {get_number_of_records()}")
    print("Running test similarity...")
    res = test_similarity_search("What is a black hole?")
    for r in res:
        print(r.page_content)


if __name__ == "__main__":
    push_data()
