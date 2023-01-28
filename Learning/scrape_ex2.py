from bs4 import BeautifulSoup
from urllib.request import urlopen

def getHTML(url):
  data = urlopen(url)
  return data.read().decode()

def main():
  url = "http://olympus.realpython.org/profiles"
  html = getHTML(url)
  soup = BeautifulSoup(html, "html.parser")
  
  [print(link) for link in map(lambda x: "{}{}".format(url, x["href"]), soup.find_all("a"))]

if __name__ == "__main__":
  main()