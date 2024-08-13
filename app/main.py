import config
import gradio as gr
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec


def main():
    chat = ChatOpenAI(model="gpt-3.5-turbo-0125")
    client = Pinecone(api_key=config.PINECONE_API_KEY)
    index = client.Index(config.VECTORDB_INDEX_NAME)
    embeddings = OpenAIEmbeddings()

    history = ""
    query = input("Ask your question, mortal!\n")

    while query != "exit":
        history += "\n-" + query
        # res = PineconeVectorStore(index=index, embedding=embeddings).similarity_search(
        #    query=query, k=5
        # )

        messages = [
            SystemMessage(
                content="You're a magical djinn responding to questions. Your answers are also magical. Use arabic interjections."
            ),
            HumanMessage(content=query),
        ]

        for chunk in chat.stream(messages):
            print(chunk.content, end=" ", flush=True)

        query = input("Ask another question, mortal!\n")

    print("\nYour questions: ")
    print(history)
    print("\nQuitting chat....")


if __name__ == "__main__":
    main()

# def read_file(filename):
#    with open(filename, "r") as f:
#        contents = f.readlines()
#        return "\n".join(contents)
#
#
#
# def greet(file):
#    res = ""
#
#    # clear vector database
#
#    # read file
#
#    # transform file contents
#
#    # load file contents to vector database
#
#
#    # initialize LLM api
#
#    return res
#
#
# demo = gr.Interface(
#    fn=greet,
#    inputs=["file"],
#    outputs=["text"],
# )
#
# demo.launch()
