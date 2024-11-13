from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()


model = ChatGroq(
    groq_api_key= os.getenv("GROQ_API_KEY"),
    model="llama-3.2-3b-preview",
    temperature=0.0,
    max_retries=2,
    streaming=True,
)


retrieval_chain = (
    model
    | StrOutputParser()
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def generate_chat_responses(message):
    async for chunk in retrieval_chain.astream(message):
        content = chunk.replace("\n", "<br>")
        yield f"data: {content}\n\n"


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.get("/chat_stream/{message}")
async def chat_stream(message: str):
    return StreamingResponse(generate_chat_responses(message=message), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)