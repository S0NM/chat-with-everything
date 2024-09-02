from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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

# Validation Logic
def validate_answer(answer):
    if answer.strip() == '120':
        return True
    return False

# Call LLM with Error Handling
def invoke_with_retries(question, max_retries=3):
    for i in range(max_retries):
        answer = chain.invoke({"question": question})
        if validate_answer(answer):
            print(f"Attempt {i}:Result:OK: {answer}")
            return answer
        else:
            print(f"Attempt {i}:Result:NOT-OK: {answer}")
    print("Max retries reached")
    return "NO CORRECT ANSWER"

# Testing
response = invoke_with_retries("What is the factorial of 5? Return the final result without any explanation ")
print(response)