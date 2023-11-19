from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="variables.env")
apiKey = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=apiKey)
def talkWithGPT():
    prompt = input("Input: ")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    return

def GPTRewrite(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Please rewrite the following text with proper formatting" + text}
        ]
    )
    content = response.choices[0].message.content
    return content
if __name__ == "__main__":
    talkWithGPT()
