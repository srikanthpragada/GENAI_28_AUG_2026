# Set environment variable GOOGLE_API_KEY to Google key.

from langchain.chat_models import init_chat_model
from google.genai.types import AutomaticFunctionCallingConfig

model = init_chat_model("gemini-3.1-flash-lite", model_provider="google_genai")

# To supress warning from google SDK
model = model.bind(automatic_function_calling=AutomaticFunctionCallingConfig(disable=True))

response = model.invoke("What is the capital of Spain")
print(response.content)