# GPT Sanity check - "What is the most populated country in the world?"

from newspaper import Article
import openai
import sys
import os
import json
 

def default_config(filename):
 
    if os.path.isfile(filename) and os.path.getsize(filename): # check if file exists and not empty
        print('Configuration already exists')
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


def get_params():
    
    if len(sys.argv) > 1:
        url = sys.argv[1] #user passes url in terminal after python file name which is at sys.argv[0]
        return url
    
    return None


def validate_url(url):
    
    space = ' '
    if space in url:
        return False    
    
    return True


def get_article(url): #using newspaper module

    article = Article(url)
    article.download()
    article.parse()
    
    return article


def extract_title(article):
    
    title = article.title
    
    return title


def extract_text(article):
    
    text = article.text #perhaps it should be article.text
    
    return text


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

    print(response)


def main_runner(url):

    filename = 'config.json'
    
    # Handle configurations
    default_config(filename)
    config_dict = read_config(filename)
    num_bulletins = config_dict['num_bulletins']
    num_words = config_dict['num_words']
    key = config_dict['api_key']

    # Get URL from cmd line argument:
    
    if not url:
        url = get_params()
        if not url:
            print("Missing URL")
            return None
    
    # Check that the URL is vald:
    if not validate_url(url):
        print("Please insert URL without spaces") 
        return None
   
    # Download and parse the article:
    article = get_article(url)
    
    # Extract title and text from article + tldr configurations from JSON:
    title = extract_title(article)
    text = extract_text(article)

    # Prepare query, send it and display result
    query = prepare_query(num_bulletins, num_words, title, text)
    response = send_query(key, query)
    
    display_result(response)

    return response      

def main():
    main_runner(None)

# main()
