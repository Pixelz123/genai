from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# 1. Load the environment variables to authenticate with Google
load_dotenv(r"d:\genai\.env")

# 2. Load your sample document using UTF-8 encoding
loader = TextLoader(r"d:\genai\sample.txt", encoding="utf-8")
documents = loader.load()

# 3. Split the text into smaller, meaningful chunks for better retrieval
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = text_splitter.split_documents(documents)

# 4. Initialize Google's Generative AI embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# 5. Create the Chroma vector store and persist it locally in the "chroma_db" folder
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=r"d:\genai\chroma_db"
)

# 6. Test the vector store with a similarity search query
query = "What will happen next Thursday?"
results = vector_store.similarity_search(query, k=1)

print(f"Top result:\n{results[0].page_content}")