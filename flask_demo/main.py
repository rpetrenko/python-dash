from flask import Flask, render_template, redirect
from flask_wtf.csrf import CSRFProtect

from flask_wtf import FlaskForm
# from wtforms import TextField, FormField, SubmitField, StringField
# from wtforms.validators import Optional, DataRequired
# from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FieldList, FormField
from wtforms.validators import DataRequired
import pandas as pd
import random
import string

app = Flask(__name__)
app.secret_key = 'adkla;jdkEEASGDAafsfasdf'
csrf = CSRFProtect(app)

df = pd.read_csv(
    '../data/data.csv')

def rand_str(n=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

class LocationForm(FlaskForm):
    location_id = BooleanField()
    col1 = ''
    col2 = ''
    # def populate_obj(self, obj):


class MyForm(FlaskForm):
    """
    authors = FieldList(StringField('Name', [validators.required()]))
    """
    # table_data = FieldList(FormField(LocationForm), min_entries=df.shape[0])
    table_data = FieldList(FormField(LocationForm), min_entries=3)
    col1 = "Desease state"
    col2 = "Recommendation"

    def populate(self, data):
        for x in self.table_data:
            print(x)
    # def populate_obj(self, obj, name):

    # def populate_obj(self, obj, name):
    #     while len(getattr(obj, name)) < len(self.entries):
    #         newModel = self.model()
            # db.session.add(newModel)
            # getattr(obj, name).append(newModel)
        # while len(getattr(obj, name)) > len(self.entries):
        #     pass
            # db.session.delete(getattr(obj, name).pop())
        # super(MyForm, self).populate_obj(obj, name)

class Default:
    col1 = 'x'

formdata = {'col1': 'X1'}
@app.route('/', methods=('GET', 'POST'))
def submit():
    # form = MyForm(formdata=formdata)
    default_data = Default()
    form = MyForm()
    form.populate(formdata)
    if form.validate_on_submit():
        print('submitted')
        # print(dir(form))
        for x in form.data['table_data']:
            print(x['location_id'])
            # form.populate_obj()
    #     return redirect('/success')
    return render_template('page2.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)