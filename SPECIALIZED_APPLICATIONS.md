# Specialized Applications and Advanced Prompt Patterns

## Overview

This document provides comprehensive documentation of the specialized applications and advanced prompt engineering patterns in the Chat with Everything project. These applications demonstrate sophisticated LLM integration techniques beyond basic document Q&A.

## Specialized Applications

### 1. Chat with Data - PandasAI Integration

**File**: `/home/daytona/chat-with-everything/chat-with-data/app.py`  
**Purpose**: Natural language interface for structured data analysis  
**Complexity Level**: Intermediate  
**Key Technology**: PandasAI with OpenAI integration

#### Architecture and Implementation

```python
# PandasAI Integration Setup
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai.connectors import PandasConnector
from pandasai.responses.response_parser import ResponseParser

# Custom Response Parser for Streamlit Integration
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
```

#### Advanced Features

1. **Multi-Format Response Handling**
   - **Text Responses**: Direct answers and explanations
   - **DataFrame Responses**: Tabular data results displayed with `st.dataframe()`
   - **Plot Responses**: Generated visualizations displayed with `st.image()`

2. **Enhanced Data Context**
   ```python
   field_descriptions = {
       "tconst": "An alphanumeric unique identifier of the title",
       "titleType": "the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)",
       "primaryTitle": "the more popular title / the title used by the filmmakers on promotional materials",
       "originalTitle": "original title, in the original language",
       "isAdult": "0: non-adult title; 1: adult title",
       "startYear": "represents the release year of a title. YYYY format",
       "endYear": "TV Series end year. \\N means null value",
       "runtimeMinutes": "primary runtime of the title, in minutes. \\N means null value",
       "genres": "includes up to three genres associated with the title"
   }
   ```

3. **Smart DataFrame Configuration**
   ```python
   connector = PandasConnector(
       {'original_df': df}, 
       field_descriptions=field_descriptions
   )
   agent = SmartDataframe(connector,
       config={
           "llm": llm,
           "conversational": False,
           "response_parser": MyStResponseParser,
       })
   ```

#### Technical Advantages
- **Natural Language Queries**: Users can ask questions in plain language
- **Automatic Code Generation**: PandasAI generates pandas code automatically
- **Cost Tracking**: Built-in token usage monitoring with `get_openai_callback()`
- **Visualization Support**: Automatic chart generation for data insights
- **Large Dataset Handling**: Optimized for 10M+ record datasets

### 2. Chat with Diagram Agent - AWS Architecture Generation

**File**: `/home/daytona/chat-with-everything/chat-with-diagram-agent/app.py`  
**Purpose**: Natural language to AWS architecture diagram conversion  
**Complexity Level**: Advanced  
**Key Technology**: Advanced prompt engineering with Python diagrams library

#### Sophisticated Prompt Engineering Architecture

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a solution architecture expert with over 15 years of experience working with AWS Web Services"),
    ("user", '''
# CHARACTER
You have the following skills {SKILLS}, and your answer should adhere to the constraints {CONSTRAINTS}. 
Based on the following user input, choose the corresponding {SKILLS} and process it.
User input: {user_request}

# SKILLS
## SKILL 1: Converting the user's workflow into a Diagram
Steps:
- Map components in the workflow to corresponding components in the AWS Solution Stack.
- Clean and correct the workflow appropriately.
- Create a Diagram from the refined workflow.
Response Format: The response must follow the TYPE1 format

## SKILL 2: Finding and advising a solution based on the user's needs
Steps:
- Think step-by-step to provide the best solution, using AWS Services
- Create a Diagram from the process
Response Format: The response must follow the TYPE2 format.

## SKILL 3: Show how to use any AWS service
Steps:
- Show the best practices of the service along with a useful sample workflow.
Response Format: The response must follow the TYPE2 format.

# CONSTRAINTS
## CONSTRAINT 1: Responses in TYPE1 format
- Your response contains only the Python code

## CONSTRAINT 2: Responses in TYPE2 format
- Short explanation and conclusion with the Python code at the bottom.

## CONSTRAINT 3: Diagram creation method
- Use the Python diagram library to create the code.
- Always refer to the list: {aws_knowledge}.
- The generated code snippet must combine Streamlit to display the diagram.
''')
])
```

#### Advanced Prompt Engineering Features

1. **Multi-Skill Architecture**: Three distinct skills for different user intents
2. **Constraint-Based Responses**: Structured output formats (TYPE1/TYPE2)
3. **Knowledge Base Integration**: AWS service mappings from `aws.knowledge` file
4. **Interactive Code Execution**: Real-time code editing and execution

#### Knowledge Base Integration

```python
# AWS Knowledge Base Loading
loader = TextLoader('aws.knowledge')
aws_knowledge = loader.load()[0].page_content

# Knowledge base contains mappings like:
# diagrams.aws.analytics.Analytics
# diagrams.aws.analytics.Athena
# diagrams.aws.compute.EC2
# diagrams.aws.database.RDS
```

#### Interactive Code Execution

```python
# Interactive code editor integration
from code_editor import code_editor

response_dict = code_editor(code, lang="python", buttons=btn_settings_editor_btns)
code_string = response_dict["text"]
if response_dict["type"] == "submit" and len(code_string) != 0:
    exec(code_string)  # Real-time code execution
```

#### Technical Innovations
- **Dynamic Code Generation**: Creates executable Python code for diagram generation
- **Interactive Editing**: Users can modify generated code in real-time
- **Knowledge-Grounded Responses**: Prevents hallucination by referencing actual AWS services
- **Multi-Modal Output**: Combines text explanations with visual diagrams

### 3. Chat with Image - Vision Capabilities

**File**: `/home/daytona/chat-with-everything/chat-with-image/app.py`  
**Purpose**: Structured data extraction from images using vision models  
**Complexity Level**: Advanced  
**Key Technology**: GPT-4o vision with Pydantic structured output parsing

#### Structured Output Parsing with Pydantic

```python
# Hierarchical Data Models
class ProductDataExtractor(BaseModel):
    product_name: str = Field(description="Product Name")
    product_price: str = Field(description="Product Price with two decimal places")

class InvoiceDataExtractor(BaseModel):
    business_name: str = Field(description="Business Name")
    business_address: str = Field(description="Business Address")
    amount: float = Field(description="total amount with two decimals")
    products: List[ProductDataExtractor] = Field(description="product list")
```

#### Multi-Modal Prompt Architecture

```python
# Vision-enabled prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an useful assistant. Wrap the output in `json` tags\n{format_instructions}"),
    ("human", [
        {"type": "text", "text": "{question}"},
        {
            "type": "image_url",
            "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
        },
    ]),
])

# Structured output parser
parser = PydanticOutputParser(pydantic_object=InvoiceDataExtractor)
chain = prompt | llm | parser
```

#### Image Processing Pipeline

```python
# Image data processing
image_data = base64.b64encode(httpx.get(url).content).decode("utf-8")
invoice = chain.invoke({
    "format_instructions": parser.get_format_instructions(),
    "question": "extract the content", 
    "image_data": image_data
})

# Structured data access
st.write(f"Business Name: {invoice.business_name}")
st.write(f"Business Address: {invoice.business_address}")
st.write(f"Total Amount: {invoice.amount}")
for index, product in enumerate(invoice.products):
    st.write(f"Product {index}: {product.product_name} : {product.product_price}")
```

#### Vision Processing Advantages
- **Structured Extraction**: Converts unstructured visual data to structured objects
- **Type Safety**: Pydantic models ensure data type consistency
- **Hierarchical Data**: Supports nested data structures (products within invoices)
- **Format Instructions**: Transparent parsing instructions for debugging

## Advanced Prompt Engineering Patterns

The project includes three sophisticated prompt engineering patterns that demonstrate advanced techniques for improving LLM reliability and performance.

### 1. Error Handling Pattern

**File**: `/home/daytona/chat-with-everything/prompt-implementation-patterns/error_handling.py`

```python
# Validation-Based Retry Mechanism
def validate_answer(answer):
    if answer.strip() == '120':  # Expected factorial of 5
        return True
    return False

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

# Usage example
response = invoke_with_retries(
    "What is the factorial of 5? Return the final result without any explanation"
)
```

#### Error Handling Features
- **Validation Logic**: Custom validation functions for answer verification
- **Retry Mechanism**: Configurable retry attempts with exponential backoff potential
- **Graceful Degradation**: Returns meaningful error messages when validation fails
- **Debug Logging**: Detailed attempt tracking for troubleshooting

### 2. Iterative Refinement Pattern

**File**: `/home/daytona/chat-with-everything/prompt-implementation-patterns/iterative_refinement.py`

```python
# Dual-Chain Architecture for Refinement
initial_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant and an expert Python developer."),
    ("user", "Create a python code to resolve the problem:{question}. Reply only python code without explanation")
])

refine_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant and an expert Python developer."),
    ("user", """ 
Enhance 3 things and regenerate the following code : {code} . Reply in json format like this:
------
{{"improvements": [[LIST ALL IMPROVEMENTS]],"code":[MAIN PYTHON CODE]}}
""")
])

def invoke_with_refinement(question, num_loop=3):
    code = chain.invoke({"question": question})
    print(f"DEBUG:Init:{code}")
    
    for i in range(num_loop):
        response = refine_chain.invoke({"code": code})
        response_json = convert_json(response)
        
        improvements = response_json["improvements"]
        code = response_json["code"]
        
        print(f"DEBUG:{i}:Improvement:{improvements}")
        print(f"DEBUG:{i}:Code:{code}")
```

#### Iterative Refinement Features
- **Progressive Improvement**: Each iteration builds on previous results
- **Structured Feedback**: JSON format ensures consistent improvement tracking
- **Transparency**: Detailed logging of improvements at each iteration
- **Flexible Iteration Count**: Configurable refinement cycles

### 3. Voting Pattern

**File**: `/home/daytona/chat-with-everything/prompt-implementation-patterns/voting.py`

```python
# Consensus-Based Decision Making
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

# Usage example
response = invoke_with_voting(
    "What is the best movie ever made? Your answer should contain only one movie title only"
)
```

#### Voting Pattern Features
- **Consensus Building**: Multiple LLM calls to reduce individual response bias
- **Statistical Confidence**: Uses frequency analysis to determine best answer
- **Configurable Voting**: Adjustable number of votes for different confidence levels
- **Bias Reduction**: Minimizes impact of outlier responses

## Advanced Pattern Comparison and Use Cases

| Pattern | Best Use Case | Advantages | Considerations |
|---------|---------------|------------|----------------|
| **Error Handling** | Factual questions with verifiable answers | High accuracy, deterministic validation | Requires known correct answers |
| **Iterative Refinement** | Code generation, creative tasks | Progressive improvement, transparency | Higher token usage, longer processing |
| **Voting** | Subjective questions, opinion-based queries | Bias reduction, statistical confidence | Multiple API calls, cost implications |

## Integration with Main Applications

These prompt patterns can be integrated into the main applications for enhanced reliability:

```python
# Enhanced PDF Chat with Error Handling
def enhanced_pdf_chat(question, content):
    def validate_pdf_answer(answer):
        # Custom validation logic for PDF content
        return len(answer) > 10 and "based on" in answer.lower()
    
    return invoke_with_retries(
        f"Based on this content: {content}. Question: {question}",
        validation_func=validate_pdf_answer
    )

# Enhanced Data Analysis with Voting
def enhanced_data_analysis(query, dataframe):
    responses = []
    for i in range(3):
        response = pandas_ai_agent.chat(query)
        responses.append(response)
    
    # Use voting for consistent results
    return most_common_response(responses)
```

## Technical Architecture Summary

The specialized applications demonstrate several advanced architectural patterns:

1. **Multi-Modal Processing**: Integration of text, images, and structured data
2. **Dynamic Code Generation**: Real-time code creation and execution
3. **Structured Output Parsing**: Type-safe data extraction with Pydantic
4. **Knowledge Base Integration**: External knowledge sources for grounded responses
5. **Interactive User Interfaces**: Real-time editing and feedback capabilities
6. **Advanced Prompt Engineering**: Sophisticated prompt patterns for reliability

## Performance and Scalability Considerations

### Cost Optimization
- **Token Management**: Efficient prompt design to minimize token usage
- **Caching Strategies**: Reuse of expensive computations
- **Model Selection**: Appropriate model choice based on task complexity

### Error Resilience
- **Graceful Degradation**: Fallback mechanisms for failed operations
- **Validation Layers**: Multiple validation strategies for different data types
- **User Feedback**: Clear error communication and recovery options

### Scalability Features
- **Modular Design**: Independent components for easy scaling
- **Stateless Operations**: Minimal session dependencies for horizontal scaling
- **Resource Management**: Efficient memory and CPU usage patterns

This comprehensive analysis of specialized applications and prompt patterns demonstrates the project's sophisticated approach to LLM integration, showcasing advanced techniques that can be applied to real-world production systems while maintaining excellent user experience and system reliability.
