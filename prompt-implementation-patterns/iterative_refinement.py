from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import re
import os

# Replace it with your OPENAI_API_KEY
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# === SET UP CHAIN ===
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant and an expert Python developer."),
        ("user", "Create a python code to resolve the problem:{question}. Reply only python code without explanation")
    ]
)

# Set up the refinement prompt template
refine_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant and an expert Python developer."),
        ("user", """ 
Enhance 3 things and regenerate the following code : {code} . Reply in json format like this:
------
{{"improvements": [[LIST ALL IMPROVEMENTS]],"code":[MAIN PYTHON CODE]}}

""")
    ]
)

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
# Create a simple chain
chain = prompt | llm | output_parser
refine_chain = refine_prompt | llm | output_parser

# === MAIN ===

# Convert response to json object
def convert_json(text):
    print(text.strip())
    try:
        json_data = json.loads(text)
        return json_data
    except Exception as e:
        print(f"Exception:{e}")
        response_str = re.search(r'```json(.*?)```', text, re.DOTALL)
        if response_str:
            response_str = response_str.group(1)
            response_json = json.loads(response_str)
            return response_json
    return None

# Call LLM with Iterative Refinement Pattern
def invoke_with_refinement(question,num_loop=3):
    code = chain.invoke({"question": question})
    print(f"DEBUG:Init:{code}")

    for i in range(num_loop):
        response = refine_chain.invoke({"code": code})
        print(f"DEBUG:{i}:Response:{response}")

        # Parsing 'code' from the response
        response_json = convert_json(response)

        improvements = response_json["improvements"]
        code = response_json["code"]

        print(f"DEBUG:{i}:Improvement:{improvements}")
        print(f"DEBUG:{i}:Code:{code}")


# Testing
invoke_with_refinement("Build a simple API using Flask")
