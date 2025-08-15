import requests
import imdb
import exceptions



class IMDBManager:
    def __init__(self): 
        self.ia = imdb.Cinemagoer()
    
    def find_films(self, movie_name: str) -> list[imdb.Movie.Movie]:
        return self.ia.search_movie(movie_name)
