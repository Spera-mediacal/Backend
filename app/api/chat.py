from fastapi.responses import JSONResponse
from app.model.chat import RequestModel
from app.chatbot.main import rag_chain
from app.core import app


@app.post("/get")
async def chat(request: RequestModel):
    input = request.msg
    print(input)
    response = rag_chain.invoke({"input": input})
    print("Response : ", response["answer"])
    return JSONResponse(content={"answer": response["answer"]})