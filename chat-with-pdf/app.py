import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

OPENAI_API_KEY=st.secrets["OPENAI_API_KEY"]

# Init langchain
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [("system","You are a very helpful assistant"),
     ("user","From my Pdf content:{content}. Please answer my question: {question}")]
)
chain = prompt | llm | output_parser
st.header("📗Chat with PDF")

uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
if uploaded_file is not None:
    temp_file = "./temp.pdf"
    with open(temp_file,"wb") as f:
        f.write(uploaded_file.getvalue())
        file_name = uploaded_file.name

    # Get pdf content
    loader = PyPDFLoader(temp_file)
    pages = loader.load()
    content = ""
    for page in pages:
        content = content + "\n --- \n" + page.page_content

    with st.expander("Check PDF full content!",expanded=False):
        st.write(content)

    question = st.text_input(label="What is your question?")
    if question != "":
        with st.spinner("I'm thinking...wait a minute!"):
            with st.container(border=True):
                response = chain.invoke({"content":content,"question":question})
                st.write(response)




