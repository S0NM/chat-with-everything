from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import streamlit as st
import os
from search_tools import SearchTools
from browser_tools import BrowserTools
from newsletter_tool import NewsletterTools

# ===Configura tion Section===

# OpenAI key
# Page setting
st.set_page_config(layout="wide")

# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
llm = ChatOpenAI(api_key=OPENAI_API_KEY)

# Avatar Photos for our bots
avatars = {"SearchAgent": "https://cdn-icons-png.flaticon.com/512/10885/10885144.png",
           "DownloadAgent": "https://cdn-icons-png.flaticon.com/512/4021/4021729.png",
           "NewsletterAgent": "https://cdn-icons-png.flaticon.com/512/5822/5822082.png"}

# Init Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What topic are you interested in?"}]


# Handle responses from CrewAI and show it on streamlit chat_message
class MyCustomHandler(BaseCallbackHandler):
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we are entering a chain.
        Turn it off if you feel noisy
        """
        # content = "DEBUG: Show you behind stories..:" + inputs['input']
        # st.session_state.messages.append({"role": "assistant", "content": content})
        # st.chat_message("assistant").write(content)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
        st.chat_message(self.agent_name, avatar=avatars[self.agent_name]).write(outputs['output'])


# ===Agent Section===

# Search Agent
search_agent = Agent(
    role='Search Agent',
    goal="Search for the latest news about the topic {topic}",
    backstory="You are an expert at searching for information on the internet and always keep up with the latest news.",
    memory = True,
    verbose = True,
    callbacks=[MyCustomHandler("SearchAgent")],
    tools = [SearchTools.search_internet]
)

# Download Agent
download_agent = Agent(
    role='Download Agent',
    goal="Download and summarize the main content from the list of URL",
    backstory="You are an expert at downloading and summarizing content from articles on the internet.",
    memory=True,
    verbose=True,
    callbacks=[MyCustomHandler("DownloadAgent")],
    tools = [BrowserTools.using_newspaper4k_scrape_and_summarize_website]
)

# Newsletter Agent
newsletter_agent = Agent(
    role='Newsletter Agent',
    goal='Create a newsletter aggregating news from a list of article summaries',
    backstory='You are an expert at aggregating news and creating engaging and easy-to-read newsletters.',
    callbacks=[MyCustomHandler("NewsletterAgent")],
    memory=True,
    verbose=True,
    tools = [NewsletterTools.create_newsletter]
)

# ===Task Section===
# search_task: search for topic via internet
search_task = Task(
    description=(
        "Search and return a list of URLs related to the topic: {topic}."
    ),
    expected_output='List of URLs.',
    agent=search_agent,
)

# download_task: download the content from each received URL
download_task = Task(
    description=(
        "Download content from each URL in the list and summarize the main content of each URL"
    ),
    expected_output='A summary of the main content of URL',
    agent=download_agent,
    context = [search_task]
)

# create_newsletter_task: aggregating the summary results from download_task
create_newsletter_task = Task(
    description=(
        "Create a newsletter from a list of article summaries and the URL list"
    ),
    expected_output='A newsletter aggregating articles including a title and brief description.',
    context = [search_task, download_task],
    agent=newsletter_agent,
)



# ===Main Section===
def main_page():
    st.title("💬 CrewAI: Creating a newsletter")

    agents = [search_agent, download_agent, newsletter_agent]
    tasks = [search_task, download_task, create_newsletter_task]

    for msg in st.session_state.messages:
        if msg["role"] in avatars.keys():
            st.chat_message(msg["role"], avatar=avatars[msg["role"]]).write(msg["content"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            manager_llm=llm,
            output_log_file="crewai.log",
        )

        final = crew.kickoff(inputs={"topic": prompt})


if __name__ == '__main__':
    main_page()
