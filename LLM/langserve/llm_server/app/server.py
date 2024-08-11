from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from chain import chain, chain_retriever
from pydantic import BaseModel


app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/judgment/playground")


class JudgmentRequest(BaseModel):
    judgment: str
    
@app.post("/judgment/chain")
def chain_start(request: JudgmentRequest):
    try:
        legal_term, response, similarity, ease_improvement = chain_retriever(request.judgment)
        return {
            "legal_term": legal_term, 
            "response": response,
            "similarity": similarity,
            "ease_improvement": ease_improvement
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

add_routes(app, chain, path="/judgment")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
