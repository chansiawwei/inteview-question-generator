# LLMs
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from dotenv import load_dotenv

# Streamlit
import streamlit as st

# Twitter
import tweepy

# Scraping
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# YouTube
from langchain.document_loaders import YoutubeLoader
# !pip install youtube-transcript-api

# Environment Variables
import os
from dotenv import load_dotenv

load_dotenv()

# Get your API keys set
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', os.getenv("OPENAI_API_KEY"))

# Load up your LLM
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI()
    return llm

# A function that will be called only if the environment's openai_api_key isn't set
def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key (or set it as .env variable)",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text


# Here we'll pull data from a website and return it's text
def pull_from_website(url):
    st.write("Getting webpages...", url )
    # Doing a try in case it doesn't work
    try:
        response = requests.get(url)
    except:
        # In case it doesn't work
        print ("Whoops, error")
        return
    
    # Put your response in a beautiful soup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get your text
    text = soup.get_text()

    # Convert your html to markdown. This reduces tokens and noise
    text = md(text)
     
    return text
# Function to change our long text about a person into documents
def split_text(user_information):
    # First we make our text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)

    # Then we split our user information into different documents
    docs = text_splitter.create_documents([user_information])

    return docs

# Prompts - We'll do a dynamic prompt based on the option the users selects
# We'll hold different instructions in this dictionary below
response_types = {
    'Interview Questions' : """
        I will send you a webpage which include the job description.Your goal is to generate possible interview questions based on a job description listed on a webpage the user input.
        Please respond with list of a few interview questions based on the job description. Please list at least 20 question in the response.
    """,
}

map_prompt = """You are a helpful AI bot that aids a user in preparing for job interview.
Below is information about a person named {persons_name}.
Information will job descriptions about a role, please list some critical interview question that related to the job description.
Use specifics from the research when possible

{response_type}

% START OF INFORMATION ABOUT {persons_name}:
{text}
% END OF INFORMATION ABOUT {persons_name}:

YOUR RESPONSE:"""
map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "persons_name", "response_type"])

combine_prompt = """
You are a helpful AI bot that aids a user in preparing for a job interview.
You will be given information about {persons_name} along with the job descriptions.
Based on the job descriptions, please generate a list of question that will help the user on preparing for the interview.

{response_type}

% PERSON CONTEXT
{text}

% YOUR RESPONSE:
"""
combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "persons_name", "response_type"])

# Start Of Streamlit page
st.set_page_config(page_title="Interview Prep", page_icon=":robot:")

# Start Top Information
st.header("Generate Interview Question based job description")
st.markdown("Have an interview coming up?  This tool is meant to help you generate possible interview questions based off of the job URL you input.\
                \n\nThis tool is powered by [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#) [markdownify](https://pypi.org/project/markdownify/), [LangChain](https://langchain.com/) and [OpenAI](https://openai.com)\n")
col1, col2 = st.columns(2)


# Collect information about the person you want to research
person_name = st.text_input(label="Person's Name",  placeholder="Eg: Jeff", key="persons_name")
webpages = st.text_input(label="Web Page URLs (Use , to seperate urls. Must include https://)",  placeholder="Enter the job's URL here: https://careers.anz.com/job/Melbourne-Front-End-Engineer/941697110/?jobPipeline=Indeed", key="webpage_user_input")

# Output
st.markdown(f"### {'Possible Interview Questions'}:")

# Get URLs from a string
def parse_urls(urls_string):
    """Split the string by comma and strip leading/trailing whitespaces from each URL."""
    return [url.strip() for url in urls_string.split(',')]

# Get information from those URLs
def get_content_from_urls(urls, content_extractor):
    """Get contents from multiple urls using the provided content extractor function."""
    return "\n".join(content_extractor(url) for url in urls)

button_ind = st.button("*Generate Output*", type='secondary', help="Click to generate output based on information")

# Checking to see if the button_ind is true. If so, this means the button was clicked and we should process the links
if button_ind:
    website_data = get_content_from_urls(parse_urls(webpages), pull_from_website) if webpages else ""
    user_information = "\n".join([website_data])

    user_information_docs = split_text(user_information)

    # Calls the function above
    llm = load_LLM(openai_api_key=OPENAI_API_KEY)

    chain = load_summarize_chain(llm,
                                 chain_type="map_reduce",
                                 map_prompt=map_prompt_template,
                                 combine_prompt=combine_prompt_template,
                                 # verbose=True
                                 )
    
    st.write("Sending request to LLM...")
    st.write("Be back with a list of question")

    # Here we will pass our user information we gathered, the persons name and the response type from the radio button
    output = chain({"input_documents": user_information_docs, # The seven docs that were created before
                    "persons_name": person_name,
                    "response_type" : response_types['Interview Questions']
                    })

    st.markdown(f"#### Output:")
    st.write(output['output_text'])