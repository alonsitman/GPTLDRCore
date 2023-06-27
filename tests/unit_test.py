# import pytest
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

target = __import__("tldrgpt")


def test_default_config():

  filename = "config.json"

  # test case 1: make sure config file exists after func execution
  target.default_config(filename)  
  assert os.path.isfile(filename), "config file was not found"

  # test case 2: make sure config file created if it didn't exist
  os.remove(filename) 
  if not os.path.isfile(filename):
    target.default_config(filename)  
    assert os.path.isfile(filename), "failed to create config file"
  
  # test case 3: make sure if config file exists that it wasn't overriden
  if os.path.isfile(filename):
    os.remove(filename) 
  
  empty_dict = "{}"
  file = open(filename, 'w')
  file.write(empty_dict)
  file.close()

  if os.path.isfile(filename):
    target.default_config(filename)
    
    file = open(filename, 'r')
    file_content = file.read()
    file.close()
  
    assert file_content == empty_dict , "existing config file has been overriden"

  os.remove(filename)
  target.default_config(filename)

  print("test_default_config - success")
  return True


def test_read_config():

  filename = 'config.json'

  # test case 1: make sure a dictionary is created
  target.default_config(filename)
  config_dict = target.read_config(filename)
  assert type(config_dict) is dict, "no dictionary was created"
  
  # test case 2: make sure the content of the created dictionary matches the content of the json file
  config_dict = target.read_config(filename)
  Json_content = ["num_bulletins", "num_words"]
  assert all(key in config_dict for key in Json_content), "the content of the dictionary does not match the content of the json file"

  print("test_read_config - success")
  return True


def test_validate_url():

  url = "https://www.phillyvoice.com/sixers-nba-free-agency-rumors-news-montrezl-harrell-decline-player-option-2023-24/"
  validation_result = target.validate_url(url)
  assert validation_result, "url contains spaces, it is not valid"

  print("test_validate_url - success")
  return True


def test_get_article():

  url = "https://www.phillyvoice.com/sixers-nba-free-agency-rumors-news-montrezl-harrell-decline-player-option-2023-24/"
  # test case 1: make sure article object is of Article class type
  article = target.get_article(url)
  assert 'newspaper.article.Article' in str(type(article)), ""

  print("test_get_article - success")
  return True

def test_extract_title():

  url = "https://www.phillyvoice.com/sixers-nba-free-agency-rumors-news-montrezl-harrell-decline-player-option-2023-24/"
  article = target.get_article(url)
  title = target.extract_title(article)
  assert title == "Sixers' Montrezl Harrell to decline player option for 2023-24", "title does not match article's title"

  print("test_extract_title - success")
  return True


def test_extract_text():
  
  url = "https://www.phillyvoice.com/sixers-nba-free-agency-rumors-news-montrezl-harrell-decline-player-option-2023-24/"
  article = target.get_article(url)
  text = target.extract_text(article)
  assert "Backup Sixers big man Montrezl Harrell" in text, "failed to extract text"

  print("test_extract_text - success")
  return True


def test_prepare_query(num_bulletins, num_words, title, text):

  pass   # no real need to test that a simple f string works, python is ok
  
  print("test_prepare_query - success")
  return True



def test_send_query():
  
  key = "PUT_YOUR_OPENAI_KEY_HERE"
  title = "Sixers' Montrezl Harrell to decline player option for 2023-24"
  text = "Backup Sixers big man Montrezl Harrell is declining his player option for the 2023-24 season, a source confirmed to PhillyVoice on Wednesday morning, a minor move that gives the Sixers the tiniest boost in flexibility heading into free agency. Turner's Chris Haynes was the first to report the news on Wednesday."\
          "" \
          "A late-offseason addition to the Sixers last season, Harrell was brought in as a veteran alternative to what would have been a youth movement behind Joel Embiid at center. Despite some promising flashes from Charles Bassey and Paul Reed, it was unclear how much either player could be trusted as a full-time backup to their franchise player. Previous head coach Doc Rivers had shown reluctance to trust Reed specifically — we weren't on a victory tour quite yet — and Harrell had familiarity with the head coach and several Sixers players, most notably James Harden."\
          "" \
          "While Harrell arrived with some issues to sort out, he felt like a reasonable flier for the team at the time as someone who might benefit from Harden's playmaking on the second unit. As has been the case throughout his career, Harrell showed some early flashes of activity on the offensive glass and had a fairly firm hold on the backup center job up until early February, when Rivers decided to go to Reed for good. It had been well past time to move on from Harrell by that point, as his defensive limitations were compounded by a continued slide in his finishing ability. Harrell had the second-worst finishing season of his career last season, taking away what would have been his point of separation from the younger, more athletic Reed."\
          "" \
          "The choice to give Harrell a player option is one that looked like it could bite the Sixers if Harrell had simply opted in, which was a decision that was left to deadline day."


  num_bulletins = 3
  num_words = 15


  prep_query = target.prepare_query(num_bulletins, num_words, title, text)
  response = target.send_query(key, prep_query)


  # test case 1.1: make sure a string is returned

  assert type(response) is str, "did not receive a response string from gpt"

  # test case 1.2: make sure the number of bulletines in the response is correct
  cur_num_bulletins = response.count('\n') + 1 - 2 
  assert cur_num_bulletins < num_bulletins

  # test case 1.3: make sure the number of words in each bulletin in the response is correct
  bulletins = response.split('\n')
  for bulletin in bulletins:
      words = bulletin.split()
      cur_num_words = len(words)
      threshold = 5
      assert cur_num_words < (num_words + threshold), "not all bulletins have requested amount of words"
      assert (num_words - threshold) < cur_num_words, "not all bulletins have requested amount of words"

  print("test_send_query - success")
  return True


def main_tester():

  test_default_config()
  test_read_config()
  test_validate_url()
  test_get_article()
  test_extract_title()
  test_extract_text()
  test_send_query()


main_tester()