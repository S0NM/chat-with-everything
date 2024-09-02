from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from collections import Counter
import os

# Replace it with your OPENAI_API_KEY
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# === SET UP CHAIN ===
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a useful assistant"),
        ("user", """ Answer the question: {question}""")
    ]
)
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
# Create a simple chain
chain = prompt | llm | output_parser

# === MAIN ===

# Call LLM with Voting Pattern
def invoke_with_voting(question, num_votes=5):
    responses = []

    for i in range(num_votes):
        answer = chain.invoke({"question": question})
        responses.append(answer.strip())
        print(f"DEBUG:{i}:{answer}")

    response_counts = Counter(responses)

    # Determine the most common response
    final_answer = response_counts.most_common(1)[0]

    return final_answer

# Testing
response = invoke_with_voting("What is the best movie ever made? Your answer should contain only one movie title only ")
print(response)