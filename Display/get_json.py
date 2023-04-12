from urllib.request import urlopen
from bs4 import BeautifulSoup
import json 

def get_json(url, lang):
  print(url)
  data = urlopen(url).read().decode()
  soup = BeautifulSoup(data, 'html.parser')

  json_data = {'source': url, 'language': lang}
  json_data["title"] = soup.find('title').text
  json_data["image_links"] = list(map(lambda i: i["src"], soup.find_all('img')))
    
  print(json_data)
  return json_data

if __name__ == "__main__":
  url = "https://www.aajtak.in/elections/karnataka-assembly-election-2023/story/karnataka-election-bjp-candidate-ex-bbmp-commissioner-anil-kumar-koratagere-constituency-ntc-1673020-2023-04-12"
  print(get_json(url, "Hindi"))