# GPT Sanity check - "What is the most populated country in the world?"

import openai
import os
import json
 

def default_config(filename):
 
    if os.path.isfile(filename) and os.path.getsize(filename): # check if file exists and not empty
        # print('Configuration already exists')
        return False
    
    default_config = {
                    'num_bulletins': 3,
                    'num_words': 15,
                    'api_key': 'PUT_YOUR_OPENAI_KEY_HERE'
                    }
    
    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(default_config))        
    
    return True


def read_config(filename):

    config_dict = None

    with open(filename, 'r') as openfile:  # Open json to read from
        if os.path.getsize(filename):
            config_dict = json.load(openfile)   # Read from json into dictionary

    return config_dict


def prepare_query(num_bulletins, num_words, title, text): #Embed "tldr" command, configurations, title and text in prompt

    query = "Give output in tldr style, " \
            f"return response with exactly {num_bulletins} bulletins and exactly {num_words} words per bulletin." \
            f"The article title is: {title} and article text is: {text}"
    
    return query


def send_query(key, query):
    
    openai.api_key = key

    # Set up the model and prompt
    model_engine = "text-davinci-003"
                
    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=query,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    
    return response


def display_result(response):
    print()
    print(response)
    print()


def run(title, text, filename='config.json'):
    # Handle configurations
    default_config(filename)
    config_dict = read_config(filename)
    num_bulletins = config_dict['num_bulletins']
    num_words = config_dict['num_words']
    key = config_dict['api_key']

    # Prepare query, send it and display result
    query = prepare_query(num_bulletins, num_words, title, text)
    response = send_query(key, query)
    formatted_response = response.removeprefix("\n\n")
    formatted_tldr = f"{title}\n{str(formatted_response)}"
    display_result(formatted_tldr)

    return response