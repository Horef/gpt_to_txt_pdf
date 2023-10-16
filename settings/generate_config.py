import configparser

def generate_settings():
    """
    Generates setting for all of the chat properties.
    """

    # Create a config parser object
    config_file = configparser.ConfigParser()

    # Database Settings section
    config_file['Database Settings']={
        'database_name': 'chat.db',
        'table_name': 'chat',
        'clear_db': 'True',
        'first_run': 'True'
    }

    # GPT Settings section
    config_file['GPT Settings'] = {
        'api_key_path': 'api_key.txt',
        'temperature': '0.3',
        'max_tokens': '8192',
        'model': 'gpt-3.5-turbo-16k',#optional gpt-4
        'prompt': '''
        Imagine that you are a person whose job is to produce ideas to move the scientific progress forward.
        Every day your head is filled with novel propositions based upon your high general knowledge of the world, and a very broad and deep scientific experience.
        Sometimes, you encounter new ideas posed by the peple you know, and you like to extrapolate them into a full-fledged plans of a possible future use.
        You will now be provided with such an idea, and please write your extrapolation from it in the following manner:
        1. Write an abstract on the plan - a short summary of your ideas.
        2. Take a deep breath and provide a step by step process to implementing your plan into life, and of the connections that you made between different ideas.
        3. Provide a few ideas that may improve the performance of your plan. And a few ideas that might be the next steps in the logical succession of the original proposition.
        4. Include a short ending containing the pros and cons of your approach. Try to incorporate as many constructive arguments supporting and rejecting your arguments.
        5. Provide a list of keywords (or search expressions) from the ideas you have provided, that one may use to search further information on the subject.
        The idea to extrapolate on:
        '''
    }

    # PDF Generator Settings section
    config_file['PDF Generator Settings'] = {
        'txt_folder': '/Users/sergiyhoref/Desktop/text_files',
        'txt_name': 'random', # random is a placeholder for the current time
        'pdf_folder': '/Users/sergiyhoref/Desktop/pdf_files',
        'pdf_name': 'random', # random is a placeholder for the current time
        'document_title': 'Chat Results',
        'title': 'Chat Results',
        'font_size': '14',
        'dpi': '96'
    }

    # Commit and push
    with open(r"settings/config.ini", "w") as file:
        config_file.write(file)
        file.flush()
        file.close()

    print("Config file created successfully")