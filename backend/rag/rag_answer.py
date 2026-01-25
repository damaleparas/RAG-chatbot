import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

def get_answer(query):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store_path = os.path.join("data", "faiss_index")
    
    if not os.path.exists(vector_store_path):
        return "Error: Knowledge base not found. Please run embed_store.py."

    vector_db = FAISS.load_local(
        vector_store_path, 
        embeddings, 
        allow_dangerous_deserialization=True 
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    template = """Use the context below to answer the question. 
    Context: {context}
    Question: {question}
    Answer:"""
    
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt}
    )

    return chain.invoke({"query": query})["result"]