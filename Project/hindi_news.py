from bs4 import BeautifulSoup
import utility 

def getSoup(url):
  data = utility.getHTML(url)
  
  soup = BeautifulSoup(data, 'html.parser')
  return soup
  
def getTitle(soup):
  text = soup.find("title")
  return text.text

def main():
  url = "https://www.bhaskar.com/international/news/pakistan-saudi-arabia-loan-shahbaz-sharif-video-goes-viral-130834381.html"
  soup = getSoup(url)
  
  print(getTitle(soup))
  
if __name__ == "__main__":
  main()
