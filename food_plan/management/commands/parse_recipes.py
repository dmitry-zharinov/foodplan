from django.core.management.base import BaseCommand
from food_plan.models import Recipe, Ingredient
import requests
from bs4 import BeautifulSoup
import time
import urllib.request


class Command(BaseCommand):
    help = 'Parse recipe'

    def handle(self, *args, **options):
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
                self.stdout.write(f"Going thru {recipe_url}")
                recipe_response = requests.get(recipe_url, headers=headers)
                recipe_bs = BeautifulSoup(recipe_response.text, 'html.parser')
                self.stdout.write("Scraped")
                recipe_portions = recipe_bs.find(
                    "input", {"class": "field__input"})['value']
                recipe_name = recipe_bs.find(
                    "h1", {"class": "recipe-header__name"}).text
                recipe_calories = recipe_bs.find(
                    "div", {"class": "kkal-meter__value"}).text

                recipe_instruction = recipe_bs.find_all(
                    "div", {"class": "plain-text recipe_step_text"})

                recipe_instruction = ' '.join(
                    [step.text for step in recipe_instruction])
                try:
                    recipe_description = recipe_bs.find(
                        "div", {"class": "recipe_description"}).text
                except AttributeError:
                    recipe_description = 'Нет описания'
                try:
                    recipe_image_url = recipe_bs.find(
                        "div", {"class": "content-media"}).find("img")['src']
                    recipe_image = recipe_image_url.split('/')[-1]
                    recipe_image = recipe_image.split('?')[0]
                    urllib.request.urlretrieve(
                        recipe_image_url, f'media/recipes/{recipe_image}')
                    self.stdout.write("Image saved!")
                except TypeError:
                    recipe_image = 'default.jpg'
                recipe_ingridients = recipe_bs.find(
                    "div", {"id": "recipe_ingredients_block"}).find_all(
                    "table", {"class": "definition-list-table"})
                recipe = Recipe(
                    title=recipe_name,
                    description=recipe_description,
                    instructions=recipe_instruction,
                    image=recipe_image,
                    portions=recipe_portions,
                    calories=int(recipe_calories),
                )
                recipe.save()
                self.stdout.write("Recipe saved.")

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

                    ingredient = Ingredient(
                        amount=ingridient_amount,
                        title=ingridient_name,
                        unit=ingridient_unit,
                        recipe=recipe

                    )
                    ingredient.save()
                    self.stdout.write("Ingredient saved.")
