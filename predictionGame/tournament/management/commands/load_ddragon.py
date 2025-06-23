import requests
from django.core.management.base import BaseCommand
from predictionGame.tournament.models import Champion, Item, Rune, SummonerSpell

DATA_DRAGON_VERSION = '15.12.1'
BASE_ICON_URL = 'https://ddragon.canisback.com/img/'
BASE_URL = f'http://ddragon.leagueoflegends.com/cdn/{DATA_DRAGON_VERSION}/data/en_US/'

class Command(BaseCommand):
   help = 'Fetch and load champions, items, runes and spells from Riot Data Dragon'

   def handle(self, *args, **kwargs):
      self.load_champions()
      self.load_items()
      self.load_runes()
      self.load_spells()

   def load_champions(self):
      url = BASE_URL + 'champion.json'
      res = requests.get(url)
      res.raise_for_status()
      data = res.json()

      for champ_key, champ_info in data['data'].items():
         name = champ_info['name']
         key = champ_info['key']
         icon = f"http://ddragon.leagueoflegends.com/cdn/{DATA_DRAGON_VERSION}/img/champion/{champ_info['image']['full']}"
         description = champ_info.get('blurb', '')

         Champion.objects.update_or_create(
               key=key,
               defaults={
                  'name': name,
                  'icon': icon,
                  'description': description,
               }
         )
      self.stdout.write(self.style.SUCCESS('Champions loaded!'))

   def load_items(self):
      url = BASE_URL + 'item.json'
      res = requests.get(url)
      res.raise_for_status()
      data = res.json()

      for item_key, item_info in data['data'].items():
         name = item_info['name']
         key = item_key
         icon = f"http://ddragon.leagueoflegends.com/cdn/{DATA_DRAGON_VERSION}/img/item/{item_info['image']['full']}"
         description = item_info.get('description', '')

         try:
            Item.objects.update_or_create(
                  item_id=key,
                  defaults={
                     'name': name,
                     'icon': icon,
                     'description': description,
                  }
            )
         except Exception as e:
            print(f"Error saving item: id={key}, name='{name}' (length: {len(name)})")
            print(f"Exception: {e}")
      self.stdout.write(self.style.SUCCESS('Items loaded!'))
           


   def load_runes(self):
      url = BASE_URL + 'runesReforged.json'
      res = requests.get(url)
      res.raise_for_status()
      data = res.json()

      for tree in data:
         path_id = str(tree['id'])
         path_name = tree['key']
         path_icon = tree['icon']

         # Save the rune tree itself
         Rune.objects.update_or_create(
            rune_id=path_id,
            defaults={
                  'name': path_name,
                  'icon': f"{BASE_ICON_URL}{path_icon}",
                  'description': '',
            }
         )

         # Keystones (first slot)
         keystones_slot = tree.get('slots', [])[0]
         for rune in keystones_slot.get('runes', []):
            rune_id = str(rune['id'])
            name = rune['name']
            icon_path = rune['icon']
            description = rune.get('longDesc') or rune.get('shortDesc') or rune.get('description') or ''

            icon_url = f"{BASE_ICON_URL}{icon_path}"

            Rune.objects.update_or_create(
                  rune_id=rune_id,
                  defaults={
                     'name': name,
                     'icon': icon_url,
                     'description': description,
                  }
            )
      self.stdout.write(self.style.SUCCESS('Runes loaded!'))



   def load_spells(self):
      url = BASE_URL + 'summoner.json'
      res = requests.get(url)
      res.raise_for_status()
      data = res.json()

      for spell_key, spell_info in data['data'].items():
         name = spell_info['name']
         key = spell_info['key']
         icon = f"http://ddragon.leagueoflegends.com/cdn/{DATA_DRAGON_VERSION}/img/spell/{spell_info['image']['full']}"
         description = spell_info.get('description', '')

         SummonerSpell.objects.update_or_create(
               spell_id=key,
               defaults={
                  'name': name,
                  'icon': icon,
                  'description': description,
               }
         )
      self.stdout.write(self.style.SUCCESS('Summoner spells loaded!'))
