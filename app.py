from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField,validators,SelectField,IntegerField, DecimalField
import pickle
import math


app = Flask(__name__)
app.config["SECRET_KEY"] = 'mysecretkey'

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

class InputForm(FlaskForm):
    gender = SelectField("What is your gender?", validators=[validators.InputRequired()],choices=[(0,"Female"),(1,"Male")])
    age = IntegerField("What is your age?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    height = DecimalField("What is your height, in metres?", validators=[validators.InputRequired(),validators.NumberRange(min=0, max = 3)])
    weight = IntegerField("What is your weight, in kilograms?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    familyhistory = SelectField("Has a family member suffered or suffers from being overweight?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    favc = SelectField("Do you eat high caloric food frequently?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    fcvc = SelectField("Do you usually eat vegetables in your meals?", validators=[validators.InputRequired()],choices=[(1,"Never"),(2,"Sometimes"),(3,"Always")])
    ncp = SelectField("How many main meals do you have daily?", validators=[validators.InputRequired()],choices=[(1,"Between 1 and 2"),(2,"3"),(3,"More than 3")])
    caec = SelectField("Do you eat any food between meals?", validators=[validators.InputRequired()],choices=[(0,"No"),(1,"Sometimes"),(2,"Frequently"),(3,"Always")])
    smoke = SelectField("Do you smoke?", validators=[validators.InputRequired()],choices=[(0,"No"),(1,"Yes")])
    ch2o = SelectField("How much water do you drink daily?", validators=[validators.InputRequired()],choices=[(1,"Less than a liter"), (2,"Between 1 and 2 litres"), (3,"More than 2 litres")])
    scc = SelectField("Do you monitor the calories you eat daily?", validators=[validators.InputRequired()],choices=[(0,"Yes"),(1,"No")])
    faf = SelectField("How often do you have physical activity per week?", validators=[validators.InputRequired()],choices=[(0,"I do not have"),(1,"1 or 2 days"),(2,"2 or 4 days"),(3,"4 or 5 days")])
    tue = SelectField("How much time do you use technological devices such as cell phone, videogames, television, computer and others?", validators=[validators.InputRequired()],choices=[(0,"0-2 hours"),(1,"3-5 hours"),(2,"More than 5 hours")])
    calc = SelectField("How often do you drink alcohol?", validators=[validators.InputRequired()],choices=[(0,"I do not drink"),(1,"Sometimes"),(2,"Frequently"),(3,"Always")])
    mtrans = SelectField("Which transportation do you usually use?", validators=[validators.InputRequired()],choices=[(0,"Automobile"),(1,"Bike"),(2,"Motorbike"),(3,"Public Transportation"),(4,"Walking")])


@app.route("/")
def homepage():
    form = InputForm()
    return render_template("./form.html", form=form)




@app.route("/submit", methods=["GET", "POST"])
def submit_form():
    form = InputForm()
    if form.validate_on_submit():  # checks if form is submitted via POST
        # Collect the form data
        # Since our model used one hot encoding extra columns corresponding to to the value were added as features
        if(form.familyhistory.data == 1):
            familyhistory_0 = 0
            familyhistory_1 = 1
        else:
            familyhistory_0 = 1
            familyhistory_1 = 0

        mtrans_data = int(form.mtrans.data)
        Mtrans_values = [0, 0, 0, 0, 0]
        if 0 <= mtrans_data <= 4:
            Mtrans_values[mtrans_data] = 1

        question_data = {
            'Gender': int(form.gender.data),
            'Age': math.log(int(form.age.data)),
            'Height': math.log(float(form.height.data)),
            'Weight': math.log(int(form.weight.data)),
            'FAVC': int(form.favc.data),
            'FCVC': float(form.fcvc.data),
            'NCP': float(form.ncp.data),
            'CAEC': int(form.caec.data),
            'SMOKE': int(form.smoke.data),
            'CH2O': float(form.ch2o.data),
            'SCC': int(form.scc.data),
            'FAF': float(form.faf.data),
            'TUE': float(form.tue.data),
            'CALC': int(form.calc.data),
            'family_history_with_overweight_0': int(familyhistory_0) , 
            'family_history_with_overweight_1': int(familyhistory_1),  
            'MTRANS_0': Mtrans_values[0],
            'MTRANS_1': Mtrans_values[1],
            'MTRANS_2': Mtrans_values[2],
            'MTRANS_3': Mtrans_values[3],
            'MTRANS_4': Mtrans_values[4],
        }
        #Using hardcoded values to standardize
        question_data['Age'] = (question_data["Age"] - 2.63905733) * 0.98390003 + -2.59656858
        question_data['Height'] = (question_data["Height"] - 0.37156356) * 3.20992985 + -1.19269295 
        question_data['Weight'] = (question_data["Weight"] - 3.66356165) * 0.6712626 + -2.45921192
        
        # Use model to predict
        obesity_label = model.predict([list(question_data.values())])[0]
        
        return render_template("submit.html", obesity_label=obesity_label, question_data=question_data)
    return render_template("form.html", form=form)
