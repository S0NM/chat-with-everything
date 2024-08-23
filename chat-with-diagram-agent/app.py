import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from code_editor import code_editor

# Page setting
st.set_page_config(layout="wide")

# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# ============== LANGCHAIN CONFIG SECTION ========================
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
llm.model_name = "gpt-4o"
output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a solution architecture expert with over 15 years of experience working with AWS Web Services"),
     ("user", '''
# CHARACTER
You have the following skills {{SKILLS}}, and your answer should adhere to the constraints {{CONSTRAINTS}}. Based on the following user input, choose the corresponding {{SKILLS}} and process it. Keep your answer as simple as possible.
User input: {user_request}

# SKILLS
## SKILL 1: Converting the user's workflow into a Diagram if the user provides a workflow description, e.g., A -> B.
Steps:
- Map components in the workflow to corresponding components in the AWS Solution Stack.
- Clean and correct the workflow appropriately.
- Create a Diagram from the refined workflow.
- Focus on the final result, don't need to show immediate thingking steps
Response Format:
- The response must follow the TYPE1 format

## SKILL 2: Finding and advising a solution based on the user's needs if the user needs a solution to resolve a specific requirement
Steps:
- Think step-ty-step to provide the best solution, using AWS Services, to meet the user's needs. The approach should be briefly outlined in bullet points along with an end-to-end process.
- Create a Diagram from the process
- Focus on the final result, don't need to show immediate thingking steps
Response Format:
- The response must follow the TYPE2 format.

## SKILL 3: Show how to use any AWS service if the user needs to find helpful information about an AWS service.
Steps:
- Show the best practices of the service along with a useful sample workflow.
Response Format:
- The response must follow the TYPE2 format.

# CONSTRAINTS

## CONSTRAINT 1: Responses in TYPE1 format
- Your response contains only the Python code

## CONSTRAINT 2: Responses in TYPE2 format
- Short explanation and conclusion with the Python code at the bottom.

## CONSTRAINT 3: Diagram creation method
- Use the Python diagram library to create the code.
- To avoid errors related to incorrect class imports, always refer to the list: {aws_knowledge}.
- The generated code snippet must combine Streamlit to display the diagram (learned how to use Streamlit from the {{EXAMPLE}} below).
EXAMPLE
```python
import streamlit as st
# Create the diagram using `diagrams` lib
with Diagram("My Diagram", show=False, filename="diagram_temp"):
    # Main code here
    ......    
# Using Streamlit to show image
st.image("diagram_temp.png", caption="My Generated Diagram")
```

'''
)])

loader = TextLoader('aws.knowledge')
aws_knowledge = loader.load()[0].page_content
chain = prompt | llm | output_parser

# ============== MANAGE SESSION STATE ========================
if "current_code" not in st.session_state:
    st.session_state.current_code = None
if "response" not in st.session_state:
    st.session_state.response = None


# ============== MAIN FUNCTIONS ========================
# @st.cache_data
def invoke(user_request):
    """Call chatgpt to process user input, store the response in cache memory"""
    response = chain.invoke({"aws_knowledge": aws_knowledge, "user_request": user_request})
    return response

def extract_main_content(text):
    """Extract the main content from the given text"""
    # print(f"DEBUG:RESPONSE:{text}")
    code_start = text.find("```python")

    if code_start != -1:
        main_content = text[0:code_start].strip()
        if len(main_content) == 0:
            return None
        else:
            return main_content
    else:
        return text

def extract_diagram_code(text):
    """Extract the diagram code from the given text"""
    print(f"DEBUG:RESPONSE:{text}")
    code_start = text.find("```python")

    if code_start != -1:
        code_end = text.find("```", code_start + 1)

        if code_start != -1 and code_end != -1:
            code_to_execute = text[code_start + len("```python"):code_end].strip()
            return code_to_execute
        else:
            st.write("There is no Python code in DIAGRAM part.")
    else:
        st.write("There is no DIAGRAM part")
    return None

# ============== MAIN PAGE SECTION ========================
btn_settings_editor_btns = [{
    "name": "Generate Diagram",
    "feather": "RefreshCw",
    "primary": True,
    "alwaysOn": True,
    "hasText": True,
    "showWithIcon": True,
    "commands": ["submit"],
    "style": {"top": "0rem", "right": "0.4rem"}
  }]

def main_page():
    st.header("👨‍💻 Chat with Diagram Agent")
    user_request = st.text_area(label="What is your Problem Statement?",
                                value="Mobile application -> DNS ->  Load Balancer -> 3 web services -> 2 Database servers ")

    clicked = st.button(" Generate Code!", type="primary")
    if clicked:
        with st.spinner("I'm thinking...wait a minute!"):
            response = invoke(user_request)
            st.session_state.response = response
            st.session_state.current_code = extract_diagram_code(response)

    code = st.session_state.current_code
    if code is not None:
        col1, col2 = st.columns([5,5])
        with col1:
            st.write(extract_main_content(st.session_state.response))
            response_dict = code_editor(code, lang="python", buttons=btn_settings_editor_btns)
        with col2:
            code_string = response_dict["text"]
            if response_dict["type"] == "submit" and len(code_string) != 0:
                exec(code_string)


if __name__ == '__main__':
    main_page()
