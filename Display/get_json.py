from urllib.request import urlopen
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import json
import re 
from nltk import sent_tokenize
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from summary import get_summary
import os

def get_hindi_content(json_data, soup):
  content = soup.find("div", {"class": "content-area"}).text
  content = re.sub(r"\n+", "\n", content)
  content = re.sub(" +", " ", content)
  # json_data["content"] = content
  sentenceList = sent_tokenize(content)
  eng_inp = ""
  # print(sentenceList)
  for sentence in sentenceList:
     hindi_text = transliterate(sentence, sanscript.ITRANS, sanscript.DEVANAGARI)
     sent_eng = GoogleTranslator(source='auto', target='en').translate(hindi_text)
    #  print(sent_eng)
     eng_inp+=sent_eng
  eng_summary = get_summary(eng_inp, 0.1)


  print(eng_summary)
  hindi_summary = GoogleTranslator(source='auto', target='hi').translate(eng_summary)
  json_data["summary"] = hindi_summary

  return json_data

def get_kannanda_content(json_data, soup):
  content = soup.find("script", {"type": "application/ld+json"}).text 
  description_index = content.index("articleBody") + len(r"articleBody\":\"")
  article_index = content.index("articleSection")
  
  content = content[description_index:article_index]
  # json_data["content"] = content
  sentenceList = sent_tokenize(content)
  # print(sentenceList[0])
  eng_inp = ""
  for sentence in sentenceList:
    kannada_text = transliterate(sentence, sanscript.ITRANS, sanscript.KANNADA)
    sent_eng = GoogleTranslator(source='auto', target='en').translate(kannada_text)
    if sent_eng == None:
      continue
    # print(sent_eng)
    eng_inp+=sent_eng
  eng_summary = get_summary(eng_inp, 0.2)

  kannada_summary = GoogleTranslator(source='auto', target='kn').translate(eng_summary)
  json_data["summary"] = kannada_summary

  return json_data

def get_telugu_content(json_data, soup):
  content = soup.find_all("div", {"class": "field"})[1].text
  content = re.sub(r"\n+", "\n", content)
  content = re.sub(" +", " ", content)
  # json_data["content"] = content
  # return json_data
  sentenceList = sent_tokenize(content)
  eng_inp = ""
  # print(sentenceList)
  for sentence in sentenceList:
     telugu_text = transliterate(sentence, sanscript.ITRANS, sanscript.TELUGU)
     sent_eng = GoogleTranslator(source='auto', target='en').translate(telugu_text)
    #  print(sent_eng)
     eng_inp+=sent_eng
  eng_summary = get_summary(eng_inp, 0.1)

  telugu_summary = GoogleTranslator(source='auto', target='te').translate(eng_summary)
  json_data["summary"] = telugu_summary

  return json_data

def get_tamil_content(json_data, soup):
  content = soup.find_all("div", {"id": "shortdiv"})[0].text
  content = re.sub(r"\n+", "\n", content)
  content = re.sub(" +", " ", content)
  # json_data["content"] = content
  # return json_data
  # sentenceList = sent_tokenize(content)
  # eng_inp = ""
  # # print(sentenceList)
  # for sentence in sentenceList:
  #    tamil_text = transliterate(sentence, sanscript.ITRANS, sanscript.TAMIL)
  #    sent_eng = GoogleTranslator(source='auto', target='en').translate(tamil_text)
  #   #  print(sent_eng)
  #    eng_inp+=sent_eng
  # eng_summary = get_summary(eng_inp, 0.1)

  # tamil_summary = GoogleTranslator(source='auto', target='ta').translate(eng_summary)
  json_data["summary"] = content

  return json_data

def get_json(url, lang):
  data = urlopen(url).read().decode()
  soup = BeautifulSoup(data, 'html.parser')

  json_data = {'source': url, 'language': lang}
  json_data["title"] = soup.find('title').text
  if lang != "tamil":
    json_data["image_links"] = list(map(lambda i: i["src"], soup.find_all('img')))
    
  if lang == "hindi":
    json_data = get_hindi_content(json_data, soup)
  if lang == "kannada":
    json_data = get_kannanda_content(json_data, soup)
  if lang == "telugu":
    json_data = get_telugu_content(json_data, soup)
  if lang == "tamil":
    json_data = get_tamil_content(json_data, soup)
    
  return json_data

if __name__ == "__main__":
  url = "https://www.aajtak.in/elections/karnataka-assembly-election-2023/story/karnataka-election-bjp-candidate-ex-bbmp-commissioner-anil-kumar-koratagere-constituency-ntc-1673020-2023-04-12"
  print(json.dumps(get_json(url, "Hindi"), indent=2))