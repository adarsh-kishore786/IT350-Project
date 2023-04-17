from instagrapi import Client
from dotenv import load_dotenv  
import os

load_dotenv()

def get_comments(url):
  load_dotenv()
  baseUrl = "https://www.instagram.com/"
  
  INSTA_USERNAME = os.environ.get('INSTA_USERNAME')
  INSTA_PASSWORD = os.environ.get('INSTA_PASSWORD')
  
  cl = Client()
  cl.login(INSTA_USERNAME, INSTA_PASSWORD)
  
  media_id = cl.media_id(cl.media_pk_from_url(baseUrl+url))
  
  return cl.media_comments(media_id, 20)

def main():
  comments = get_comments("p/Cqzy-IOrTyD")
  
  # scraper = CommentScraper(baseUrl, url)
  # print(scraper.soup.find("title"))
  
  # for c in comments:
  #   print(vars(c)["text"])
  #   print()

if __name__ == "__main__":
  main()