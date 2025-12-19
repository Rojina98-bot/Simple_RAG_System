- install Postgres SQL + pgvetor
- enable pgvector in Database

**cd backend**

- python -m venv venv

- source venv/bin/activate

- install:
    fastapi
    uvicorn
    python-multipart
    langchain-text-splitters
    sentence-transformers
    psycopg2-binary
    pgvector
    python-dotenv
    numpy
    pandas
    google-generativeai

- To run: fastapi dev main.py


<br><br>
**cd frontend/my-app**

- npm install

- To run: npm run dev


**ARCHITECTURE**


- **Upload File (.txt)**  
  - User uploads a document.

- **Split into Chunks**  
  - The document is split into smaller text chunks for efficient retrieval.

- **Generate Embeddings**  
  - Each chunk is converted into a vector using a sentence embedding model.

- **Store in Postgres (pgvector)**  
  - Chunks and their embeddings are saved in PostgreSQL using the `pgvector` extension.

- **Query & Retrieve**  
  - When the user asks a question, it is embedded into a vector, and the top-k most similar chunks are fetched from the database.

- **Answer Generation (RAG)**  
  - The retrieved chunks are sent as context to the LLM (e.g., Gemini 2.5) to generate a response.


