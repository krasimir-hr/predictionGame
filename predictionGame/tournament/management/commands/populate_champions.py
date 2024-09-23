import json
import os
from django.core.management.base import BaseCommand
from predictionGame.tournament.models import Champion


class Command(BaseCommand):
    help = 'Populate the champion model'

    def handle(self, *args, **kwargs):
        json_file_path = os.path.join(os.path.dirname(__file__), 'champion.json')

        with open(json_file_path, encoding='utf-8') as f:
            data = json.load(f)

        champions_data = data['data']

        for champ_id, champ_info in champions_data.items():
            Champion.objects.update_or_create(
                name=champ_info['name'],
                img=f"https://ddragon.leagueoflegends.com/cdn/14.18.1/img/champion/{champ_info['name']}.png"
            )

        self.stdout.write(self.style.SUCCESS('Champions have been populated successfully!'))