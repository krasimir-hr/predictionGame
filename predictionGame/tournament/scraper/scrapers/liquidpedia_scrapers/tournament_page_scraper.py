from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import requests

class TournamentPageScraper:
   """
   Scrapes teams, players and match URLs from a Liquidpedia tournament page.
   """

   def __init__(self, base_url):
      """
      Initialize the scraper with a base URL.
      """
      self.base_url = base_url
      self.session = requests.Session()

   def fetch_page(self) -> Optional[BeautifulSoup]:
      """
      Fetch and parse the HTML content of the tournament page.

      Returns:
         BeautifulSoup: Parsed HTML of the page, or None on request failure.
      """
      try:
         response = self.session.get(self.base_url)
         response.raise_for_status()
      except requests.RequestException as e:
         print(f"Failed to retreive page: {e}")
      return BeautifulSoup(response.text, 'html.parser') 

   def extract_teams(self, soup) -> List[str]:
      """
      Extract team names from the parsed page.

      Args:
         soup (BeautifulSoup): Parsed HTML content.

      Returns:
         list[str]: A list of team names.
      """
      team_elements = soup.select('div.teamcard > center > a')
      return [team.get_text(strip=True) for team in team_elements]
   
   def extract_players(self, soup) -> List[str]:
      """
      Extract player names from the parsed page.

      Args:
         soup (BeautifulSoup): Parsed HTML content.

      Returns:
         list[str]: A list of player names.
      """
      player_elements = soup.select('[data-toggle-area-content="1"] > tbody > tr > td > a')
      return [player.get_text(strip=True) for player in player_elements]
   
   def extract_match_urls(self, soup) -> List[str]:
      """
      Extract match URLs from the parsed page.

      Args:
         soup (BeautifulSoup): Parsed HTML content.

      Returns:
         list[str]: A list of match URL paths.
      """
      match_url_elements = soup.select('div.brkts-match-info-popup > div.brkts-popup-body-element > center > div > a')
      return [match_url['href'] for match_url in match_url_elements]
   
   def fetch_all(self) -> Dict[str, List[str]]:
      """
      Perform a full scrape of the tournament page.

      Returns:
         dict: A dictionary containing lists of teams, players, and match URLs.
      """
      soup = self.fetch_page()
      teams = self.extract_teams(soup)
      players = self.extract_players(soup)
      match_urls = self.extract_match_urls(soup)
      return {'teams': teams, 'players': players, 'match_urls': match_urls}