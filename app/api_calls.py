import requests

api_key = "YOUR API KEY"
base_url = "https://api.themoviedb.org/3/{}"

def get_by_category(category):
    url = base_url.format(category)  # Format the base URL with the category
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None  # Handle errors as needed
    
def search_tv(query):
    search_url = "https://api.themoviedb.org/3/search/tv?api_key={}&query={}".format(api_key,query)
    data = requests.get(search_url).json()
    return data

def search_movie(query):
    search_url = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(api_key,query)
    data = requests.get(search_url).json()
    return data

def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def get_tv_show_details(tv_id):
    url = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    return data








