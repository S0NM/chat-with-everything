# 🎬 Chat with Youtube

### **Level**: Beginner 🎖️ 

### 1. Our Goal 🎯

* Understand the content of a YouTube video without watching it
* Search for useful information in the video without missing anything
* Interact with the YouTube video content through a chat interface

These are the things you can do with the "chat with YouTube" technique here.

**Tech Stack**

- Streamlit
- Langchain ([Working with Youtube Audio](https://python.langchain.com/v0.2/docs/integrations/document_loaders/youtube_audio/))

Take a look at the following demo to understand what we will achieve :)):

![chat-with-youtube](https://github.com/S0NM/chat-with-everything/blob/26afd07d1f5029f2ed504610d779fef3a896de11/gif/chat-with-youtube.gif)

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

...Will be updated later...

-----------
#### Fix issues
If you meet the issue: "ERROR: Postprocessing: ffprobe and ffmpeg not found. Please install or provide the path using --ffmpeg-location"
After that you can solve this problem by installing the missing ffmpeg.

```shell
# Ubuntu and debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

## Windows:
choco install ffmpeg* 
```




