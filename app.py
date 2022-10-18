from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sqxxcooslvxqjm:bb9d0ac21780244dceb1f47733113ab7ff649c02f1548924f68e32795f438ef5@ec2-18-207-37-30.compute-1.amazonaws.com:5432/d6bghturh5g56k'

db = SQLAlchemy(app)

class Accountability(db.Model):
    __tablename__ = "accountability"
    id = db.Column(db.Integer, primary_key=True)
    stakeholder = db.Column(db.String)
    date = db.Column(db.Date)
    num_meetings_admin_since_last = db.Column(db.Integer)
    admin_met_with = db.Column(db.String)
    num_meetings_students = db.Column(db.Integer)
    num_committee_meetings = db.Column(db.Integer)
    num_meetings_other_committees = db.Column(db.Integer)
    num_hours_worked = db.Column(db.Integer)
    asg_rating = db.Column(db.Integer)
    recieveing_support = db.Column(db.String)
    notes = db.Column(db.String)

    def __init__(self, stakeholder, date, num_meetings_admin_since_last, 
                        admin_met_with, num_meetings_students, num_committee_meetings, num_meetings_other_committees, 
                        num_hours_worked, asg_rating, recieveing_support, notes):
        self.stakeholder = stakeholder
        self.date = date
        self.num_meetings_admin_since_last = num_meetings_admin_since_last
        self.admin_met_with = admin_met_with
        self.num_meetings_students = num_meetings_students
        self.num_committee_meetings = num_committee_meetings
        self.num_meetings_other_committees = num_meetings_other_committees
        self.num_hours_worked = num_hours_worked
        self.asg_rating = asg_rating
        self.recieveing_support = recieveing_support
        self.notes = notes

with app.app_context():
    db.create_all()

stakeholders = ['Jason Hegelmeyer',
                'Donovan Cusick',
                'Steph Shields',
                'Valeria Rodriguez',
                'Jo Scaletty',
                'Molly Whalen',
                'Armaan Ajani',
                'Sadie Bernstein',
                'Alexis Schwartz',
                'Joshua Gregory',
                'Marcos Rios',
                'Felix Beilin',
                'Brian Whetsell',
                'Zai Dawodu',
                'Julia Karten',
                'Sam Douki',
                'Sohae Yang',
                'Sara Azimipour',
                'Dylan Jost',
                'Leah Ryzenman',
                'Dalia Segal-Miller']
admin =  ['Jaci Casazza',
          'Michael Fitzpatrick',
          'Roma Khanna',
          'Miriam Sherin',
          'K. Parker Hess',
          'Hayley Kretchmer',
          'Tracey Gibson-Jackson',
          'Joe Lattal',
          'Jeremy Schenk',
          'Kelly Schaefer',
          'Mona Dugo',
          'Lesley-Ann Brown Henderson',
          'Patricia Lampkin']

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/data_entry")
def data_entry():
    data = Accountability.query.order_by(Accountability.date.desc()).all()
    stakeholders_and_dates = []
    for row in data:
        curr_row = {}
        curr_row['date'] = row.date
        curr_row['stakeholder'] = row.stakeholder
        stakeholders_and_dates.append(curr_row)
    return render_template('data_entry.html',stakeholders=stakeholders,admin=admin,stakeholders_and_dates=stakeholders_and_dates)

@app.route("/data_submitted", methods=['POST'])
def data_submitted():
    if request.method == 'POST':
        stakeholder = request.form['stakeholder']
        date = request.form['date']
        num_meetings_admin_since_last = request.form.get('num_meetings_admin_since_last')
        admin_met_with_lst = request.form.getlist('admin_met_with')
        admin_met_with = ''
        if admin_met_with_lst != []:
            for admin in admin_met_with_lst:
                if admin != 'Other(s)':
                    admin_met_with += str(admin) + ','
        admin_met_with_other = request.form.get('admin_met_with_other')
        if admin_met_with_other != '':
            admin_met_with += admin_met_with_other
        else:
            admin_met_with = admin_met_with[:-1]
        if admin_met_with == '':
            admin_met_with = None
        num_meetings_students = request.form.get('num_meetings_students')
        num_committee_meetings = request.form.get('num_committee_meetings')
        num_meetings_other_committees = request.form.get('num_meetings_other_committees')
        num_hours_worked = request.form.get('num_hours_worked')
        asg_rating = request.form.get('asg_rating')
        recieveing_support = request.form.get('recieveing_support')
        notes = request.form.get('notes')
        if notes == '':
            notes = None
        reg = Accountability(stakeholder,date,num_meetings_admin_since_last,admin_met_with,
                            num_meetings_students, num_committee_meetings,num_meetings_other_committees,num_hours_worked,
                            asg_rating,recieveing_support,notes)
        db.session.add(reg)
        db.session.commit()
    return render_template('data_submitted.html')

@app.route("/search_by_person")
def search_by_person():
    data_q = Accountability.query.order_by(Accountability.date.desc()).all()
    data = []
    for row in data_q:
        curr_row = {}
        curr_row['date'] = row.date
        curr_row['stakeholder'] = row.stakeholder
        curr_row['num_meetings_admin_since_last'] = row.num_meetings_admin_since_last
        curr_row['admin_met_with'] = row.admin_met_with
        curr_row['num_meetings_students'] = row.num_meetings_students
        curr_row['num_committee_meetings'] = row.num_committee_meetings
        curr_row['num_meetings_other_committees'] = row.num_meetings_other_committees
        curr_row['num_hours_worked'] = row.num_hours_worked
        curr_row['asg_rating'] = row.asg_rating
        curr_row['recieveing_support'] = row.recieveing_support
        data.append(curr_row)
    return render_template('search_by_person.html',stakeholders=stakeholders,data=data)