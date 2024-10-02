# LLM PDF Question Answering Bot

## Overview
This project implements an AI agent that leverages OpenAI’s GPT-3.5 model to extract answers from a PDF document and post the results on Slack. The agent takes a PDF file and a list of questions as input, retrieves answers from the content of the PDF, and posts those answers to a specified Slack channel. The implementation avoids using pre-built chains from frameworks like Langchain and LLama Index to ensure a custom solution.

## Demo Video

You can view the demo video in the repository under the `media` folder:

[Demo Video](./media/1.mp4)


## Features
- **PDF Parsing**: Extracts text from large PDF documents.
- **OpenAI Integration**: Uses GPT-3.5 to generate answers to specific questions based on the content of the PDF.
- **Slack Integration**: Posts answers to a Slack channel of your choice using Slack’s API.
- **Environment Security**: OpenAI API keys and Slack tokens are securely handled using environment variables.

## Tech Stack
- **Python**: Core programming language.
- **OpenAI GPT-3.5**: Language model for question answering.
- **Slack API**: For posting messages to Slack channels.
- **pdfplumber**: Library for extracting text from PDF files.
- **slack_sdk**: SDK for Slack bot interactions.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/code-griffin/LLM_PDF_QA_Bot.git
cd LLM_PDF_QA_Bot
```

### 2. Install Dependencies
Make sure you have Python 3.7+ installed. Install the required Python packages using pip:

```bash
pip install openai langchain pdfplumber slack_sdk
```

### 3. Set Up Environment Variables
To ensure that sensitive information such as API keys are not hard-coded, use environment variables.

#### Windows:
```bash
set OPENAI_API_KEY=your-openai-api-key
set SLACK_BOT_TOKEN=your-slack-bot-token
```

#### macOS/Linux:
```bash
export OPENAI_API_KEY=your-openai-api-key
export SLACK_BOT_TOKEN=your-slack-bot-token
```

### 4. Usage

1. **PDF File**: Place your PDF file in the desired directory or point to an existing PDF file.
2. **Questions**: Modify the list of questions in the Python script to include the questions you want to ask.
3. **Slack Channel**: Set the desired Slack channel name (e.g., `#general`) in the script.

#### Example:
```python
# Sample usage
if __name__ == "__main__":
    # Input PDF file path
    pdf_path = "/path/to/your/pdf/document.pdf"

    # List of questions
    questions = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?"
    ]

    # Slack channel to post results
    slack_channel = "#your-slack-channel"  # Replace with your Slack channel name

    # Call the main function to process the PDF and post results
    process_pdf_and_post_to_slack(pdf_path, questions, slack_channel, openai_api_key, slack_token)
```

### 5. Run the Script
Once everything is set up, run the Python script:
```bash
python your_script.py
```

This will extract the relevant answers from the PDF and post the results to your specified Slack channel.

## Sample Output in Slack
The bot will post a message like this to the specified Slack channel:

```
Here are the answers:

Q: What is the name of the company?
A: Zania, Inc.

Q: Who is the CEO of the company?
A: Shruti Gupta

Q: What is their vacation policy?
A: Refer to section 7.7 Vacation.

Q: What is the termination policy?
A: Refer to section 5.10 Resignation Policy.
```

## Improvements
To further enhance this solution:
1. **PDF Parsing Optimization**: For large PDF files, consider adding a method to intelligently navigate and extract only relevant sections based on the question.
2. **Confidence Levels**: Use GPT-3’s token log probabilities to filter out answers with low confidence.
3. **Error Handling**: Improve error handling for edge cases (e.g., malformed PDFs, Slack API failures).
4. **Caching**: Implement caching for frequently queried documents to reduce redundant API calls and costs