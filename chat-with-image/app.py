
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
import base64, httpx

# Page setting
st.set_page_config(layout="wide")

# Replace it with your OPENAI API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


class ProductDataExtractor(BaseModel):
    product_name: str = Field(description="Product Name")
    product_price: str = Field(description="Product Price with two decimal places")


class InvoiceDataExtractor(BaseModel):
    business_name: str = Field(description="Business Name")
    business_address: str = Field(description="Business Address")
    amount: float = Field(description="total amount with two decimals")
    products: List[ProductDataExtractor] = Field(description="product list")


# Init langchain
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
llm.model_name = "gpt-4o"

parser = PydanticOutputParser(pydantic_object=InvoiceDataExtractor)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an useful assistant. Wrap the output in `json` tags\n{format_instructions}"),
    ("human", [
        {"type": "text", "text": """{question}"""},
        {
            "type": "image_url",
            "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
        },
    ]),
])


chain = prompt | llm | parser

if "action" not in st.session_state:
    st.session_state.action = ""


def main_page():
    st.header("📗 Invoice Extractor")

    url = st.text_input("Please enter your Invoice URL",
                        value="https://marketplace.canva.com/EAFC1OcYOM0/2/0/1131w/canva-black-white-minimalist-simple-creative-freelancer-invoice-pyLVaYlAk1o.jpg")
    clicked = st.button("Load Image", type="primary")
    if clicked:
        st.session_state.action = "SHOW_IMAGE"

    if st.session_state.action == "SHOW_IMAGE":
        col1, col2 = st.columns([4, 6])
        with col1:
            with st.expander("Image:", expanded=True):
                st.image(url, use_column_width=True)

        with col2:
            extract_clicked = st.button("Extract Invoice Information", type="primary")
            with st.expander("Parser Format Instruction:", expanded=True):
                st.write(parser.get_format_instructions())
            if extract_clicked:
                with st.spinner("I'm thinking...wait a minute!"):
                    with st.container(border=True):
                        image_data = base64.b64encode(httpx.get(url).content).decode("utf-8")
                        invoice = chain.invoke({"format_instructions":parser.get_format_instructions(),"question": "extract the content", "image_data": image_data})

                        #Extract information from invoice object
                        st.write(f"Business Name: {invoice.business_name}")
                        st.write(f"Business Address: {invoice.business_address}")
                        st.write(f"Total Amount: {invoice.amount}")
                        for index, product in enumerate(invoice.products):
                            st.write(f" Product:{index}: Name: {product.product_name} : Price : {product.product_price}")

if __name__ == '__main__':
    main_page()
