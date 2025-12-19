from fastapi import FastAPI, Form
from fastapi import FastAPI, File, UploadFile
from langchain_text_splitters import TokenTextSplitter
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import psycopg2
from pgvector.psycopg2 import register_vector
from psycopg2.extras import execute_values
import numpy as np
import pandas as pd
import google.genai as genai


load_dotenv()
DATABASE_URL=os.environ.get("DATABASE_URL")
client=genai.Client(api_key=os.environ['GOOGLE_API_KEY']) 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_methods=["*"],                      
    allow_headers=["*"],
)
def get_conn():
    conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"))
    register_vector(conn)
    return conn, conn.cursor()
 
def init_db():
    conn,cur=get_conn()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        content text,
        tokens integer,
        embedding vector(768)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()


init_db()
    


def CreateChunks(content_text):
    splitter = TokenTextSplitter(chunk_size=50, chunk_overlap=10)  # adjust size
    chunks = splitter.split_text(content_text)
    return chunks


def CreateEmbedding(chunks):
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    embeddings = model.encode(chunks)
    return embeddings

def similar_chunks(query_embedding,limit=3):
    conn,cur=get_conn()
    cur.execute("SELECT content FROM embeddings ORDER BY embedding <=> %s LIMIT 3", (query_embedding,))
    sim_text=cur.fetchall()
    cur.close()
    conn.close()
    return [text[0] for text in sim_text]

def build_prompt(context_chunks, user_question):
    context="\n\n".join(context_chunks)
    prompt=f"""You are a helpful assistant.
    Answer the question using ONLY the context below.
    If the answer is not in the context, say "I don't know".

    Context:
    {context}

    Question:
    {user_question}
    """
    return prompt


@app.post("/uploadFile")
async def upload_file(file:UploadFile=File(...)):
    content=await file.read()
    content_text = content.decode("utf-8")  
    chunks=CreateChunks(content_text)
    embeddings=CreateEmbedding(chunks)
    data_list = [(chunks[i], len(chunks[i].split()), embeddings[i]) for i in range(len(chunks))]
    conn, cur = get_conn()
    execute_values(cur, "INSERT INTO embeddings (content, tokens, embedding) VALUES %s", data_list)
    conn.commit()
    cur.close()
    conn.close()

    return{
        "filename": file.filename,
        "size": len(content),
        "chunks_count": len(chunks),
        "first_chunk": chunks[0] if chunks else ""
    }

@app.post("/chat")
async def chat(text:str=Form(...)):
    embeddings=CreateEmbedding([text])[0]
    sim_texts=similar_chunks(embeddings)
    prompt=build_prompt(sim_texts,text)
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )
    return{
        "question":text,
        "answer":response.text,
        "context_used":sim_texts
    }
    




