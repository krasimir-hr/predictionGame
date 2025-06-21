class MatchDataFormatter:
   def __init__(self, initial_raw_data, final_raw_data):
      self.initial_raw_data = initial_raw_data
      self.final_raw_data = final_raw_data

   def parse_match_status(self):
      return self.initial_raw_data['match_status']
   
   def match_finished(self):
      if self.initial_raw_data['match_status'] == 'finished':
         return True
      return False

   def parse_timestamp(self):
      return self.initial_raw_data['timestamp']

   def parse_team_names(self):
      items = list(self.initial_raw_data.items())[1:-2]
      team_1_data = {}
      team_2_data = {}

      for key, values in items:
         team_1_data[key[:-1] if key.endswith('s') else key] = values[0]
         team_2_data[key[:-1] if key.endswith('s') else key] = values[1]
      
      return [team_1_data, team_2_data]
   
   def parse_number_of_match_tabs(self):
      return self.initial_raw_data['number_of_match_tabs']
   
   def calculate_total_games(self):
      if not self.match_finished:
         total_games = self.parse_number_of_match_tabs()
         return total_games
      raw_result = self.final_raw_data['final_result']
      total_games = 0
      for score in raw_result.split('–'):
         total_games += int(score)
      return total_games


   def structure_initial_data(self):
      status = self.parse_match_status()
      timestamp = self.parse_timestamp()
      teams = self.parse_team_names()
      total_games = self.calculate_total_games()
      return {
         'status': status,
         'timestamp': timestamp,
         'total_games': total_games,
         'teams': teams,
         }
   
   def parse_player_names(self):
      return self.final_raw_data['player_names']
   
   def parse_player_champions(self):
      return self.final_raw_data['player_champions']
   
   def parse_player_stats(self):
      return self.final_raw_data['player_stats']
   
   def structure_player_stats(self):
      raw_stats = self.parse_player_stats()
      stats = []
      while raw_stats:
         stats.append({
            'kda': raw_stats.pop(0),
            'cs': raw_stats.pop(0),
            'gold': raw_stats.pop(0),
            'dmg': raw_stats.pop(0),
            })
      return stats
   
   def parse_player_loadouts(self):
      return self.final_raw_data['player_loadout']
   
   def structure_player_loadouts(self):
      raw_loadouts = self.parse_player_loadouts()
      loadouts = []
      while raw_loadouts:
         loadouts.append({
            'primary': raw_loadouts.pop(0),
            'seconady': raw_loadouts.pop(0),
            'summoner1': raw_loadouts.pop(0),
            'summoner2': raw_loadouts.pop(0),
         })
      return loadouts
   
   def parse_player_items(self):
      return self.final_raw_data['player_items']
   
   def structure_player_items(self):
      raw_items = self.parse_player_items()
      item_sets = []

      curr_item_set = []
      while raw_items:
         curr_item_set.append(raw_items.pop(0))
         if len(curr_item_set) == 6:
            item_sets.append(curr_item_set)
            curr_item_set = []
      
      return item_sets
      
   
   def structure_players_dict(self):
      names = self.parse_player_names()
      champions = self.parse_player_champions()
      stats = self.structure_player_stats()
      loadouts = self.structure_player_loadouts()
      items = self.structure_player_items()

      players = []

      for i in range(len(names)):
         players.append({
            'name': names.pop(0),
            'champion': champions.pop(0),
            'stats': stats.pop(0),
            'loadouts': loadouts.pop(0),
            'items': items.pop(0),
         })
      return players
   
   def parse_team_stats(self):
      return self.final_raw_data['team_stats']
   
   def structure_team_stats_dict(self):
      raw_team_stats = self.parse_team_stats()
      stats = []


      stat_keys = ['kda', 'gold', 'towers', 'inhibitors', 'barons', 'dragons']
      
      while raw_team_stats:
         team1_stats = {}
         team2_stats = {}
         for key in stat_keys:
            team1_stats[key] = raw_team_stats.pop(0)
            raw_team_stats.pop(0)
            team2_stats[key] = raw_team_stats.pop(0)
         stats.append(team1_stats)
         stats.append(team2_stats)
      return stats
   
   def parse_game_results(self):
      return self.final_raw_data['game_results']
   
   def determine_game_winner(self):
      result_map = {
         'W–L': 'team 1',
         'L–W': 'team 2'
      }

      raw_results = self.parse_game_results()
      
      return [result_map.get(result, 'unknown') for result in raw_results]
   
   def parse_side_selections(self):
      return self.final_raw_data['side_selections']
   
   def structure_teams_data(self):
      all_team_stats = self.structure_team_stats_dict()
      all_players = self.structure_players_dict()
      all_side_selections = self.parse_side_selections()

      teams_data = []
      while all_team_stats:
         curr_team_data = {
            'team_stats': all_team_stats.pop(0),
            'side_selection': all_side_selections.pop(0),
            'player_stats': [all_players.pop(0) for _ in range(5)],
         }
         teams_data.append(curr_team_data)

      return teams_data
   
   def structure_game_data(self):
      all_teams = self.structure_teams_data()
      games = []

      while all_teams:
         games.append({
            'team_1': all_teams.pop(0),
            'team_2': all_teams.pop(0),
         })
      return games

      
   def structure_final_match_data(self):
      number_of_games = self.calculate_total_games()
      all_games = self.structure_game_data()

      match = {}
      for i in range(number_of_games):
         match[f'game_{i + 1}'] = all_games.pop(0)
      return match


