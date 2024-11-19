from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired  # Checks if user left question empty or not

app = Flask(__name__)
app.config["SECRET_KEY"] = 'mysecretkey'


# Define the form with all the features
class InputForm(FlaskForm):
    
    CH2O = IntegerField("How many liters of water do you drink a day?", validators=[DataRequired()])
    SCC = RadioField("Do you monitor the calories you eat daily?", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    FAF = IntegerField("How many days in a week do you usually work out?", validators=[DataRequired()])
    TUE = IntegerField("How many hours per day do you spend on any technological device?", validators=[DataRequired()])
    CALC = SelectField("How often do you drink alcohol?", choices=[('Never', 'Never'), ('Sometimes', 'Sometimes'), ('Frequently', 'Frequently'), ('Always', 'Always')], validators=[DataRequired()])
    MTRANS = SelectField("Which transportation do you usually use?", choices=[('Automobile', 'Automobile'), ('Motorbike', 'Motorbike'), ('Bike', 'Bike'), ('Public Transportation', 'Public Transportation'), ('Walking', 'Walking')], validators=[DataRequired()])
    Gender = RadioField("Gender", choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    Age = IntegerField("Age", validators=[DataRequired()])
    Height = IntegerField("Height (meters)", validators=[DataRequired()])
    Weight = IntegerField("Weight (kg)", validators=[DataRequired()])
    family_history_with_overweight = RadioField("Do you have a family history of weight related issues?", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    FAVC = RadioField("Do you eat high caloric food frequently?", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    FCVC = IntegerField("Do you usually eat vegetables in your meals?(1-never, 2-sometimes, 3-always)", validators=[DataRequired()])
    NCP = IntegerField("How many main meals do you have daily?(1-4)", validators=[DataRequired()])
    CAEC = SelectField("Do you eat any food between meals?", choices=[('No', 'No'), ('Sometimes', 'Sometimes'), ('Frequently', 'Frequently'), ('Always', 'Always')], validators=[DataRequired()])
    SMOKE = RadioField("Do you smoke?", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])


@app.route("/", methods=["GET", "POST"])
def home():
    form = InputForm()
    if form.validate_on_submit():  #checks to see if user submitted form
        # Dictionary to store data
        question_data = {
            'CH2O': form.CH2O.data,
            'SCC': form.SCC.data,
            'FAF': form.FAF.data,
            'TUE': form.TUE.data,
            'CALC': form.CALC.data,
            'MTRANS': form.MTRANS.data,
            'Gender': form.Gender.data,
            'Age': form.Age.data,
            'Height': form.Height.data,
            'Weight': form.Weight.data,
            'family_history_with_overweight': form.family_history_with_overweight.data,
            'FAVC': form.FAVC.data,
            'FCVC': form.FCVC.data,
            'NCP': form.NCP.data,
            'CAEC': form.CAEC.data,
            'SMOKE': form.SMOKE.data
        }
        return render_template("form.html", form=form, question_data=question_data)
    return render_template("form.html", form=form)


