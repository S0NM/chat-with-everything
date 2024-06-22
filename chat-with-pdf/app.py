import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Page setting
st.set_page_config(layout="wide")

# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Init langchain
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a very helpful assistant"),
     ("user",
      "Based on my Pdf content:{content}. Please answer my question: {question}. Please use the language that I used in the question")]
)
chain = prompt | llm | output_parser

if "content" not in st.session_state:
    st.session_state.content = ""

def main_page():
    st.header("📗 Chat with PDF")

    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

    if uploaded_file is not None:
        temp_file = "./temp/temp.pdf"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Get pdf content
        loader = PyPDFLoader(temp_file)
        pages = loader.load()

        content = ""
        for page in pages:
            content = content + "\n\n" + page.page_content
        st.session_state.content = content

        if st.session_state.content != "":
            col1, col2 = st.columns([4, 6])
            with col1:
                with st.expander("Check PDF Content:", expanded=True):
                    st.write(st.session_state.content)

            with col2:
                question = st.text_input(label="Ask me anything:",
                                         value="Show me the best 5 prompts for Social Media Marketing ")
                if question != "":
                    with st.spinner("I'm thinking...wait a minute!"):
                        with st.container(border=True):
                            response = chain.invoke({"content": st.session_state.content, "question": question})
                            st.write("Answer:")
                            st.write(response)


if __name__ == '__main__':
    main_page()
