# Program to show how LLM can call a tool based on the requirement
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage, AIMessage
import requests

@tool
def get_weather(latitude : float, longitude : float) -> dict:
    """function to return weather information based on latitude and longitude"""

    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    data = response.json()
    return data["current_weather"]


# 2.5 does not  privide geocoding
gemini = init_chat_model(
    "gemini-3.5-flash", model_provider="google_genai", temperature=0
)

# 3.5 does privide geocoding
gemini = init_chat_model(
    "gemini-3.5-flash", model_provider="google_genai", temperature=0
)


system_message = SystemMessage(
    "You are a helpful weather assistant.If needed, find out latitude and logitude then provide to tool. ")

user_message = HumanMessage("What is the weather in Perth")
#user_message = HumanMessage("What is the capital of Australia")

messages = [
    system_message,
    user_message
]

gemini_with_tools = gemini.bind_tools([get_weather])

while True:
    response = gemini_with_tools.invoke(messages)
    messages.append(response)

    if len(response.tool_calls) > 0:
        for tool_call in response.tool_calls:
            func_name = tool_call["name"]
            chosen_function = eval(func_name)

            # Call the tool and add result
            tool_result = chosen_function.invoke(tool_call)
            messages.append(tool_result)
    else:
        break 


for message in messages:
    message.pretty_print()
  
 
