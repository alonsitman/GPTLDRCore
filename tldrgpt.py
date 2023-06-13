# GPT Sanity check - "What is the most populated country in the world?"

from newspaper import Config
from newspaper import Article
import openai
import sys
import os
import io
import json
 

def default_config(filename):
 
    if os.path.isfile(filename): # check if file exists
        print('Configuration already exists')
        return False
    
    default_config = {
                    'num_bulletins': 3,
                    'num_words': 15
                    }
    
    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(default_config))        
    
    return True

def read_config(filename):

    with open(filename, 'r') as openfile:  # Open json to read from
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
    
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = user_agent

    article = Article(url, config=config)
    article.download()
    
    return article
  

def parse_article(article):
    
    parsed_article = article.parse()
    return parsed_article


def extract_title(article):
    
    title = article.title
    return title


def extract_text(article):
    
    text = article.text #perhaps it should be article.text
    return text


def prepare_query(num_bulletins, num_words, title, text): #Embed "tldr" command, configurations, title and text in prompt

    query = "Give output in tldr style, " \
            f"return response with max {num_bulletins} bulletins and max {num_words} words per bulletin." \
            f"The article title is: {title} and article text is: {text}"
    
    return query

def send_query(query):
    
    openai.api_key = "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"

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


def main():

    filename = 'config.json'
    
    # Handle configurations
    default_config(filename)
    config_dict = read_config(filename)
    num_bulletins = config_dict['num_bulletins']
    num_words = config_dict['num_words']

    # Get URL from cmd line argument:
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
    parse_article(article)
    
    # Extract title and text from article + tldr configurations from JSON:
    title = extract_title(article)
    text = extract_text(article)

    # Prepare query, send it and display result
    query = prepare_query(num_bulletins, num_words, title, text)
    response = send_query(query)
    display_result(response)        
    
main()
