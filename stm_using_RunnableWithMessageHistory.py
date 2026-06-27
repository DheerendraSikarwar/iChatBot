"""
Issue:
 Passing the complete conversation history manually to the LLM for every request increases code complexity and makes session management difficult, especially when supporting multiple users. Managing chat history yourself can quickly become error-prone and harder to scale.
    
Solution:
    This implementation uses RunnableWithMessageHistory with InMemoryChatMessageHistory to automatically store and retrieve conversation history based on a unique session_id. It simplifies chatbot development by enabling session-aware, context-rich conversations without requiring manual message management.
"""

from dotenv import load_dotenv

# load the environment, first 
load_dotenv()

# Create Message History Store:
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}

def get_session_history(session_id : str):
	if session_id not in store:
		store[session_id] = InMemoryChatMessageHistory()
	return store[session_id]

# Create LLM:
from langchain_google_genai import ChatGoogleGenerativeAI

llm_model = ChatGoogleGenerativeAI(
    model = "gemini-3.1-flash-lite",
	temperature = 0.0
)

# Wrap LLM with Message History:
from langchain_core.runnables.history import RunnableWithMessageHistory

chain = RunnableWithMessageHistory(llm_model, get_session_history=get_session_history)

if __name__ == "__main__":
    yellow = "\033[0;33m"
    green = "\033[0;32m"
    print("\n=============== CHATBOT APP ===============\n")

    while True:
        query = input(f"\n{yellow}You (or 'exit') : ")
        if query.lower() == "exit":
            break
        if not query.strip():
            continue
        
        config = {"configurable": {"session_id" : "user_1"}}
        
        # passing
        response = chain.invoke(query, config=config) 
        print(f"\n{green}BOT : ", response.content[0]["text"])