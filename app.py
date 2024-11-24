from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField,validators,SelectField,IntegerField

app = Flask(__name__)
app.config["SECRET_KEY"] = 'mysecretkey'

class InputForm(FlaskForm):
    gender = SelectField("Gender", validators=[validators.InputRequired()],choices=[(1,"Male"),(2,"Female")])
    age = IntegerField("What is your age?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    height = IntegerField("What is your height?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    weight = IntegerField("What is your weight?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    familyhistory = SelectField("Has a family member suffered or suffers from overweight?", validators=[validators.InputRequired()],choices=[(1,"Male"),(2,"Female")])
    favc = SelectField("Do you eat high caloric food frequently?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    fcvc = SelectField("Do you usually eat vegetables in your meals?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    ncp = SelectField("How many main meals do you have daily?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    caec = SelectField("Do you eat any food between meals?", validators=[validators.InputRequired()],choices=[(1,"Always"),(2,"Frequently"),(3,"Sometimes"),(4,"no")])
    smoke = SelectField("Do you smoke?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    ch2o = IntegerField("How much water do you drink daily?", validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    scc = SelectField("Do you monitor the calories you eat daily?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    faf = IntegerField("How often do you have physical activity?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    tue = IntegerField("How much time do you use technological devices such as cell phone, videogames, television, computer and others?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    calc = SelectField("How often do you drink alcohol?", validators=[validators.InputRequired()],choices=[(1,"Always"),(2,"Frequently"),(3,"Sometimes"),(4,"no")])
    mtrans = SelectField("Which transportation do you usually use?", validators=[validators.InputRequired()],choices=[(1,"Automobile"),(2,"Bike"),(3,"Motorbike"),(4,"Public_Transportation"),(5,"Walking")])


@app.route("/")
def homepage():
    form = InputForm()
    return render_template("./form.html", form=form)

@app.route("/submit",methods=("GET", "POST"))
def submit_page():
    if request.method== "POST":
        return render_template("./submit.html")
