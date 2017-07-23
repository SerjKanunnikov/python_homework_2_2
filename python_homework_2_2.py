import json
import yaml
import re
from pprint import pprint


def import_cookbook():
    """импорт рецептов из текстового файла"""
    cook_book = {}
    dish_list = []  # список блюд
    ingredients_list = []  # список ингридиентов
    dish_number = 0  # номер блюда для использования в списке
    ingredient_stats = ["ingredient_name", "quantity", "measure"]  # свойства ингридиента
    ingredients_count = 0  # счетчик ингредиентов
    left_index = 0  # левая граница для перебора списка ингредиентов
    ingredients_count_list = []
    with open(file="recipes.txt") as f:
        for line in f:
            if re.match('^[а-яА-Я]\D*$', line):  # регулярка для поиска названий блюд
                dish_list.append(line.split(' ', 1)[0].strip())  # создание списка блюд
                left_index += ingredients_count
            if re.match('^\d$', line):  # регулярка для поиска количества ингредиентов
                ingredients_count = int(line)
                dish_number += 1  # номер блюда из списка
                ingredients_count_list.append(ingredients_count)
            if re.match('^[а-яА-Я]*\s\|\s\d*\s\|\s[а-яА-Я]*$', line):  # регулярка для поиска строки со свойствами ингредиента
                dish_ingredients_list = line.strip().split(" | ")
                ingredients_list.append(dict(zip(ingredient_stats, dish_ingredients_list)))  # список словарей ингредиентов
                cook_book.update({dish_list[dish_number-1]: ingredients_list[left_index:left_index+ingredients_count]})
    return cook_book


def convert_json_cook_book(cook_book):
    """конвертация рецептов в json-файл"""
    with open("cook_book.json", "w") as f:
        json.dump(cook_book, f, ensure_ascii=False)
        pprint.pprint(f)


def load_json_cook_book():
    """загрузка рецептов из json-файла"""
    with open("cook_book.json", "r") as f:
        cook_book = json.load(f)
        cook_book.update(cook_book)
        return cook_book


def convert_yaml_cook_book(cook_book):
    """конвертация рецептов в yaml-файл"""
    with open("cook_book.yaml", "w") as f:
        yaml.safe_dump(cook_book, f, encoding='utf-8', allow_unicode=True)


def load_yaml_cook_book():
    """загрузка рецептов из yaml-файла"""
    with open("cook_book.yaml", "r") as f:
        cook_book = yaml.load(f)
        cook_book.update(cook_book)
        return cook_book


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}
    for dish in dishes:
        for ingredient in cook_book[dish]:
            new_shop_list_item = dict(ingredient)
            new_shop_list_item['quantity'] = int(new_shop_list_item['quantity']) * person_count
            if new_shop_list_item['ingredient_name'] not in shop_list:
                shop_list[new_shop_list_item['ingredient_name']] = new_shop_list_item
            else:
                shop_list[new_shop_list_item['ingredient_name']]['quantity'] += new_shop_list_item['quantity']
    return shop_list


def print_shop_list(shop_list):
    for shop_list_item in shop_list.values():
        print('{} {} {}'.format(shop_list_item['ingredient_name'], shop_list_item['quantity'], shop_list_item['measure']))


def create_shop_list(cook_book):
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую): ').lower().split(', ')
    shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
    print_shop_list(shop_list)


def main():
    command = input("Выберите способ импорта:\n"
          "1. JSON\n"
          "2. YAML\n")
    if command == "1":
        create_shop_list(load_json_cook_book())
    elif command == "2":
        create_shop_list(load_yaml_cook_book())

main()