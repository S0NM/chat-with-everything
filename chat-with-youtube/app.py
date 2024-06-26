import streamlit as st
from langchain.document_loaders.generic import GenericLoader
from langchain_openai import ChatOpenAI
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Page setting
st.set_page_config(layout="wide")

# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Langchain Init
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
llm.model_name="gpt-4-turbo"
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a very helpful assistant"),
     ("user", "Based on my content:{content}. Please answer my question: {question}")]
)
chain = prompt | llm | output_parser
st.header("🎬 Chat with Youtube")

if "content" not in st.session_state:
    st.session_state.content = ""

# If YouTube video has transcript then return it
def get_trascript_content(url):
    content = ""
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        #Get the content only
        for transcript in transcript_list:
            content = content + transcript["text"]
    except Exception as e:
        print(f"GETTING TRANSCRIPT FAILED: {e}")
    return content

# If YouTube video has no transcript
def video_to_text(url):
    save_dir = "./temp/"

    loader = GenericLoader(YoutubeAudioLoader([url], save_dir), OpenAIWhisperParser())
    docs = loader.load()
    combined_content = [doc.page_content for doc in docs]
    content = " ".join(combined_content)

    # Save content
    st.session_state.content = content
    return content


def main_page():
    url = st.text_input("Please enter your YouTube URL",
                        value='https://www.youtube.com/watch?v=x5-MuZvr0l4&ab_channel=FantasyStorytimeTales')
    clicked = st.button("Load Youtube Video", type="primary")

    if clicked:
        with st.spinner("Loading YouTube Content..."):
            content = get_trascript_content(url)
            if content == "":
                # if video has no transcript -> using video-to-text method
                content = video_to_text(url)
            st.session_state.content = content

    if st.session_state.content != "":
        col1, col2 = st.columns([4, 6])
        with col1:
            with st.expander("Video Content:", expanded=True):
                st.write(st.session_state.content)

        with col2:
            question = st.text_input(label="Ask me anything:", value="Summary the content in comprehensive way to understand")
            if question != "":
                with st.spinner("I'm thinking...wait a minute!"):
                    with st.container(border=True):
                        response = chain.invoke({"content": st.session_state.content, "question": question})
                        st.write("Answer:")
                        st.write(response)


if __name__ == '__main__':
    main_page()
