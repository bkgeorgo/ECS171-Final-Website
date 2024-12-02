from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField,validators,SelectField,IntegerField

app = Flask(__name__)
app.config["SECRET_KEY"] = 'mysecretkey'

class InputForm(FlaskForm):
    gender = SelectField("What is your gender?", validators=[validators.InputRequired()],choices=[(1,"Female"),(2,"Male")])
    age = IntegerField("What is your age?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    height = IntegerField("What is your height, in metres?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    weight = IntegerField("What is your weight, in kilograms?", validators=[validators.InputRequired(),validators.NumberRange(min=0)])
    familyhistory = SelectField("Has a family member suffered or suffers from overweight?", validators=[validators.InputRequired()],choices=[(1,"Male"),(2,"Female")])
    favc = SelectField("Do you eat high caloric food frequently?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    fcvc = SelectField("Do you usually eat vegetables in your meals?", validators=[validators.InputRequired()],choices=[(1,"Never"),(2,"Sometimes"),(3,"Always")])
    ncp = SelectField("How many main meals do you have daily?", validators=[validators.InputRequired()],choices=[(1,"Between 1 and 2"),(2,"3"),(3,"More than 3")])
    caec = SelectField("Do you eat any food between meals?", validators=[validators.InputRequired()],choices=[(1,"No"),(2,"Sometimes"),(3,"Frequently"),(4,"Always")])
    smoke = SelectField("Do you smoke?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    ch2o = SelectField("How much water do you drink daily?", validators=[validators.InputRequired()],choices=[(1,"Less than a liter"), (2,"Between 1 and 2 litres"), (3,"More than 2 litres")])
    scc = SelectField("Do you monitor the calories you eat daily?", validators=[validators.InputRequired()],choices=[(1,"Yes"),(2,"No")])
    faf = SelectField("How often do you have physical activity per week?", validators=[validators.InputRequired()],choices=[(1,"I do not have"),(2,"1 or 2 days"),(3,"2 or 4 days"),(4,"4 or 5 days")])
    tue = SelectField("How much time do you use technological devices such as cell phone, videogames, television, computer and others?", validators=[validators.InputRequired()],choices=[(1,"0-2 hours"),(2,"3-5 hours"),(3,"More than 5 hours")])
    calc = SelectField("How often do you drink alcohol?", validators=[validators.InputRequired()],choices=[(1,"I do not drink"),(2,"Sometimes"),(3,"Frequently"),(4,"Always")])
    mtrans = SelectField("Which transportation do you usually use?", validators=[validators.InputRequired()],choices=[(1,"Automobile"),(2,"Bike"),(3,"Motorbike"),(4,"Public Transportation"),(5,"Walking")])


@app.route("/")
def homepage():
    form = InputForm()
    return render_template("./form.html", form=form)




@app.route("/submit", methods=["GET", "POST"])
def submit_form():
    form = InputForm()
    if form.validate_on_submit():  # checks if form is submitted via POST
        # Collect the form data
        question_data = {
            'CH2O': form.ch2o.data,
            'SCC': form.scc.data,
            'FAF': form.faf.data,
            'TUE': form.tue.data,
            'CALC': form.calc.data,
            'MTRANS': form.mtrans.data,
            'Gender': form.gender.data,
            'Age': form.age.data,
            'Height': form.height.data,
            'Weight': form.weight.data,
            'family_history_with_overweight': form.familyhistory.data,
            'FAVC': form.favc.data,
            'FCVC': form.fcvc.data,
            'NCP': form.ncp.data,
            'CAEC': form.caec.data,
            'SMOKE': form.smoke.data
        }
        # Example: include obesity_label as an argument to render_template to display prediction
        # obesity_label = run_model(question_data)  # Your model prediction logic here
        
        return render_template("submit.html", form=form, question_data=question_data)
    return render_template("form.html", form=form)


