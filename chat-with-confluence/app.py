import streamlit as st
from langchain_community.document_loaders import ConfluenceLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Page setting
st.set_page_config(layout="wide")

# Get your OPENAI API KEY: https://platform.openai.com/api-keys
# Get your CONFLUENCE API TOKEN: https://id.atlassian.com/manage-profile/security/api-tokens
# Use your login account as USERNAME: username@example.com
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
CONFLUENCE_API_TOKEN = st.secrets["CONFLUENCE_API_TOKEN"]
USERNAME = st.secrets["USER_NAME"]


# Init langchain
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a very helpful assistant"),
     ("user",
      "Based on my content:{content}. Please answer my question: {question}. Please use the language that I used in the question ")]
)
chain = prompt | llm | output_parser
st.header("	📚 Chat with Confluence")

if "content" not in st.session_state:
    st.session_state.content = ""

def main_page():
    # BASE_URL = https://yoursite.atlassian.com
    # Get SPACE_KEY in: https://yoursite.atlassian.com/wiki/spaces/<space_key>/pages/<page_id>
    BASE_URL = st.text_input("Confluence URL", value="https://appfire.atlassian.net/")
    SPACE_KEY = "CWP"

    clicked = st.button("Load Confluence Content",type="primary")
    if clicked:
        loader = ConfluenceLoader(
            url=BASE_URL,cloud=True,space_key=SPACE_KEY,
            username=USERNAME,api_key=CONFLUENCE_API_TOKEN,
            limit=1, max_pages=10
        )
        pages = loader.load()
        content = ""
        for page in pages:
            content = content + "\n \n" + page.page_content
            # Save content
        st.session_state.content = content

    if st.session_state.content != "":
        col1, col2 = st.columns([4, 6])
        with col1:
            with st.expander("Confluence Space Content:", expanded=False):
                st.write(st.session_state.content)

        with col2:
            question = st.text_input(label="Ask me anything:", value="Summary the content")
            if question != "":
                with st.spinner("I'm thinking...wait a minute!"):
                    with st.container(border=True):
                        response = chain.invoke({"content": st.session_state.content, "question": question})
                        st.write("Answer:")
                        st.write(response)

if __name__ == '__main__':
    main_page()
