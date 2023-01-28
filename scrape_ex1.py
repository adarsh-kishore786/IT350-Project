import re
from urllib.request import urlopen

def getHTML(url):
  data = urlopen(url)
  return data.read().decode()

def getName(html):
  start_index = html.find("<h2>") + len("<h2>")
  end_index = html.find("</h2>")
  return html[start_index:end_index]

def getColor(html):
  start_index = html.find("Color") - len("Favorite ")
  end_index = html.find("\n</center>")
  return html[start_index:end_index]

def main():
  url = "http://olympus.realpython.org/profiles/dionysus"
  html = getHTML(url)
  
  print(html)
  print("-----")
  print(getName(html))
  print(getColor(html))
  
if __name__ == "__main__":
  main()