from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag.rag_answer import get_answer


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message : str

@app.get("/")
def read_root():
    return {"status":"AI Agent Backend is running "}


@app.post("/chat")
async def chat_endpoint(request:ChatRequest):
    try:
        # Pass the user message to our RAG logic
        answer = get_answer(request.message)
        return {"reply":answer}
    except Exception as e:
        return {"reply":f"internal error {str(e)}"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host = "0.0.0.0", port = 8000)