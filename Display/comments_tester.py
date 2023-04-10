from utility import CommentScraper
from instagrapi import Client
from dotenv import load_dotenv  
import os

def main():
  load_dotenv()
  baseUrl = "https://www.instagram.com/"
  url = "p/CjI2UgUJZMBj3JqdXLDosPYqyx_Mw742hKEPBc0/"
  
  INSTA_USERNAME = os.environ.get('INSTA_USERNAME')
  INSTA_PASSWORD = os.environ.get('INSTA_PASSWORD')
  
  # scraper = CommentScraper(baseUrl, url)
  # print(scraper.soup.find("title"))
  cl = Client()
  cl.login(INSTA_USERNAME, INSTA_PASSWORD)
  
  media_id = cl.media_id(cl.media_pk_from_url(baseUrl+url))
  
  comments = cl.media_comments(media_id)
  
  for c in comments:
    print(type(c))

if __name__ == "__main__":
  main()