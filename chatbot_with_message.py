"""
Issue:
    When developers build their first chatbot, they often invoke the LLM with only the current user query. As a result, the model has no memory of previous interactions and can't answer follow-up questions that depend on earlier context.
    
Solution:
    This program demonstrates how to build a context-aware chatbot using LangChain and the Gemini LLM by maintaining conversation history with SystemMessage, HumanMessage, and AIMessage. 
    
    It covers LLM initialization, environment configuration, chat history management, message handling, and interactive CLI development, providing a strong foundation for advanced AI applications such as RAG, agents, and conversational assistants.
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# load the environment, first 
load_dotenv()

# create LLM
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.5)

# chat history, which contains user conversation chat history along with SystemMessage
chat_msgs = [       
    SystemMessage(content="You are a helpful AI Assistant")
]


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
        
        # appending human message to chat history before passing to LLM
        chat_msgs.append(HumanMessage(content = query))
        
        # passing chat history = System Message + user query as user query / prompt
        response = model.invoke(chat_msgs) 
        print(f"\n{green}BOT : ", response.content[0]["text"])
    
        # appending the model response to the chat history 
        chat_msgs.append(AIMessage(content=response.content))

    # print chat history of current thread
    print(chat_msgs)
    