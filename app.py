from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import os
import csv
import json
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["connection_string"]
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

class Accountability(db.Model):
    __tablename__ = "accountability"
    id = db.Column(db.Integer, primary_key=True)
    stakeholder = db.Column(db.String)
    date = db.Column(db.Date)
    num_meetings_admin_since_last = db.Column(db.Integer)
    admin_met_with = db.Column(db.String)
    admin_met_with_numbers = db.Column(db.String)
    num_meetings_students = db.Column(db.Integer)
    num_committee_meetings = db.Column(db.Integer)
    num_meetings_other_committees = db.Column(db.Integer)
    num_hours_worked = db.Column(db.Integer)
    asg_rating = db.Column(db.Integer)
    recieveing_support = db.Column(db.String)
    notes = db.Column(db.String)

    def __init__(self, stakeholder, date, num_meetings_admin_since_last, 
                        admin_met_with, admin_met_with_numbers, num_meetings_students, num_committee_meetings, num_meetings_other_committees, 
                        num_hours_worked, asg_rating, recieveing_support, notes):
        self.stakeholder = stakeholder
        self.date = date
        self.num_meetings_admin_since_last = num_meetings_admin_since_last
        self.admin_met_with = admin_met_with
        self.admin_met_with_numbers = admin_met_with_numbers
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
        admin_met_with_numbers = ''
        if admin_met_with_lst != []:
            for admin in admin_met_with_lst:
                if admin != 'Other(s)':
                    admin_met_with += str(admin) + ','
                    admin_met_with_numbers += str(request.form.get('num_meetings_with_' + str(admin))) + ','
        if 'Other(s)' in admin_met_with_lst:
            admin_met_with_other = request.form.get('admin_met_with_other')
            if admin_met_with_other != '':
                admin_met_with += admin_met_with_other
                lst = [word.strip() for word in admin_met_with_other.split(',')]
                for j in lst:
                    admin_met_with_numbers += str(request.form.get('num_meetings_with_' + str(j))) + ','
            else:
                admin_met_with = admin_met_with[:-1]
            admin_met_with_numbers = admin_met_with_numbers[:-1]
        if admin_met_with == '':
            admin_met_with = None
        if admin_met_with_numbers == '':
            admin_met_with_numbers = None
        num_meetings_students = request.form.get('num_meetings_students')
        num_committee_meetings = request.form.get('num_committee_meetings')
        num_meetings_other_committees = request.form.get('num_meetings_other_committees')
        num_hours_worked = request.form.get('num_hours_worked')
        asg_rating = request.form.get('asg_rating')
        recieveing_support = request.form.get('recieveing_support')
        notes = request.form.get('notes')
        if notes == '':
            notes = None
        reg = Accountability(stakeholder,date,num_meetings_admin_since_last,admin_met_with,admin_met_with_numbers,
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
        curr_row['admin_met_with_numbers'] = row.admin_met_with_numbers
        curr_row['num_meetings_students'] = row.num_meetings_students
        curr_row['num_committee_meetings'] = row.num_committee_meetings
        curr_row['num_meetings_other_committees'] = row.num_meetings_other_committees
        curr_row['num_hours_worked'] = row.num_hours_worked
        curr_row['asg_rating'] = row.asg_rating
        curr_row['recieveing_support'] = row.recieveing_support
        if row.notes != None:
            curr_row['notes'] = row.notes.replace('\r\n','newlinehere').replace('"',"'")
        else:
            curr_row['notes'] = ''
        data.append(curr_row)
    return render_template('search_by_person.html',stakeholders=stakeholders,data=data)

@app.route("/asg_performance_summary")
def asg_performance_summary():
    data_q = Accountability.query.order_by(Accountability.date.desc()).all()
    data = []
    for row in data_q:
        curr_row = {}
        curr_row['date'] = row.date
        curr_row['stakeholder'] = row.stakeholder
        curr_row['num_meetings_admin_since_last'] = row.num_meetings_admin_since_last
        curr_row['admin_met_with'] = row.admin_met_with
        curr_row['admin_met_with_numbers'] = row.admin_met_with_numbers
        curr_row['num_meetings_students'] = row.num_meetings_students
        curr_row['num_committee_meetings'] = row.num_committee_meetings
        curr_row['num_meetings_other_committees'] = row.num_meetings_other_committees
        curr_row['num_hours_worked'] = row.num_hours_worked
        curr_row['asg_rating'] = row.asg_rating
        curr_row['recieveing_support'] = row.recieveing_support
        if row.notes != None:
            curr_row['notes'] = row.notes.replace('\r\n','newlinehere').replace('"',"'")
        else:
            curr_row['notes'] = ''
        data.append(curr_row)
    return render_template('asg_performance_summary.html',stakeholders=stakeholders,data=data)

# FOR ASG PIVOT
@app.route("/mockdata", methods = ['GET', 'POST'])
@cross_origin()
def mockdata():
    rows = None
    if (request.method == 'GET'):
        with open('pivotcsvs/cleaned-asg-data.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        with open('pivotjsons/cleaned-asg-data.json', 'w') as json_file:
            json.dump(rows, json_file)
    f = open(r'pivotjsons/cleaned-asg-data.json')
    data = json.load(f)
    return data

@app.route("/data1819", methods = ['GET', 'POST'])
@cross_origin()
def data1819():
    rows = None
    if (request.method == 'GET'):
        with open('pivotcsvs/data1819.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        with open('pivotjsons/data1819.json', 'w') as json_file:
            json.dump(rows, json_file)
    f = open(r'pivotjsons/data1819.json')
    data = json.load(f)
    return data

@app.route("/data1920", methods = ['GET', 'POST'])
@cross_origin()
def data1920():
    rows = None
    if (request.method == 'GET'):
        with open('pivotcsvs/data1920.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        with open('pivotjsons/data1920.json', 'w') as json_file:
            json.dump(rows, json_file)
    f = open(r'pivotjsons/data1920.json')
    data = json.load(f)
    return data

@app.route("/data2021", methods = ['GET', 'POST'])
@cross_origin()
def data2021():
    rows = None
    if (request.method == 'GET'):
        with open('pivotcsvs/data2021.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        with open('pivotjsons/data2021.json', 'w') as json_file:
            json.dump(rows, json_file)
    f = open(r'pivotjsons/data2021.json')
    data = json.load(f)
    return data

@app.route("/data2122", methods = ['GET', 'POST'])
@cross_origin()
def data2122():
    rows = None
    if (request.method == 'GET'):
        with open('pivotcsvs/data2122.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        with open('pivotjsons/data2122.json', 'w') as json_file:
            json.dump(rows, json_file)
    f = open(r'pivotjsons/data2122.json')
    data = json.load(f)
    return data

@app.route("/data2223", methods = ['GET', 'POST'])
@cross_origin()
def data2223():
    rows = None
    if (request.method == 'GET'):
        with open('pivotcsvs/data2223.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        with open('pivotjsons/data2223.json', 'w') as json_file:
            json.dump(rows, json_file)
    f = open(r'pivotjsons/data2223.json')
    data = json.load(f)
    return data