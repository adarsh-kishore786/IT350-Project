from urllib.request import urlopen
from bs4 import BeautifulSoup

class NewsScraper:
  def __init__(self, baseUrl, url=""):
    self.baseUrl = baseUrl
    self.soup = BeautifulSoup(self._getHTML(url), 'html.parser') 
    
  def getDataByTag(self, tag):
    data = self.soup.find_all(tag)
    return data 

  def getTextByTag(self, tag):
    return [d.text for d in self.getDataByTag(tag)]

  def getTitle(self):
    return self.getTextByTag("title")[0]

  def getHeadingsWithLinks(self):
    data = self.getDataByTag("a")
    data = list(filter(lambda d: "href" in d.attrs and self.baseUrl in d["href"], data))
    return { d.text : (self.baseUrl if not d["href"].startswith("http") else "") + d["href"] for d in data }
  
  def _getHTML(self, url):
    data = urlopen(self.baseUrl + url)
    return data.read().decode()
  
  def _separateDomain(self, fullUrl):
    try:
      index_ = fullUrl.index("/", 10)
      return (fullUrl[:index_], fullUrl[index_:])
    except ValueError:
      return fullUrl
    
  def crawlSoups(self):
    titlesAndLinks = self.getHeadingsWithLinks()
    res = []
    for (_, link) in titlesAndLinks.items():
      try:
        baseUrl, url = self._separateDomain(link)
        if '/' in url[1:]:
          continue 
        if baseUrl != self.baseUrl:
          continue
        print(baseUrl, url)
        res.append(NewsScraper(baseUrl, url))
      except:
        continue
    return res
    
  def changeUrl(self, newBaseUrl, newUrl=""):
    self.baseUrl = newBaseUrl
    self.soup = BeautifulSoup(self.getHTML(newUrl), 'html.parser')
    
  def __str__(self):
    try:
      return self.getTitle()
    except:
      return ""