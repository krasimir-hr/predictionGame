from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import requests

from urllib.parse import unquote

class LogoScrapper:
   def __init__(self, abbrevation):
      self.abbrevation = abbrevation
      self.base_url = 'https://lolesports.com/en-GB/tournament/113470835034591734/overview'
      self.session = requests.Session()

   def fetch_page(self):
      try:
         response = self.session.get(self.base_url)
         response.raise_for_status()
      except requests.RequestException as e:
         print(f"Failed to retreive page: {e}")
      return BeautifulSoup(response.text, 'html.parser')
   
   def url_decoder(self, raw_url):
      url = raw_url.replace('https://am-a.akamaihd.net/image?resize=64:&f=', '') 
      return unquote(url)

   def extract_logo_urls(self):
      soup = self.fetch_page()
      logo_url = soup.find("img", alt=self.abbrevation)['src']
      logo_url = self.url_decoder(logo_url)
      return logo_url
   

scrapper = LogoScrapper('T1')

print(scrapper.extract_logo_urls())
