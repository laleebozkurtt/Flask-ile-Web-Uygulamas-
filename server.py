from flask import Flask, redirect, url_for
#redirect ->yönlendirme için, url_for-> gidilecek yerin urlini veriyor

app = Flask(__name__)

@app.route("/")
def home_page():
    return redirect(url_for("welcome_page"))

@app.route("/welcome")
def welcome_page():
    return "welcooome"

if __name__ == "__main__":
    app.run(debug = True)