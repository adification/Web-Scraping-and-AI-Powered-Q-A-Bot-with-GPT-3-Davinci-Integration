from bs4 import BeautifulSoup
import requests
import openai
import re

# Set up OpenAI API credentials
openai.api_key='API KEY'

def extract_plain_text_from_html(html_content):
    try:
        # Parsing HTML content with BeautifulSoup
        soup=BeautifulSoup(html_content, 'html.parser')

        # Extracting useful plain text from the parsed HTML
        plain_text=soup.get_text()

        # Remove leading/trailing whitespaces and extra line breaks
        plain_text=re.sub(r'^\s+|\s+$', '', plain_text, flags=re.MULTILINE)
        plain_text=re.sub(r'\n{2,}', '\n\n', plain_text)

        return plain_text

    except Exception as e:
        print("Error:", e)
        return None

# User input for URL
url=input("Enter the URL to scrape: ")

# Scraping using the web scraping API
api_key='API KEY'
payload={'api_key': api_key, 'url': url, 'dynamic': 'false'}
resp=requests.get('https://api.scrapingdog.com/scrape', params=payload)

if resp.status_code==200:
    html_output=resp.text
    # Extract plain text from the HTML content
    plain_text=extract_plain_text_from_html(html_output)

    if plain_text:
        # Generate tokens to understand the background
        prompt="Text: " + plain_text[:4096]  # Limit to 4096 tokens
        response=openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7
        )
        background=response.choices[0].text.strip()

        # Start the Q&A interaction
        print("Q&A Bot is ready. Ask your questions or enter 'exit' to quit.")
        while True:
            question=input("You: ")
            if question.lower() == "exit":
                break

            # Generate answer tokens based on the question and background
            prompt = "Question: " + question + "\nAnswer:"
            prompt += "\nText: " + plain_text[:4096]  # Limit to 4096 tokens
            prompt += "\nBackground: " + background
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7
            )
            answer = response.choices[0].text.strip()

            # Display the answer
            print("Bot: " + answer)
    else:
        print("Error: Unable to extract plain text from the provided HTML content.")
else:
    print("Error: Unable to fetch the HTML content from the provided URL.")
