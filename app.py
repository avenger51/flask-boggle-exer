from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

boggle_game = Boggle()


@app.route("/")
def homepage():
    """Show board."""

    board = boggle_game.make_board() #boggle_game is created using Boggle() I literally had no idea you could do this
    session['board'] = board #stores the generated boggle board in a session to keep track in browser...
    highscore = session.get("highscore", 0) #I guess if 'highscore' and 'nplays' doesn't exist, make it 0....
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word") #server-side endpoint and acts like an API.  
#It comes from boggle.js??????? absolute nonsense..I don't recall even covering this..
#const resp = await axios.get("/check-word", { params: { word: word }});
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]  #gets the session again..still don't understand where "board" is coming from...
    response = boggle_game.check_valid_word(board, word)  #runs the Boggle.check_valid_word

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)