import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from plantuml import PlantUML

# Page setting
st.set_page_config(layout="wide")

# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# ============== LANGCHAIN CONFIG SECTION ========================
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
# llm.model_name="gpt-4o"
llm.temperature = 0.2
output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a Solution Architect with more than 20+ years of experience"),
     ("user",'''
# GOAL:  
Based on your experience and best practices collected from the internet, thinking step-by-step to provide detailed-solution design to resolve user's problem statement: {problem_statement} using the C4 Model.
# OUTPUT:  
Your response should be structured into four sections based on C4 Model:  
#### 1. CONTEXT:
Provide a detailed-level of the system's context. Describe the system, the actors interacting with it, and the external systems. This section outline the major interactions and relationships. The answer should have clear explanation in bullet points format.
    
Diagram: Generate a diagram using PlanUML Python library that visually represents this part, include a Python code snippet that can be run using Streamlit to display the diagram (example: {{EXAMPLE}} below). Check & regenerate if code is run correctly.  

#### 2. CONTAINER:
Break down the system into major containers (applications, databases, services). Describe the responsibilities of each container and how they interact. The answer should have clear explanation in bullet points format.

Diagram: Generate a diagram using PlanUML Python library that visually represents this part, include a Python code snippet (with 'import' part) that can be run using Streamlit to display the diagram (example: {{EXAMPLE}} below). Check & regenerate if code is run correctly.

#### 3. COMPONENT:
Zoom in on one of the containers and describe its internal components and their responsibilities. Focus on the interactions between components. The answer should have clear explanation in bullet points format.

Diagram: Generate a diagram using PlanUML Python library that visually represents this part, include a Python code snippet (with 'import' part) that can be run using Streamlit to display the diagram (example: {{EXAMPLE}} below). Check & regenerate if code is run correctly.

#### 4. CODE:
Provide a detailed description of how specific classes or methods within a component are implemented to fulfill the design. This section should detail the code-level implementation. The answer should have clear explanation in bullet points format.

Diagram: Generate a diagram using PlanUML Python library that visually represents this part, include a Python code snippet (with 'import' part) that can be run using Streamlit to display the diagram (example: {{EXAMPLE}} below). Check & regenerate if code is run correctly.  

EXAMPLE  
```python  
import streamlit as st
from plantuml import PlantUML

# Define the PlantUML diagram
uml_code = """
@startuml
participant User
participant Server
participant Database

User -> Server: Request
Server -> Database: Query
Database --> Server: Result
Server --> User: Response
@enduml
"""

# Generate and display the diagram using PlantUML
plantuml = PlantUML(url="http://www.plantuml.com/plantuml/img/")
diagram_url = plantuml.get_url(uml_code)

st.image(diagram_url, caption="Healthcare Chatbot Architecture")
```

'''
)])

chain = prompt | llm | output_parser

if "content" not in st.session_state:
    st.session_state.content = ""

# ============== TEXT PROCESSING FUNCTIONS ========================
def extract_main_part(text,header):
    """Split CONCEPT part form the answer."""
    concept_start = text.find(header)
    diagram_start = text.find("```python", concept_start)
    if concept_start != -1 and diagram_start != -1:
        st.write(text[concept_start:diagram_start].strip())
    else:
        st.write("There is no CONCEPT part")


def extract_and_execute_diagram_part(text,header):
    """Split and execute python code in DIAGRAM part"""
    diagram_start = text.find(header)

    if diagram_start != -1:
        code_start = text.find("```python", diagram_start)
        code_end = text.find("```", code_start + 1)

        if code_start != -1 and code_end != -1:
            code_to_execute = text[code_start + len("```python"):code_end].strip()
            try:
                print(f"DEBUG:{code_to_execute}")
                exec(code_to_execute)
            except Exception as e:
                print(f"ERROR:{e}")
            return code_to_execute
        else:
            st.write(f"There is no Python code in {header} part.")
    else:
        st.write(f"There is no {header} part")
    return None

def show_diagram_part(text,header):
    col1, col2 = st.columns([6,4])
    with col1:
        extract_main_part(text, header)
    with col2:
        code = extract_and_execute_diagram_part(text, header)
        if code is not None:
            with st.expander(f"Show generated code for {header} Part", expanded=True):
                st.code(code)


# ============== MAIN PAGE SECTION ========================
def main_page():
    st.header("👨‍💻 Chat with Solution Expert")
    problem_statement = st.text_area(label="What is your problem statement?", value="Create a basic chatbot application for customer service team in a bank")

    clicked = st.button(" Generate solution!",type="primary")
    if clicked:

        with st.spinner("I'm thinking...wait a minute!"):
            with st.container(border=True):
                response = chain.invoke({"problem_statement": problem_statement})
                show_diagram_part(response,'CONTEXT:')
                show_diagram_part(response, 'CONTAINER:')
                show_diagram_part(response, 'COMPONENT:')
                show_diagram_part(response, 'CODE:')

if __name__ == '__main__':
    main_page()