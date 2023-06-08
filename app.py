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

class Accountability_2023(db.Model):
    __tablename__ = "accountability_2023"
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

class Projects(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    committee_name = db.Column(db.String)
    date = db.Column(db.Date)
    project_name = db.Column(db.String)
    num_hours_worked = db.Column(db.Integer)
    notes = db.Column(db.String)

    def __init__(self, committee_name, date, project_name, num_hours_worked, notes):
        self.committee_name = committee_name
        self.date = date
        self.project_name = project_name
        self.num_hours_worked = num_hours_worked
        self.notes = notes

with app.app_context():
    db.create_all()

stakeholders = ['Donovan Cusick',
                'Molly Whalen',
                'Dalia Segal-Miller',
                'Alexis Schwartz',
                'Malik Rice',
                'Constanza Estrada',
                'Aylin Eryilmaz',
                'Enzo Banal',
                'Dylan Jost',
                'Kurtis Nelson',
                'Patrick Hoey',
                'Aria Wozniak',
                'Leah Ryzenman',
                'Grace Houren',
                'Brian Whetsell',
                'Adrian Ayala-Perez',
                'Madeleine Williams',
                'Stephanie Shields',
                'Zai Dawodu',
                'Caleb Snead',
                'Mia Xia',
                'Ty\'Shea Woods',
                'Sam Bull']

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
          'Susan Davis']

committees = ['Academics',
              'Analytics',
              'Campus Life',
              'Communications',
              'Community Relations',
              'Finance',
              'Health & Wellness',
              'Justice & Inclusion',
              'Policy Research',
              'Sustainability']

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/data_entry")
def data_entry():
    data = Accountability_2023.query.order_by(Accountability_2023.date.desc()).all()
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
        reg = Accountability_2023(stakeholder,date,num_meetings_admin_since_last,admin_met_with,admin_met_with_numbers,
                            num_meetings_students, num_committee_meetings,num_meetings_other_committees,num_hours_worked,
                            asg_rating,recieveing_support,notes)
        db.session.add(reg)
        db.session.commit()
    return render_template('data_submitted.html')

@app.route("/search_by_person")
def search_by_person():
    data_q = Accountability_2023.query.order_by(Accountability_2023.date.desc()).all()
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
    data_q = Accountability_2023.query.order_by(Accountability_2023.date.desc()).all()
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

@app.route("/datawinter2223", methods = ['GET', 'POST'])
@cross_origin()
def datawinter2223():
    rows = None
    if (request.method == 'GET'):
        with open('pivotcsvs/datawinter2223.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        with open('pivotjsons/datawinter2223.json', 'w') as json_file:
            json.dump(rows, json_file)
    f = open(r'pivotjsons/datawinter2223.json')
    data = json.load(f)
    return data

@app.route("/project_data")
def project_data():
    projects_data = {}
    data = Projects.query.order_by(Projects.date.desc()).all()
    for row in data:
        commitee_name = row.committee_name
        project_name = row.project_name
        if (commitee_name in projects_data.keys()):
            if (not project_name in projects_data[commitee_name]):
                projects_data[commitee_name].append(project_name)
        else:
            projects_data[commitee_name] = [project_name]
    return render_template('project_data.html',projects_data=projects_data,committees=committees)

@app.route("/project_data_submitted", methods=['POST'])
def project_data_submitted():
    if request.method == 'POST':
        committee_name = request.form['committee_name']
        date = request.form['date']
        project_name = None
        if (request.form['project_name'] != 'Other'):
            project_name = request.form['project_name']
        else:
            project_name = request.form['project_other']
        num_hours_worked = request.form['num_hours_worked']
        notes = request.form.get('notes')
        if notes == '':
            notes = None
        reg = Projects(committee_name,date,project_name,num_hours_worked,notes)
        db.session.add(reg)
        db.session.commit()
    return render_template('data_submitted.html')

@app.route("/projectapi", methods = ['GET', 'POST'])
@cross_origin()
def projectapi():
    new_data = []
    data = Projects.query.order_by(Projects.date.desc()).all()
    for row in data:
        found = False
        for data in new_data:
            if data['committee_name'] == str(row.committee_name) and data['project_name'] == str(row.project_name):
                found = True
                num = int(data['num_hours_worked'])
                num += int(row.num_hours_worked)
                data['num_hours_worked'] = str(num)
                data["data"].append({
                    'date':  str(row.date),
                    'notes': str(row.notes)
                })
        row_dict = {}
        if not found:
            row_dict["committee_name"] = str(row.committee_name)
            row_dict["project_name"] = str(row.project_name)
            row_dict["num_hours_worked"] = str(row.num_hours_worked)
            row_dict["data"] = [{
                'date':  str(row.date),
                'notes': str(row.notes)
            }]
            new_data.append(row_dict)
    return new_data