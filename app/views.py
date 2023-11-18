from app import app
from app.api_calls import get_by_category, search_movie, search_tv

from flask import render_template, request

@app.route("/")
def index():
    
    trending_now = get_by_category("trending/all/week")
    return render_template("index.html", trending_now=trending_now['results'])

@app.route("/movies")
def movies():
    
    popular_movies = get_by_category("movie/popular")
    upcoming_movies = get_by_category("movie/upcoming")
    now_playing_movies = get_by_category("movie/now_playing")
    
    return render_template("movie.html", popular_movies=popular_movies['results'], 
                           upcoming_movies=upcoming_movies['results'], 
                           now_playing_movies=now_playing_movies['results'])
    
@app.route("/tv")
def tv():
    
    popular_tv = get_by_category("tv/popular")
    top_rating = get_by_category("tv/top_rated")
    on_the_air = get_by_category("tv/on_the_air")
    
    return render_template("tv.html", popular_tv=popular_tv['results'],
                        top_rating=top_rating['results'],
                        on_the_air=on_the_air['results'])
    
@app.route('/search')
def results(): 
    query = request.args.get('query')  
    name_list = query.split(" ")
    name_format = "+".join(name_list)
    searched_movies = search_movie(name_format)
    searched_tv = search_tv(name_format)
    title = query
    
    return render_template("search.html",title=title, m_results=searched_movies['results'], tv_results=searched_tv['results'])


    
