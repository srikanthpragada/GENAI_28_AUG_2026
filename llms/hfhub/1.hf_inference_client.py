from huggingface_hub import InferenceClient
import keys 

client = InferenceClient(model="openai/gpt-oss-120b", token = keys.HUGGINGFACE_KEY)

messages = [
    {"role": "user", "content": "What is the capital of France?"}
]
response = client.chat_completion(messages)
#print(response)
print(response.choices[0].message.content)
