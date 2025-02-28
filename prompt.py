from langchain_ollama import OllamaLLM

# Define a strict business-related prompt
print("\nMediocre Business Analyst Chatbot")
print("=================================")
print("Ask any business question, and receive a mediocre analysis.")
print("Type 'exit' to quit the program.")

llm = OllamaLLM(model="llama3.2:latest")  # Set up the model

while True:
    query = input("\nYour question: ")

    if query.lower() in ['exit', 'quit', 'bye']:
        print("\nMeeting adjourned. Let's circle back next quarter! 🚀")
        break

    # Generate a mediocre response
    prompt_text = f"""
    You are a Mediocre Business Analyst model. You provide simple, jargon-heavy, but ultimately vague responses.

    Rules:
    - Stick strictly to business analysis topics.
    - If the question is unrelated to business analysis, reply: "I focus only on business analysis topics."
    - Keep responses professional but avoid deep insights.

    QUERY: {query}
    RESPONSE:
    """

    try:
        response = llm.invoke(prompt_text)
        print(f"\n==== MEDIOCRE BUSINESS ANALYSIS ====\n{response}\n====================================")
    except Exception as e:
        print(f"Error generating business analysis: {str(e)}")
