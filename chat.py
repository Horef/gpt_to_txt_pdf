from math import ceil

from pdf.pdf_generator import PdfGenerator

import text_processing as tp

from settings.generate_config import generate_settings
import configparser

import openai
import sys

class Chat:
    """
    A class to manage the chat.
    """
    def __init__(self):
        # Setting up the configurations.
        config = configparser.ConfigParser()
        config.read("settings/config.ini")

        # Loading the settings.
        self.temperature = config.getfloat("GPT Settings", "temperature")
        self.api_key_path = config.get("GPT Settings", "api_key_path")
        self.max_tokens = config.getint("GPT Settings", "max_tokens")
        self.model = config.get("GPT Settings", "model")
        self.prompt = config.get("GPT Settings", "prompt")

        self.completion_length = self.max_tokens

    def generate_response(self, arg):
        """
        Generates a response from the GPT API.
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{'role': 'system', 'content': self.generate_prompt(argument=arg)}],
            temperature=self.temperature,
            max_tokens=self.completion_length,
        )
        return response['choices'][0]['message']['content']

    def generate_prompt(self, argument: str) -> str:
        # Add the argument to the prompt defined in the config file.
        prompt = tp.preprocess(self.prompt + argument)

        # Calculate the number of tokens we pass into the gpt.
        # The number is always bigger than the actual tokenization, but it doesn't return an error this way.
        tokens_by_chars: int = ceil(len(prompt)/4)

        # Calculate the maximal number of tokens available to complete the prompt.
        self.completion_length = self.max_tokens - tokens_by_chars

        return prompt

def get_parameters() -> str:
    args = sys.argv[1:]
    arg = args[0]
    if len(args) > 0:
        for i in range(1,len(args)):
            arg += " " + args[i]
    return arg

if __name__ == "__main__":
    # Generating the settings file. 
    # Should be done before each run to ensure the settings are up to date.
    generate_settings()
    # Initializing the chat and pdf generator.
    chat = Chat()
    pdf = PdfGenerator()

    # Setting up the API key.
    openai.api_key_path = chat.api_key_path

    # Get the argument from the command line.
    arg = get_parameters()
    # Saving the original text passed.
    pdf.add_text(f"Original text: {arg}\n")

    # Run GPT
    response = chat.generate_response(arg=arg)
    pdf.add_text(f"GPT response: {response}")
    
    pdf.save_pdf()