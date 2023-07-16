# Interview Question Generator

The Interview Question Generator is a powerful tool designed to assist you in generating potential interview questions based on the job URL you provide. This tool leverages various technologies, including BeautifulSoup, markdownify, LangChain, and OpenAI, to provide accurate and relevant question suggestions.

## How It Works

1. Input the job URL: Simply enter the URL of the job description or posting you want to generate interview questions for.

2. Processing the URL: The tool uses the BeautifulSoup library to extract relevant information from the job URL, such as the job title, qualifications, responsibilities, and any other pertinent details.

3. Analyzing the job requirements: The tool analyzes the extracted information to understand the key skills, qualifications, and responsibilities associated with the job.

4. Generating interview questions: Based on the analyzed data, the tool generates a list of interview questions that cover various aspects of the job. These questions are designed to help you assess candidates' suitability for the position.

5. Review and customization: Once the questions are generated, you have the flexibility to review and customize them further to align with your specific requirements or preferences.

## Dependencies

The Interview Question Generator relies on the following technologies:

- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#): A Python library used for web scraping and extracting information from HTML and XML documents.

- [markdownify](https://pypi.org/project/markdownify/): A Python library that converts HTML content to Markdown format, making it easier to process and manipulate.

- [LangChain](https://langchain.com/): A language analysis and processing tool that helps identify key information and extract relevant insights from textual data.

- [OpenAI](https://openai.com): An advanced AI platform that powers the language generation capabilities of this tool, providing accurate and context-aware interview questions.

## Usage

1. Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt

2. Run The App

streamlit run main.py