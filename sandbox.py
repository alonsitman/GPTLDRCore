from newspaper import Config
from newspaper import Article
import json
import io
import os
import openai

#A new article from TOI
url = "https://www.haaretz.co.il/news/world/europe/2023-06-06/ty-article-magazine/.premium/00000188-910c-d3a7-adcf-b10f5b750000"

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = user_agent

#For different language newspaper refer above table
# toi_article = Article(url, config=config) # en for English

# import nltk
# nltk.download('punkt')

#To perform natural language processing ie..nlp
# toi_article.nlp()

# #To extract summary
# print("Article's Summary:")
# print(toi_article.summary)
# print("n")

# #To extract keywords
# print("Article's Keywords:")
# print(toi_article.keywords)


def create_config():
    
    path = 'DefaultConfig.json'
    if not os.path.isfile(path): # check if file exists
      
        config_dict = {'number of bulletins': 3,
                   'max words per bulletin': 15}
        
        # json_string = json.dumps(config_dict)
        # json_file = open("DefaultConfig.json", "w")
        # json_file.write(json_string)
        # json_file.close()

        with io.open(os.path.join('DefaultConfig.json'), 'w') as json_file:
            json_file.write(json.dumps(config_dict))

    else:
        print('File exists')
        

def read_config():

    # Opening JSON file
    with open('DefaultConfig.json', 'r') as openfile:
    
        # Reading from json file
        config_dict = json.load(openfile)
    
    return config_dict


# create_config()
# read_config()

# Define OpenAI API key 
openai.api_key = "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"

num_bulletins = 5
num_words = 20
title = "Paris secures signing of French prodigy Nadir Hifi"
text = """ Paris Basketball is already putting its plans for next season into place, 
            with the club announcing the signing of talented point guard Nadir Hifi from fellow French side Le Portel on a three-year deal.
            Hifi (20 years old, 1.84 meters) impressed with Le Portel in the French top flight in the 2022-23 season, averaging 16.8 points, 2.7 rebounds, 3.4 assists and 1.3 steals across 33 games.
            "I'm very proud and honored to be signing with Paris Basket!" Hifi said during his introductory press conference.
            "At this stage of my career, I really think it's the best project for me to continue my development.
            I fully share the club's ambition and am determined to help it achieve its many goals!
            I can't wait to meet my teammates and the staff and start this new adventure!" """


# Set up the model and prompt
model_engine = "text-davinci-003"

prompt = "Give output in tldr style, " \
        f"return response with max {num_bulletins} bulletins and max {num_words} words per bulletin." \
        f"The article title is: {title} and article text is: {text}"
            
# Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

response = completion.choices[0].text
print(response)