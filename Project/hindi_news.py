from utility import NewsScraper 

def main():
  baseUrl = "https://www.aajtak.in" # "https://www.bhaskar.com"
  scraper = NewsScraper(baseUrl)
  
  print(scraper.getTitle())
  [print(s) for s in scraper.crawlSoups()]
  
if __name__ == "__main__":
  main()
