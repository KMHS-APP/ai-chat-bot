from fastapi import *
from fastapi.responses import *
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from src import func
from vertexai.preview.generative_models import grounding
from vertexai.preview.generative_models import SafetySetting, Tool


app = FastAPI(
    title="Nergis API",
    summary="Made By Dev_Nergis",
    description="Nergis API",
    version="7.3.6",
    default_response_class=ORJSONResponse)


# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return FileResponse("static/index.html")


@app.get("/status")
async def status():
    return ORJSONResponse({"status": "ok"})


@app.get("/ip")
async def get_ip(request: Request):
    client_host = request.headers.get("X-Real-IP")
    if not client_host:
        client_host = request.client.host
    return PlainTextResponse(client_host)

# ai

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

tools = [
    Tool.from_google_search_retrieval(
        google_search_retrieval=grounding.GoogleSearchRetrieval()
    ),
]

class ChatText(BaseModel):
    message: str  

@app.post("/ai")
async def ai(body: ChatText):
    return ORJSONResponse({"response": func.generate(body.message, tools, generation_config, safety_settings)})
