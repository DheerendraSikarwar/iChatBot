## Project Name
iChatBot - using chat history to mentained short-term memory 

## 1. How to create virtual environment
### Initialize working workspace using uv package
% uv init  

### 1.1 Create virtual environment
% uv venv <python_specific_version_optional>

### 1.2 Activate virtual environment 
% source .venv/Scripts/activate     (Mac/Linux)
% . .venv/Scripts/activate          (Window)

## 2. Create ‘requirements.txt’ file to add all the packages which need to be install in this virtual environment  for this project.
langchain
langgraph
Langchain_community
langchain-openai
langchain-groq
langchain-google-genai
python-dotenv
<add more packages as per project requirement>

## Run requirements.txt to install required packages
uv add -r requirements.txt
