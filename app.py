from flask import Flask, render_template, request, url_for, flash, redirect
import pickle
from flask_wtf import FlaskForm
from wtforms import StringField,validators,SelectField,IntegerField, FloatField
import xgboost as xgb
import numpy as np

app = Flask(__name__)
app.config["SECRET_KEY"] = 'mysecretkey'

class InputForm(FlaskForm):
    gender = SelectField("What is your gender?", validators=[validators.InputRequired()],choices=[(0,"Female"),(1,"Male")])
    age = IntegerField("What is your age?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    height = FloatField("What is your height, in metres?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    weight = IntegerField("What is your weight, in kilograms?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    familyhistory = SelectField("Has a family member suffered or suffers from overweight?", validators=[validators.InputRequired()],choices=[(0,"No"),(1,"Yes")])
    favc = SelectField("Do you eat high caloric food frequently?", validators=[validators.InputRequired()],choices=[(0,"Yes"),(1,"No")])
    fcvc = SelectField("Do you usually eat vegetables in your meals?", validators=[validators.InputRequired()],choices=[(0,"Never"),(1,"Sometimes"),(2,"Always")])
    ncp = SelectField("How many main meals do you have daily?", validators=[validators.InputRequired()],choices=[(0,"Between 1 and 2"),(1,"3"),(2,"More than 3")])
    caec = SelectField("Do you eat any food between meals?", validators=[validators.InputRequired()],choices=[(0,"No"),(1,"Sometimes"),(2,"Frequently"),(3,"Always")])
    smoke = SelectField("Do you smoke?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(0,"No")])
    ch2o = SelectField("How much water do you drink daily?", validators=[validators.InputRequired()],choices=[(0,"Less than a liter"), (1,"Between 1 and 2 litres"), (2,"More than 2 litres")])
    scc = SelectField("Do you monitor the calories you eat daily?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(0,"No")])
    faf = SelectField("How often do you have physical activity per week?", validators=[validators.InputRequired()],choices=[(0,"I do not have"),(1,"1 or 2 days"),(2,"2 or 4 days"),(3,"4 or 5 days")])
    tue = SelectField("How much time do you use technological devices such as cell phone, videogames, television, computer and others?", validators=[validators.InputRequired()],choices=[(0,"0-2 hours"),(1,"3-5 hours"),(2,"More than 5 hours")])
    calc = SelectField("How often do you drink alcohol?", validators=[validators.InputRequired()],choices=[(0,"I do not drink"),(1,"Sometimes"),(2,"Frequently"),(3,"Always")])
    mtrans = SelectField("Which transportation do you usually use?", validators=[validators.InputRequired()],choices=[(0,"Automobile"),(1,"Motorbike"),(2,"Bike"),(3,"Public Transportation"),(4,"Walking")])


@app.route("/",methods=("GET", "POST"))
def homepage():
    form = InputForm()
    if request.method == "POST":
        gender = form.gender.data
        age = form.age.data
        height = form.height.data
        weight = form.weight.data
        familyhistory = form.familyhistory.data
        favc = form.favc.data
        fcvc = form.fcvc.data
        ncp = form.ncp.data
        caec = form.caec.data
        smoke = form.smoke.data
        ch2o = form.ch2o.data
        scc = form.scc.data
        faf = form.faf.data
        tue = form.tue.data
        calc = form.calc.data
        mtrans = form.mtrans.data
        outcome = runModel([gender,age,height,weight,familyhistory,favc,fcvc,ncp,caec,smoke,ch2o,scc,faf,tue,calc,mtrans])
        return render_template("./submit.html",outcome=outcome)

    return render_template("./form.html", form=form) 

def runModel(data):
    loaded_model = pickle.load(open('model.pkl', 'rb'))
    nobeyesdad_mapping = [
        'Insufficient_Weight',
        'Normal_Weight',
        'Overweight_Level_I',
        'Overweight_Level_II',
        'Obesity_Type_I',
        'Obesity_Type_II',
        'Obesity_Type_III',
    ]
    result = loaded_model.predict(np.array(data,dtype=object).reshape(-1,16))
    return nobeyesdad_mapping[result[0]]
