from openai import OpenAI
import os

def describe_image(image_url):
    """
    This function takes an image URL and returns a description of the image using OpenAI's API.

    Args:
    image_url (str): The URL of the image to be described.

    Returns:
    str: A description of the image.
    """
    openAIkey = "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"
    client = OpenAI(api_key=openAIkey)

    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Describe the core aspects of the image using a single sentence designed at giving a user who has never seen the image a clear idea of what is happening.",
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image_url,
              },
            }
          ],
        }
      ],
      max_tokens=300,
    )

    choice = response.choices[0]  # Get the first (and likely only) choice from the response
    message = choice.message  # Access the 'message' attribute of the Choice object
    output_text = message.content  # Extract the 'content' from the message
    return output_text
