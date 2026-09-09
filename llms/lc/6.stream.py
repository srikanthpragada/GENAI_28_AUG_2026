# Set environment variable GOOGLE_API_KEY to Google key.

from langchain.chat_models import init_chat_model
from google.genai.types import AutomaticFunctionCallingConfig

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
# To supress warning from google SDK
model = model.bind(automatic_function_calling=AutomaticFunctionCallingConfig(disable=True))

#response = model.invoke("Who is James Gosling")
response = model.stream("Who is Van Rossum?")

for chunk in response:
    print(chunk.content, end = "\n--------------\n")
