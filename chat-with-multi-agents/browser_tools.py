from crewai import Agent, Task, Crew, Process
import re
from langchain.tools import tool
import newspaper

class BrowserTools():

    @tool("using_newspaper4k_scrape_and_summarize_website")
    def using_newspaper4k_scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content"""
        print(f"DEBUG:BrowserTools:{type(website)}:URL:{website}")
        try:
            link = ""
            if isinstance(website, dict):
                # Check and get link from webiste
                link = website.get("website")["title"]
            else:
                # website is string
                pattern = r'"website":\s*"([^"]+)"'
                match = re.search(pattern, website)

                if match:
                    link = match.group(1)
                else:
                    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
                    url_match = re.match(url_pattern, website)
                    if url_match:
                        link = website
                    else:
                        print("No link found")
            print(f"DEBUG:URL:{link}")

            article = newspaper.article(link)
            content = f"Title: {article.title}. Content: {article.text}"

            summary_agent = Agent(
                role='Summary Agent',
                goal='Summarize the following content in less than 150 words: {content}',
                backstory="You are an assistant of a famous CEO",
                allow_delegation=False,
            )

            summary_task = Task(
                description="Summarize the following content in less than 150 words: {content}",
                expected_output=" A summary",
                agent=summary_agent,
            )

            crew = Crew(
                agents=[summary_agent],
                tasks=[summary_task],
            )
            result = crew.kickoff(inputs={"content": content})
            return result
        except Exception as e:
            return f"BrowserTools:Exception:{e}"
