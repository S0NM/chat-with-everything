import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from gnews import GNews
import newspaper
from newspaper import ArticleException

# Page setting
st.set_page_config(layout="wide")

# Get your OPENAI API KEY: https://platform.openai.com/api-keys
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Init langchain
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a very helpful assistant"),
     ("user",
      "Based on my content:{content}. Please answer my question: {question}. Please use the language that I used in the question ")]
)
chain = prompt | llm | output_parser
st.header("	📰 Chat with Google News")

if "content" not in st.session_state:
    st.session_state.content = ""

@st.cache_data
def get_news_detail(gnews_results):
    news_with_detail = []
    for site in gnews_results:
        url = site["url"]
        try:
            article = newspaper.article(url)
            print("DEBUG:SITE:" + article.title)
            news_with_detail.append({"title": article.title, "url": article.url, "content": article.text})
        except ArticleException as e:
            print(f"DEBUG:SITE:EXCEPTION:{e}")

    return news_with_detail


def main_page():
    google_news = GNews()
    google_news.period = "2d"
    google_news.max_results = 3

    topic = st.text_input("Please enter your topic", "claude 3.5")
    clicked = st.button("Load 3 results", type="primary")
    if clicked:
        with st.spinner("Loading ..."):
            results = google_news.get_news(topic)
            articles = get_news_detail(results)

            content = ""
            for index, article in enumerate(articles):
                content = content + "\n\n" + "-- Article " + str(index + 1) + "-- \n\n Title:" + article[
                    "title"] + "\n\n Content:" + article["content"]
            st.session_state.content = content

    if st.session_state.content != "":
        col1, col2 = st.columns([4, 6])
        with col1:
            with st.expander("Google News Content:", expanded=False):
                st.write(st.session_state.content)

        with col2:
            question = st.text_input(label="Ask me anything:", value="Summarize the content of each article in one bullet point")
            if question != "":
                with st.spinner("I'm thinking...wait a minute!"):
                    with st.container(border=True):
                        response = chain.invoke({"content": st.session_state.content, "question": question})
                        st.write("Answer:")
                        st.write(response)


if __name__ == '__main__':
    main_page()
