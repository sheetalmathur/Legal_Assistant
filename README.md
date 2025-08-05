
LawGPT - RAG based Generative AI Attorney Chatbot
==================================================
Know Your Rights! Better Citizen, Better Nation!

About the Project
-----------------
LawGPT is a RAG-based generative AI attorney chatbot that is trained using Indian Penal Code data. 
This project was developed using Streamlit, LangChain, and Groq API for the LLM instead of TogetherAI. 
Ask any questions to the chatbot and it will give you context-aware, IPC-based responses.
Not sure about your rights? This is for you!

Getting Started
---------------

##1. Clone the repository:
   git clone https://github.com/sheetalmathur/Legal_Assistant.git

##2. Install necessary packages:
   pip install -r requirements.txt

##3. Embeddings Setup (Two Options):

   Option A: Run the `ingest.py` file (preferably on Kaggle or Colab for faster embedding generation),
   then download the `ipc_vector_db` from the output folder and save it locally.

   Option B: Skip `ingest.py` and directly download the vector database from Hugging Face Space:
   https://huggingface.co/spaces/Sheetal12345/ipc_vector_space

##4. Set up Groq API Key (instead of TogetherAI):
   Sign up at https://console.groq.com and get your API key.

   Set it in your code:
   os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"

   If deploying on Streamlit or Hugging Face, add it to the secrets with key as GROQ_API_KEY.

   For model support, refer: https://python.langchain.com/docs/integrations/llms/groq

5. Run the Streamlit app:
   streamlit run app.py

Contact
-------
If you have any questions or feedback, please raise an issue at:
https://github.com/sheetalmathur/Legal_Assistant/issues

Note: This tool is for educational and informational purposes only. It is not a substitute for professional legal advice.
