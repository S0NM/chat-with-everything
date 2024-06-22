
# 📚 Chat with PDF 

### **Level**: Beginner 🎖️ 

### 1. Our Goal 🎯

The technique of using Large Language Models (LLMs) to work with PDFs is very important. It is a foundational technique for building document processing applications, automating workflows, content search tools, etc. In this section, you will learn:

- How to extract content from an uploaded PDF file 
- Basic Q&A application based on the extracted text content

**Tech Stack**

- Streamlit
- Langchain ([Working with PDF](https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/pdf/))
- [Some useful prompts to work with PDF](https://generativeai.pub/25-prompting-techniques-to-help-you-chat-with-pdf-like-a-pro-1524a2f52674)

**Take a look at the following demo to understand what we will achieve :))**
![chat-with-pdf](https://github.com/S0NM/chat-with-everything/blob/7af4afed918a6d392ab2a1774016267fd8dd54e6/gif/chat-with-pdf.gif)

### 2. How to get started?  🐌

1. Clone my GitHub repository

```bash
git clone https://github.com/S0NM/chat-with-everything.git
```
2. Install the required dependencies

```bash
pip install -r requirements.txt
```
3. Get your OpenAI API Key

- Sign up [OpenAI account](https://platform.openai.com/) (or the LLM provider of your choice) and get your API key.

4. Run the Streamlit App
```bash
streamlit run app.py
```


### 💰 3. Digging Deeper

If you want to challenge yourself, here are some ideas for you, guys:

**🎖️🎖️ Intermediate Level **
- **Finding the Right Model**: Experiment with different LLM models to find the one that best suits your problem.
- **Input Text Processing**: For optimal results, input text quality is crucial. Focus on preprocessing the input text, such as cleaning, removing redundant information, or reorganizing the input data.
- **Handling Large Data by Text Segmentation**: Guide on how to split large documents into smaller chunks to send to the LLM model (e.g., GPT-3.5-turbo has a limit of 16,385 tokens. GPT-4-turbo and GPT-4o will have a limit of 128,000 tokens).
- **Advanced State Management**: Guide on managing more complex conversation states, maintaining context across multiple requests.

**🎖️🎖️🎖️ Advanced Level **
- **Handling Non-Text Elements**: Guide on recognizing and processing images, charts, and tables in PDFs using additional tools.
- **Performance Optimization**: Optimize costs and latency when sending requests to LLM models in real-time applications.
- **Model Customization**: Fine-tune the model with domain-specific data to improve performance for specialized applications.

-----------
### Tài liệu tham khảo
* Streamlit
* Tài liệu working với pdf từ langchain: https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/pdf/
* https://medium.com/generative-ai/25-prompting-techniques-to-help-you-chat-with-pdf-like-a-pro-1524a2f52674
* 