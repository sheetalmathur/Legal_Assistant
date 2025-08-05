from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_together import Together
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import streamlit as st
import time
st.set_page_config(page_title="LawGPT")
col1, col2, col3 = st.columns([1,4,1])
import streamlit as st

# Page config
st.set_page_config(
    page_title="LawGPT – Indian Penal Code Assistant",
    page_icon="⚖️",
    layout="centered"
)

# Custom CSS for clean, elegant look
st.markdown(
    """
    <style>
    /* Center the title */
    .block-container {
        padding-top: 2rem;
    }

    /* Style buttons */
    div.stButton > button:first-child {
        background-color: #e63946;
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 6px;
        font-weight: 600;
        transition: background-color 0.2s;
    }

    div.stButton > button:hover {
        background-color: #d62828;
    }

    /* Hide Streamlit footer and hamburger menu */
    #MainMenu, footer, .stDeployButton, #stDecoration {
        visibility: hidden;
    }

    /* Hide fullscreen button */
    button[title="View fullscreen"] {
        visibility: hidden;
    }

    /* Optional: refine status widget appearance */
    div[data-testid="stStatusWidget"] div button {
        display: none;
    }

    /* Add a soft shadow and rounded edges to chat input */
    .stChatInputContainer {
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Optional heading
st.markdown("## ⚖️ LawGPT – Your Indian Penal Code Assistant")
st.markdown("Ask legal questions related to the IPC and receive concise, reliable responses based on relevant context.")



def reset_conversation():
  st.session_state.messages = []
  st.session_state.memory.clear()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history",return_messages=True) 

embeddings = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1",model_kwargs={"trust_remote_code":True,"revision":"289f532e14dbbbd5a04753fa58739e9ba766f3c7"})
db = FAISS.load_local("ipc_vector_db", embeddings, allow_dangerous_deserialization=True)
db_retriever = db.as_retriever(search_type="similarity",search_kwargs={"k": 4})

prompt_template = """<s>[INST]This is a chat template and As a legal chat bot specializing in Indian Penal Code queries, your primary objective is to provide accurate and concise information based on the user's questions. Do not generate your own questions and answers. You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from posing additional questions. The aim is to deliver professional, precise, and contextually relevant information pertaining to the Indian Penal Code.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]
"""

prompt = PromptTemplate(template=prompt_template,
                        input_variables=['context', 'question', 'chat_history'])

# You can also use other LLMs options from https://python.langchain.com/docs/integrations/llms. Here I have used TogetherAI API
llm = ChatGroq(
    api_key="API_KEY",
    model="llama3-70b-8192",  # supported Groq model
    temperature=0.5,
    max_tokens=1024
)

qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=st.session_state.memory,
    retriever=db_retriever,
    combine_docs_chain_kwargs={'prompt': prompt}
)

for message in st.session_state.messages:
    with st.chat_message(message.get("role")):
        st.write(message.get("content"))

input_prompt = st.chat_input("Say something")

if input_prompt:
    with st.chat_message("user"):
        st.write(input_prompt)

    st.session_state.messages.append({"role":"user","content":input_prompt})

    with st.chat_message("assistant"):
        with st.status("Thinking 💡...",expanded=True):
            result = qa.invoke(input=input_prompt)

            message_placeholder = st.empty()

            full_response = "⚠️ **_Note: Information provided may be inaccurate._** \n\n\n"
        for chunk in result["answer"]:
            full_response+=chunk
            time.sleep(0.02)
            
            message_placeholder.markdown(full_response+" ▌")
        st.button('Reset All Chat 🗑️', on_click=reset_conversation)

    st.session_state.messages.append({"role":"assistant","content":result["answer"]})
