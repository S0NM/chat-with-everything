from langchain.tools import tool

class NewsletterTools():

    @tool("create_newsletter")
    def create_newsletter(summaries):
        """
        Useful when creating a newsletter aggregating all the summary contents
        """
        print(f"DEBUG:NewsletterTools:{summaries}")
        try:
            newsletter = ""
            for summary in summaries:
                # Assume each summary includes 'title' and 'content'
                title = summary['title']
                content = summary['description'][:150]  # Summarize to less than 150 words
                newsletter += f"Title: {title}\nContent: {content}\n\n"
            return newsletter
        except Exception as e:
            return f"NewsletterTools:Exception:{e}"

