- install Postgres SQL + pgvetor
- enable pgvector in Database

cd backend

python -m venv venv

source venv/bin/activate

install:
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

To run: fastapi dev main.py


cd frontend/my-app

npm install

To run:npm run dev
