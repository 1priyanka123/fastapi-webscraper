from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",  # Ensure this model is installed
    temperature=0
)

messages = [
    ("system", "You are a helpful assistant that translates English to French. Translate the user sentence."),
    ("human", "I love programming."),
]


ai_msg = llm.invoke(messages)
print(ai_msg.content)
