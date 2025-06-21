from scrapers.liquidpedia_scrapers.match_page_scraper import MatchPageScraper
from scrapers.liquidpedia_scrapers.tournament_page_scraper import TournamentPageScraper

from formatters.match_data_formatter import MatchDataFormatter
from formatters.team_data_formatter import TournamentDataFormatter

import json

tournament_scraper = TournamentPageScraper('https://liquipedia.net/leagueoflegends/Mid-Season_Invitational/2025')
tournament_raw_data = tournament_scraper.fetch_all()

tournament_formatter = TournamentDataFormatter(tournament_raw_data)

match_scraper = MatchPageScraper('/leagueoflegends/Match:ID_LCKRtMSI25_R04-M001')
initial_raw_data = match_scraper.fetch_initial_data()
finished_raw_data = match_scraper.fetch_finished_data()

match_formatter = MatchDataFormatter(initial_raw_data, finished_raw_data)

with open('tournament_data.json', 'w') as f:
   json.dump(tournament_formatter.structure_data(), f, indent=2)