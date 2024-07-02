📚 Chat with Confluence

### **Level**: Beginner 🎖️ 

### 1. Our Goal 🎯

Confluence is a tool used as a wiki by many companies. If we consider Confluence as a knowledge repository, providing a tool to access this repository is very important. In this application, I will show you:

* How to access and load content from this knowledge repository 
* A Q&A chatbot to interact with this knowledge repository

**Tech Stack**

- Streamlit
- Langchain ([Working with Confluence Lodaer](https://python.langchain.com/v0.2/docs/integrations/document_loaders/confluence/))

Take a look at the following demo to understand what we will achieve :)):

![chat-with-youtube](https://github.com/S0NM/chat-with-everything/blob/0df9d749d1628af62764de417f616c33bc5a42a6/gif/chat-with-confluence.gif)

### 2. How to get started?  🐌

1. Clone my GitHub repository

```bash
git clone https://github.com/S0NM/chat-with-everything.git
```
2. Install the required dependencies

```bash
pip install -r requirements.txt
```
3. Get your OpenAI API Key

- Sign up [OpenAI account](https://platform.openai.com/) (or the LLM provider of your choice) and get your API key.
```python
# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
```
4. Run the Streamlit App
```bash
streamlit run app.py
```


### 💰 3. Digging Deeper

...Will be updated later,,,,
