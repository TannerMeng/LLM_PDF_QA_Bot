import openai
import pdfplumber
from slack_sdk import WebClient
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Function to get answers from GPT-3.5 using OpenAI API
def get_answers_from_gpt(questions, document_text, openai_api_key):
    openai.api_key = openai_api_key
    answers = {}

    try:
        for question in questions:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on a provided document."},
                    {"role": "user", "content": f"Document: {document_text}\nQuestion: {question}"}
                ],
                max_tokens=100
            )
            answer_text = response['choices'][0]['message']['content'].strip()
            answers[question] = answer_text if answer_text else "Data Not Available"
    except Exception as e:
        print(f"Error in getting answers from GPT-3.5: {e}")
        return {}

    return answers

# Function to format answers for Slack
def format_answers_for_slack(answers):
    formatted_message = "Here are the answers:\n"
    for question, answer in answers.items():
        formatted_message += f"Q: {question}\nA: {answer}\n\n"
    return formatted_message

# Function to post a message to Slack
def post_to_slack(channel, message, slack_token):
    client = WebClient(token=slack_token)
    try:
        # Post the message to the specified Slack channel
        response = client.chat_postMessage(channel=channel, text=message)
        assert response["ok"]
        print("Message successfully posted to Slack.")
    except Exception as e:
        print(f"Error posting to Slack: {e}")

# Main function to process PDF and post results to Slack
def process_pdf_and_post_to_slack(pdf_path, questions, slack_channel, openai_api_key, slack_token):
    # Step 1: Extract text from PDF
    document_text = extract_text_from_pdf(pdf_path)

    # Check if the document text is too long, truncate if necessary
    if len(document_text) > 2000:  # GPT-3.5 token limit, adjust if needed
        document_text = document_text[:2000] + "... (truncated)"

    # Step 2: Get answers using GPT-3.5
    answers = get_answers_from_gpt(questions, document_text, openai_api_key)

    # Step 3: Format answers for Slack
    slack_message = format_answers_for_slack(answers)

    # Step 4: Post the message on Slack
    post_to_slack(slack_channel, slack_message, slack_token)

# Sample usage
if __name__ == "__main__":
    # Input PDF file path
    pdf_path = "handbook.pdf"  # Update this path based on your setup

    # List of questions
    questions = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?"
    ]

    # Load API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this environment variable
    slack_token = os.getenv("SLACK_BOT_TOKEN")  # Make sure to set this environment variable

    if not openai_api_key or not slack_token:
        print("Error: Missing API keys. Ensure OPENAI_API_KEY and SLACK_BOT_TOKEN environment variables are set.")
    else:
        # Slack channel to post results
        slack_channel = "#llm"  # Replace with your Slack channel name

        # Call the main function to process the PDF and post results
        process_pdf_and_post_to_slack(pdf_path, questions, slack_channel, openai_api_key, slack_token)
        
