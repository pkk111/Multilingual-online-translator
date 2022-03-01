import sys
import requests
from bs4 import BeautifulSoup

languages = ['all',
             'arabic',
             'german',
             'english',
             'spanish',
             'french',
             'hebrew',
             'japanese',
             'dutch',
             'polish',
             'portuguese',
             'romanian',
             'russian',
             'turkish']
required_translations = 1
session = requests.Session()


def input_lang():
    args = sys.argv
    if len(args) > 2:
        from_language = args[1]
        to_language = args[2]
        word = args[3]
        if from_language in languages:
            if to_language in languages:
                save_results(from_language, to_language, word)
            else:
                raise Exception("Sorry, the program doesn't support {}".format(to_language))
        else:
            raise Exception("Sorry, the program doesn't support {}".format(from_language))
    else:
        print(args)
        raise IndexError


def make_request(from_language, to_language, word):
    url = f"https://context.reverso.net/translation/{from_language}-{to_language}/{word}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        page = session.get(url, headers=headers)
    except Exception:
        raise Exception("Something wrong with your internet connection")

    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        words = [element.text.strip() for element in soup.find('div', id='translations-content').find_all('a')]
        examples = [element.text.strip() for element in
                    soup.find('section', id="examples-content").find_all('span', class_="text")]
    except Exception:
        raise Exception(f"Sorry, unable to find {word}")
    words = [words[i] for i in range(min(required_translations, len(words)))]
    examples = [examples[i] for i in range(min(2 * required_translations, len(examples)))]
    language_translation = f"\n\n{to_language.capitalize()} Translations:\n"
    translation = "\n".join(words)
    language_example_translation = f"\n\n{to_language.capitalize()} Examples:\n"
    example_translation = "\n".join(examples)
    return language_translation + translation + language_example_translation + example_translation


def save_results(from_language, to_language, word):
    with open(f'{word}.txt', 'w', encoding="utf-8") as file:
        output = ""
        if to_language == 'all':
            for i in range(1, len(languages)):
                output += make_request(from_language, languages[i], word) if languages[i] != from_language else ""
        else:
            output += make_request(from_language, to_language, word)
        file.write(output)
        print(output)
        file.close()


try:
    input_lang()
except Exception as e:
    print(e)
