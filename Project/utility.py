from urllib.request import urlopen

def getHTML(url):
  data = urlopen(url)
  return data.read().decode()