import vertexai
from vertexai.preview.generative_models import GenerativeModel, SafetySetting, Tool


def generate(text: str, tools: list, generation_config: dict, safety_settings: list):
    vertexai.init(project="my-service-436118", location="asia-northeast3")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        tools=tools,
        system_instruction=["""Chatbot that answers users' questions, please set the output format to Markdown"""]
    )
    responses = model.generate_content(
        [f"""{text}"""],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    return responses.text
