import os

import dotenv

dotenv.load_dotenv()
VECTORDB_INDEX_NAME = "quizbot-index-test"
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
WCD_URL = os.environ.get("WCD_URL")
WCD_API_KEY = os.environ.get("WCD_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
