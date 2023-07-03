import os
import json

def main_tester():

    url = "https://www.euroleaguebasketball.net/eurocup/news/paris-secures-signing-of-french-prodigy-nadir-hifi/"
    command = f"python3 tldrgpt.py {url}"
    num_of_lines = 4
    
    # Execute the command
    gpt_response = os.popen(command).read()
    gpt_response_processsed = gpt_response.split("\n")[-1 - num_of_lines : -1][1:]
    # Read the configuration from the config.json file
    with open('config.json') as config_file:
        config_dict = json.load(config_file)

    # test case 1: make sure a string is returned
    assert type(gpt_response_processsed) is list, "did not receive a response string from gpt"

    # test case 2: make sure the number of bulletines in the response is correct
    num_bulletin = len(gpt_response_processsed)
    assert num_bulletin <= config_dict['num_bulletins'], "number of bulletins in resnponse does not match requested number"

    # test case 3: make sure the number of words in each bulletin in the response is correct
    for bulletin in gpt_response_processsed:
        words = bulletin.split()
        cur_num_words = len(words)
        threshold = 5
        assert cur_num_words <= (config_dict['num_words'] + threshold), f"amount of words exceeded: {cur_num_words} > {config_dict['num_words'] + threshold}"
        assert (config_dict['num_words'] - threshold) <= cur_num_words, f"amount of words exceeded: {cur_num_words} < {config_dict['num_words'] - threshold}"

main_tester()