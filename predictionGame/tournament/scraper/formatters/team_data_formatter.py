from predictionGame.tournament.scraper.scrapers.lolesports_scrapers.logo_scraper import LogoScrapper

TEAM_ABBREVIATIONS = {
    "Gen.G Esports": "GEN",
    "T1": "T1",
    "G2 Esports": "G2",
    "KOI": "MKOI",
    "Bilibili Gaming": "BLG",
    "Anyone's Legend": "AL",
    "FlyQuest": "FLY",
    "FURIA" : "FUR",
    "CTBC Flying Oyster": "CFO",
    "GAM Esports": "GAM",
}

class TournamentDataFormatter:
   def __init__(self, raw_data):
      self.raw_data = raw_data

   def parse_team_names(self):
      return self.raw_data['teams']
   
   def parse_player_names(self):
      return self.raw_data['players']
   
   def parse_match_urls(self):
      return self.raw_data['match_urls']
   
   def get_team_abbreviation(self, team_name):
      return TEAM_ABBREVIATIONS.get(team_name, team_name[:3].upper())
   
   def get_team_logo(self, abbr):
      logo_scrapper = LogoScrapper(abbr)
      return logo_scrapper.extract_logo_urls()
   
   def get_player_picture(self, name):
      return f'https://dpm.lol/esport/players/{name}.webp'
   
   def structure_player_profile(self):
      all_players = self.parse_player_names()
      players = []
      
      while all_players:
         player_name = all_players.pop(0)
         player = {
            'name': player_name,
            'photo_url': self.get_player_picture(player_name)
         }
         players.append(player)
      return players
   
   def structure_team_dict(self):
      all_teams = self.parse_team_names()
      all_players = self.structure_player_profile()

      teams = {}

      for team in all_teams:
         abbr = self.get_team_abbreviation(team)
         teams[team] = {
            'roster': [all_players.pop(0) for _ in range(5)],
            'abbreviation': abbr,
            'logo_url': self.get_team_logo(abbr)
            }
      return teams
   
   def structure_data(self):
      teams = self.structure_team_dict()
      return teams