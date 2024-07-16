from pandasai.helpers.openai_info import get_openai_callback
import matplotlib
from pandasai.responses.response_parser import ResponseParser
from pandasai.connectors import PandasConnector
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import tiktoken

# Set backend before import pyplot (Do not show a new windows after plotting)
matplotlib.use("Agg", force=True)

# Page setting
st.set_page_config(layout="wide")

# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Init pandasai
llm = OpenAI()

if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False
if 'prompt_called' not in st.session_state:
    st.session_state['prompt_called'] = False


# Handle response messages according to type: dataframe, plot or text
class MyStResponseParser(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)
    def parse(self, result):
        if result['type'] == "dataframe":
            st.dataframe(result['value'])
        elif result['type'] == 'plot':
            st.image(result["value"])
        else:
            st.write(result['value'])
        return

@st.cache_data
def load_data():
    dataset_file = "./dataset/title.basics.tsv"
    df = pd.read_csv(dataset_file, sep="\t", low_memory=False)
    return df

# Tip: Adding Description for data fields to make GPT understand more easily, using in case you don't want to use GPT's automatic understanding mechanism
field_descriptions = {
    "tconst": "An alphanumeric unique identifier of the title",
    "titleType": " the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)",
    "primaryTitle": "the more popular title / the title used by the filmmakers on promotional materials at the point of release",
    "originalTitle": "original title, in the original language",
    "isAdult":"0: non-adult title; 1: adult title",
    "startYear": "represents the release year of a title. In the case of TV Series, it is the series start year. YYYY format",
    "endYear" : "TV Series end year. \\N means null value",
    "runtimeMinutes": "primary runtime of the title, in minutes. \\N means null value",
    "genres":"includes up to three genres associated with the title"
}

def main_page():
    st.header("📗 Chat with 10M Movies Datasets")

    clicked = st.button("Load Dataset into Memory", type="primary")

    if clicked:
        st.session_state['data_loaded'] = True

    if st.session_state['data_loaded']:
        df = load_data()
        with st.expander("Check Data Reading Log", expanded=False):
            st.write(df.head(3))
            st.markdown(df.info())
        st.write("### Ask me anything about your Data:")
        prompt = st.text_input("Enter your prompt", value="Thống kê số lượng giao dịch theo ngày")
        connector = PandasConnector(
            {'original_df': df}, field_descriptions=field_descriptions)
        agent = SmartDataframe(connector,
                               config={
                                   "llm": llm,
                                   "conversational": False,
                                   "response_parser": MyStResponseParser,
                               })
        if st.button("Send Message"):
            st.session_state['prompt_called'] = True

        if st.session_state['prompt_called']:
            if prompt:
                st.write(" 👻 Response:")
                with st.spinner("Generating response..."):
                    with get_openai_callback() as call_back_info:
                        chat_reponse = agent.chat(prompt)
                        st.write("📚 What happened behind:")
                        st.code(agent.last_code_executed)
                        st.write(call_back_info)
            else:
                st.warning("Please enter a prompt")

def calculate_cost():
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    cost_per_1M_tokens = 0.5 # 0.5$ / 1M Tokens

    # Load data in df
    dataset_file = "./dataset/title.basics.tsv"
    df = pd.read_csv(dataset_file, sep="\t", low_memory=False)

    # For each row, combine all fields into a tring
    data_as_strings = df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1).tolist()

    # Count the number of tokens for each row
    token_counts = [len(encoding.encode(text)) for text in data_as_strings]

    # Print the results
    total_tokens = sum(token_counts)
    # for i, count in enumerate(token_counts):
    #     print(f"Row {i} has {count} tokens.")
    print('Total tokens:', total_tokens)
    print('Cost:', total_tokens * cost_per_1M_tokens / 1000000)

if __name__ == '__main__':
    main_page()


