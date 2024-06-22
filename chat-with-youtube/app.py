import streamlit as st
from langchain.document_loaders.generic import GenericLoader
from langchain_openai import ChatOpenAI
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

# Page setting
st.set_page_config(layout="wide")

# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Langchain Init
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a very helpful assistant"),
     ("user", "Based on my content:{content}. Please answer my question: {question}")]
)
chain = prompt | llm | output_parser
st.header("🎬 Chat with Youtube")

if "content" not in st.session_state:
    st.session_state.content = ""

def main_page():
    url = st.text_input("Please enter your YouTube URL",
                        value='https://www.youtube.com/watch?v=x5-MuZvr0l4&ab_channel=FantasyStorytimeTales')
    clicked = st.button("Load Youtube Video", type="primary")


    if clicked:
        # download YouTube audio only and save into test.mp4 file
        save_dir = "./temp/"
        with st.spinner("I'm thinking...wait a minute!"):
            loader = GenericLoader(YoutubeAudioLoader([url], save_dir), OpenAIWhisperParser())
            docs = loader.load()
            content = ""
            for doc in docs:
                content = content + doc.page_content + "\n"

            # Save content
            st.session_state.content = content

    if st.session_state.content != "":
        col1, col2 = st.columns([4, 6])
        with col1:
            with st.expander("Video Content:", expanded=True):
                st.write(st.session_state.content)

        with col2:
            question = st.text_input(label="Ask me anything:", value="Summary the content in 5 bullet points")
            if question != "":
                with st.spinner("I'm thinking...wait a minute!"):
                    with st.container(border=True):
                        response = chain.invoke({"content": st.session_state.content, "question": question})
                        st.write("Answer:")
                        st.write(response)


if __name__ == '__main__':
    main_page()
