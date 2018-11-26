import argparse
import os

from api import api_request
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDb_API_KEY")


def get_movie_info(film_title):
    method = 'GET'
    url = 'http://www.omdbapi.com/'
    params = {
        'apikey': API_KEY,
        't': film_title
    }
    try:
        response = api_request(method=method, url=url, params=params)
        if response.status_code == 200:
            return response.json()
    except Exception as ex:
        return ex


def parse_film_info(film_dict):
    if film_dict.get('Response') == 'True':
        title = film_dict.get('Title')
        year = film_dict.get('Year')
        runtime = film_dict.get('Runtime')
        genre = film_dict.get('Genre')
        director = film_dict.get('Director')
        actors = film_dict.get('Actors')
        plot = film_dict.get('Plot')
        ratings = film_dict.get('Ratings')
        try:
            rotten_tomatoes_score = ratings[1]['Value']
        except IndexError:
            rotten_tomatoes_score = "n/a"
        try:
            metacritic_score = film_dict.get('Ratings')[2]['Value']
        except IndexError:
            metacritic_score = "n/a"
        film_print_stdout(title, year, runtime, rotten_tomatoes_score,
                           metacritic_score, genre, director, actors, plot)
    else:
        print("Oops, can't find that film title.")


def film_print_stdout(title, year, runtime, rotten_tomatoes_score,
                      metacritic_score, genre, director, actors, plot):
    print('==================================================')
    print(f"Title: {title}")
    print(f"Year: {year}")
    print(f"Runtime: {runtime}")
    print(f"Rotten Tomatoes: {rotten_tomatoes_score}")
    print(f"Metacritic: {metacritic_score}")
    print(f"Genre: {genre}")
    print(f"Director: {director}")
    print(f"Actors: {actors}")
    print(f"Plot: {plot}")
    print('==================================================')


def cli():
    parser = argparse.ArgumentParser(description="Parse film title from user")
    parser.add_argument("film_title")
    args = parser.parse_args()
    film_title = args.film_title
    response = get_movie_info(film_title)
    parse_film_info(response)


if __name__ == '__main__':
    cli()
