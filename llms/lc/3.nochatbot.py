# Set environment variable GOOGLE_API_KEY to Google key.

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

while True:
    prompt = input("Enter prompt [q to quit] :")
    if prompt.lower() == 'q':
        break 
    response = model.invoke( [SystemMessage(content="Give one line answers") ,
                              HumanMessage(content= prompt)])
    print(response.content)
    print('-' * 50)
    print(f'Total Tokens : {response.usage_metadata["total_tokens"]}')
