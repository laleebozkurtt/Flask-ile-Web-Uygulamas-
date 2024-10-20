from flask import Flask, redirect, url_for, render_template, request
#redirect ->yönlendirme için, url_for-> gidilecek yerin urlini veriyor
import os
from db_init import initialize

from queries import *



app = Flask(__name__)

Heroku =False

#eğer local de çalışıyorsam bunları yap diyorum çünkü heroku debug=true yu kabul etmiyor

if (not Heroku):
    os.environ['DATABASE_URL'] = "dbname ='postgres' user ='postgres' host ='localhost' password ='1234'"
    initialize(os.environ.get('DATABASE_URL'))

@app.route("/")
def home_page():
    return render_template("home_page.html")

@app.route("/movies", methods=['GET','POST'])
def movies_page():
    if request.method =="GET":
        movies = select("id, name, likes, dislikes, image", "movie",asDict=True)
        return render_template("movies.html", movies = movies)
    elif request.method =="POST":
        if "like" in request.form:
            update("movie", "likes =likes+1", "id={}".format(request.form.get('like')))
        if "dislike" in request.form:
            update("movie", "dislikes = dislikes + 1", "id={}".format(request.form.get('dislike')))
        return redirect(url_for('movies_page'))
    
@app.route("/movies/<id>")
def movie_detail_page(id):
    movie = select("name, image ", "movie", "id={}".format(id), asDict =True)
    actors =select("actor.name, actor.likes, actor.dislikes, actor.image",
    "actor join index on actor.id=index.actor_id",
    "index.movie_id={}".format(id), asDict=True)
    return render_template("movie_detail_page.html",movie=movie, actors=actors)

if __name__ == "__main__":
    if (not Heroku):
        app.run(debug = True)
    else:
        app.run()