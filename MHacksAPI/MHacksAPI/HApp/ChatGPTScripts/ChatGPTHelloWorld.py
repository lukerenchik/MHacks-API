# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:26:12 2022

@author: Derek Joslin
"""

import openai
import os

# Set the organization and API key for authentication
openai.organization = "org-sPMdhEdIci9y8jimrE2FDrVu"
openai.api_key = os.getenv("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")

# List available models
models = openai.Model.list()

# Filter the list to find the davinci GPT model
davinci_model = [m for m in models if m.id == "davinci"][0]

# Use the davinci GPT model to generate text
response = davinci_model.completions(
    prompt="The quick brown fox jumps over the lazy dog.",
    max_tokens=128,
    temperature=0.5,
)

# Print the generated text
print(response.choices[0].text)


