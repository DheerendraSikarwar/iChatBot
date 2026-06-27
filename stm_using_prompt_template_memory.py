"""
Issue:
	A standard LangChain chatbot does not automatically retain conversation history across multiple interactions, making it unable to 
	understand follow-up questions or maintain context. Manually managing message history for each session also increases code complexity 
	and becomes difficult to scale for multiple users.
Solution:
	This implementation uses RunnableWithMessageHistory together with MessagesPlaceholder and InMemoryChatMessageHistory to automatically 
	manage conversation history on a per-session basis. By associating each interaction with a unique session_id, the chatbot preserves 
	context across multiple turns, enabling more natural and context-aware conversations without manual history management.
"""

from dotenv import load_dotenv

# load the environment, first 
load_dotenv()

# required Modules:
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory


# prepare prompt:
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
	    MessagesPlaceholder(variable_name="history"),
	    ("human", "{input}"),
	]
)

# create Chain:
llm_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.0)
chain = prompt | llm_model

# create Session Store:
store = {}

def get_session_history(session_id):
	if session_id not in store:
		store[session_id] = InMemoryChatMessageHistory()
	return store[session_id]

# add memory:
chain_with_memory = RunnableWithMessageHistory(
	chain, 
	get_session_history=get_session_history,
	input_messages_key="input",
	history_messages_key="history",
)

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
        response = chain_with_memory.invoke(
                {"input" : query}, 
                config=config
            )
        
        print(f"\n{green}BOT : ", response.content[0]["text"])
