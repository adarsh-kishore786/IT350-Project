from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re 

def get_hindi_content(json_data, soup):
  content = soup.find("div", {"class": "content-area"}).text
  content = re.sub(r"\n+", "\n", content)
  content = re.sub(" +", " ", content)
  json_data["content"] = content
  return json_data

def get_kannanda_content(json_data, soup):
  content = soup.find("script", {"type": "application/ld+json"}).text 
  description_index = content.index("description") + len(r"description\":\"")
  article_index = content.index("articleBody")
  
  content = content[description_index:article_index]
  json_data["content"] = content
  return json_data

def get_json(url, lang):
  data = urlopen(url).read().decode()
  soup = BeautifulSoup(data, 'html.parser')

  json_data = {'source': url, 'language': lang}
  json_data["title"] = soup.find('title').text
  json_data["image_links"] = list(map(lambda i: i["src"], soup.find_all('img')))
    
  if lang == "hindi":
    json_data = get_hindi_content(json_data, soup)
  if lang == "kannada":
    json_data = get_kannanda_content(json_data, soup)
    
  return json_data

if __name__ == "__main__":
  url = "https://www.aajtak.in/elections/karnataka-assembly-election-2023/story/karnataka-election-bjp-candidate-ex-bbmp-commissioner-anil-kumar-koratagere-constituency-ntc-1673020-2023-04-12"
  print(json.dumps(get_json(url, "Hindi"), indent=2))