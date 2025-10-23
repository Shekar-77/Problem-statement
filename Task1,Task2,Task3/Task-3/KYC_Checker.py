import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import PIL.Image
import yfinance as yf
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from huggingface_hub import InferenceClient

# configure api key and initialise model
import os


# if "GOOGLE_API_KEY" not in os.environ:
#     os.environ["GOOGLE_API_KEY"] = userdata.get('api_key')
load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

aadhar_image = PIL.Image.open('Sample_Aadhar.png') 
vision_model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
aadhar_response = vision_model.generate_content(["What is the name,aadhar number,gender,dob?",aadhar_image])
pan_image=PIL.Image.open('sample-pan-card-front.jpg')
pan_response = vision_model.generate_content(["What is the name,dob?",pan_image])
print(aadhar_response.text)

#df = pd.read_csv('synthetic_aadhaar_data.csv')

# client = InferenceClient(
#     provider="fireworks-ai",
#     api_key=
# )
#response="069375628506,Kimberly Williams,2005-04-06,70291 Anthony Tunnel Suite 374 Taylorfurt, MH 38495,+1-468-900-8044,johnsonrobert@example.com"
messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful ai assistant that tells if the name and dob in two text is same.If same then declare the person legit else declare the person not legit"
        )
    },
    {
        "role": "user",
        "content": f"Here's the pan data:{pan_response.text} and the aadhar information{aadhar_response} tell if the name and dob matches"
    }
]
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",       # or "gemini-1.5-pro" for higher quality
    google_api_key="",
    temperature=0.6 #Temperature contrls the randomness of the output, lesser value gives more focused output
)
response = llm.invoke(messages)

# reply=client.chat.completions.create(
#     model="meta-llama/Llama-3.1-8B-Instruct",
#     messages=messages
#     )

print(response)



loader = TextLoader("synthetic_aadhaar_data.txt", encoding="utf-8") 
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
docs = text_splitter.split_documents(documents)

# -------------------------------------------------------------------
# 3️⃣ Initialize embeddings (Hugging Face)
# -------------------------------------------------------------------
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
embedding_dim = 384  # match this dimension to the model you use

# -------------------------------------------------------------------
# 4️⃣ Initialize Pinecone
# -------------------------------------------------------------------
load_dotenv()
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "kyc-checker"

if index_name not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=embedding_dim,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")  # Specifies the index has to be hosted on aws and in us-east-1 region
    )

index = pc.Index(index_name)

vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=embedding,
    index_name=index_name
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",       # or "gemini-1.5-pro" for higher quality
    google_api_key="",
    temperature=0.6 #Temperature contrls the randomness of the output, lesser value gives more focused output
)

template = """
You are a helpful ai assistant who can has given few information and you have to check if it is present in the dataset provided to you

Dataset:
{dataset}

Information:
{information}

Answer:
"""


prompt = PromptTemplate(
    template=template,
    input_variables=["dataset", "information"]
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

rag_chain = (
    {
        "dataset": retriever,
        "information": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser() #It takes output from llm and returns it as a string
)

query = f"Check is this is there in the dataset{aadhar_response.text}"
result = rag_chain.invoke(query)


print("\n🔹 Gemini RAG Answer:\n", result)
