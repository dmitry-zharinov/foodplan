from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll
import requests
from bs4 import BeautifulSoup
import time


class Command(BaseCommand):
    help = 'Parse recipe'

    def handle(self, *args, **options):
        pass

    def get_recipes(self):
        recipes_collection = []
        headers = {'User-Agent': 'Chrome/51.0.2704.64 Safari/537.36'}
        urls = [
            f'https://www.edimdoma.ru/retsepty?page={n}' for n in range(1, 5)]
        for url in urls:
            time.sleep(5)
            self.stdout.write(self.style.WARNING("Going thru pages"))
            res = requests.get(url, headers=headers)
            bs = BeautifulSoup(res.text, 'html.parser')
            recipes_urls = bs.find_all("div", {"class": "card__description"})
            for recipe_url in recipes_urls:

                time.sleep(5)
                recipe_href = recipe_url.find("a")["href"]
                recipe_url = f'https://www.edimdoma.ru{recipe_href}'
                self.stdout.write(self.style.WARNING("Going thru recipes"))
                recipe_response = requests.get(recipe_url, headers=headers)
                recipe_bs = BeautifulSoup(recipe_response.text, 'html.parser')

                recipe_portions = recipe_bs.find(
                    "input", {"class": "field__input"})['value']
                recipe_name = recipe_bs.find(
                    "h1", {"class": "recipe-header__name"}).text
                recipe_instruction = recipe_bs.find(
                    "div", {"class": "recipe_description"}).text
                recipe_ingridients = recipe_bs.find(
                    "div", {"id": "recipe_ingredients_block"}).find_all(
                    "table", {"class": "definition-list-table"})

                full_recipe = {
                    'recipe_name': recipe_name,
                    'recipe_portions': recipe_portions,
                    'recipe_instruction': recipe_instruction
                }

                ingridient = []
                for recipe_ingridient in recipe_ingridients:
                    ingridient_name = recipe_ingridient.find(
                        "input",
                        {"class": "checkbox__input recipe_ingredient_checkbox"}
                    )['data-intredient-title']
                    ingridient_amount = recipe_ingridient.find(
                        "input",
                        {"class": "checkbox__input recipe_ingredient_checkbox"}
                    )['data-amount']
                    ingridient_unit = recipe_ingridient.find(
                        "input",
                        {"class": "checkbox__input recipe_ingredient_checkbox"}
                    )['data-unit-title']
                    ingridient.append({
                        'ingridient_name': ingridient_name,
                        'ingridient_amount': ingridient_amount,
                        'ingridient_unit': ingridient_unit}
                    )

                full_recipe['ingridients'] = ingridient
                recipes_collection.append(full_recipe)
        return recipes_collection
