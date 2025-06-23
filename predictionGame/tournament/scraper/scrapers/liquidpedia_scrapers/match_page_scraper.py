from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import requests

from urllib.parse import urljoin


class MatchPageScraper:
   def __init__(self, url):
      self.base_url = 'https://liquipedia.net'
      self.url = url
      self.session = requests.Session()

   def fetch_page(self):
      try:
         full_url = urljoin(self.base_url, self.url)
         response = self.session.get(full_url)
         response.raise_for_status()
      except requests.RequestException as e:
         print(f"Failed to retreive page: {e}")
      return BeautifulSoup(response.text, 'html.parser')
   
   def can_extract_initial_data(self, soup) -> bool:
      """
      Return True if the soup contains the required match data elements.
      """
      proof = soup.select('div.match-bm-match-header-team-group')
      return bool(proof)
   
   def extract_match_status(self, soup):
      match_status_element = soup.select('div.match-bm-match-header-result-text')
      return match_status_element[0].get_text(strip=True)
   
   def extract_number_of_match_tabs(self, soup):
      if soup.select('li.tab5'):
         return 5
      elif soup.select('li.tab3'):
         return 3
      else:
         return 1
      
   def extract_full_team_names(self, soup):
      """
      Extracts and returns a list of team names from the page soup, only if the initial data can be extracted.
      """ 
      if not self.can_extract_initial_data(soup):
         return []
      
      full_name_elements = soup.select('div.match-bm-match-header-team-long > a')
      return [team.get_text(strip=True) for team in full_name_elements]
   
   def extract_short_team_names(self, soup):
      if not self.can_extract_initial_data(soup):
         return []
      
      short_name_elements = soup.select('div.match-bm-match-header-team-short > a')
      return [team.get_text(strip=True) for team in short_name_elements]
   
   def extract_match_start_time(self, soup):
      time_element = soup.select_one('span.timer-object')
      if time_element and 'data-timestamp' in time_element.attrs:
        return time_element['data-timestamp']
      else:
        return None
   
   def fetch_initial_data(self):
      soup = self.fetch_page()
      match_status = self.extract_match_status(soup)
      full_names = self.extract_full_team_names(soup)
      short_names = self.extract_short_team_names(soup)
      timestamp = self.extract_match_start_time(soup)
      if not timestamp:
         timestamp = None
      number_of_match_tabs = self.extract_number_of_match_tabs(soup)

      return {
         'match_status': match_status,
         'full_names': full_names, 
         'short_names': short_names, 
         'timestamp': timestamp,
         'number_of_match_tabs': number_of_match_tabs,
         }
   
   def extract_player_names(self, soup):
      player_name_elements = soup.select('div.match-bm-players-player-name > a')
      return [player.get_text(strip=True) for player in player_name_elements]
   
   def extract_player_champions(self, soup):
      player_champion_elements = soup.select('div.match-bm-players-player-name > i')
      return [champion.get_text(strip=True) for champion in player_champion_elements]
   
   def extract_player_stats(self, soup):
      player_stat_elements = soup.select('div.match-bm-players-player-stat-data')
      return [score.get_text(strip=True) for score in player_stat_elements]
   
   def extract_player_loadouts(self, soup):
      player_loadout_elements = soup.select('div.match-bm-lol-players-player-loadout-rs > img')
      return [loadout['title'] for loadout in player_loadout_elements]
   
   def extract_player_items(self, soup):
      player_item_elements = soup.select('div.match-bm-lol-players-player-loadout-item > img')
      return [item['title'] for item in player_item_elements]
   
   def extract_team_stats(self, soup):
      team_stat_elements = soup.select('div.match-bm-team-stats-list-cell')
      return [team_stat.get_text(strip=True) for team_stat in team_stat_elements if team_stat.get_text(strip=True)]
   
   def extract_game_results(self, soup):
      game_result_elements = soup.select('div.match-bm-lol-game-summary-score')
      return [game_result.get_text(strip=True) for game_result in game_result_elements]
   
   def extract_side_selections(self, soup):
      side_selection_elements = soup.select('div.match-bm-lol-game-summary-faction > img')
      return [side['alt'] for side in side_selection_elements]
   
   def extract_final_results(self, soup):
      result_element = soup.select_one('div.match-bm-match-header-result')
      return ''.join(result_element.find_all(string=True, recursive=False)).strip()
   
   def extract_bans(self, soup):
      ban_elements = soup.select('div.match-bm-game-veto-overview-team-veto-row.match-bm-game-veto-overview-team-veto-row--ban > div.match-bm-game-veto-overview-team-veto-row-item > div.match-bm-game-veto-overview-team-veto-row-item-icon > a')
      clean_ban_elements = []
      for i in range(0, len(ban_elements), 20):
         clean_ban_elements.extend(ban_elements[i:i+10])
   
      return [ban['title'] for ban in clean_ban_elements]
   
   def extract_games_length(self, soup):
      length_elements = soup.select('div.match-bm-lol-game-summary-length')
      return [game_length.get_text(strip=True) for game_length in length_elements]
     
   def fetch_finished_data(self):
      soup = self.fetch_page()

      match_status = self.extract_match_status(soup)

      if not match_status == 'finished':
         return

      player_names = self.extract_player_names(soup)
      player_champions = self.extract_player_champions(soup)
      player_stats = self.extract_player_stats(soup)
      player_loadouts = self.extract_player_loadouts(soup)
      player_items = self.extract_player_items(soup)

      team_stats = self.extract_team_stats(soup)

      final_result = self.extract_final_results(soup)
      game_results = self.extract_game_results(soup)
      side_selections = self.extract_side_selections(soup)

      bans = self.extract_bans(soup)
      lengths = self.extract_games_length(soup)

      return {
         'player_names': player_names, 
         'player_champions': player_champions,
         'player_stats': player_stats, 
         'player_loadout': player_loadouts, 
         'player_items': player_items,
         'team_stats': team_stats,
         'final_result': final_result,
         'game_results': game_results,
         'side_selections': side_selections,
         'bans': bans,
         'lengths': lengths,
         }
