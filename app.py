from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField

app = Flask(__name__)
app.config["SECRET_KEY"] = 'mysecretkey'

class InputForm(FlaskForm):
    question1 = StringField("Answer this question: ")


@app.route("/")
def hello_world():
    form = InputForm()
    return render_template("./form.html", form=form)
    #return "<p>Hi!</p>"

