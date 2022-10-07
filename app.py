from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/asg-data'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zzgbanrolxeoql:8d9526e98359fc9b676443479d91ef329343b06010795271cedaa32be19a5693@ec2-3-214-2-141.compute-1.amazonaws.com:5432/dlglent4m7pik'
db = SQLAlchemy(app)

class Accountability(db.Model):
    __tablename__ = "accoutability"
    id = db.Column(db.Integer, primary_key=True)
    stakeholder = db.Column(db.String)
    date = db.Column(db.Date)
    num_meetings_admin_since_last = db.Column(db.Integer)
    admin_met_with = db.Column(db.String)
    num_meetings_administration_since_last = db.Column(db.Integer)
    num_meetings_students = db.Column(db.Integer)
    num_committee_meetings = db.Column(db.Integer)
    num_meetings_other_committees = db.Column(db.Integer)
    num_hours_worked = db.Column(db.Integer)
    asg_rating = db.Column(db.Integer)
    recieveing_support = db.Column(db.String)
    notes = db.Column(db.String)

    def __init__(self, stakeholder, date, num_meetings_admin_since_last, 
                        admin_met_with, num_meetings_administration_since_last, 
                        num_meetings_students, num_committee_meetings, num_meetings_other_committees, 
                        num_hours_worked, asg_rating, recieveing_support, notes):
        self.stakeholder = stakeholder
        self.date = date
        self.num_meetings_admin_since_last = num_meetings_admin_since_last
        self.admin_met_with = admin_met_with
        self.num_meetings_administration_since_last = num_meetings_administration_since_last
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
admin =  ['Fill me',
          'Ask Molly']

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/data_entry")
def data_entry():
    return render_template('data_entry.html',stakeholders=stakeholders,admin=admin)

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
        num_meetings_administration_since_last = request.form.get('num_meetings_administration_since_last')
        num_meetings_students = request.form.get('num_meetings_students')
        num_committee_meetings = request.form.get('num_committee_meetings')
        num_meetings_other_committees = request.form.get('num_meetings_other_committees')
        num_hours_worked = request.form.get('num_hours_worked')
        asg_rating = request.form.get('asg_rating')
        recieveing_support = request.form.get('recieveing_support')
        notes = request.form.get('notes')
        reg = Accountability(stakeholder,date,num_meetings_admin_since_last,admin_met_with,
                            num_meetings_administration_since_last,num_meetings_students,
                            num_committee_meetings,num_meetings_other_committees,num_hours_worked,
                            asg_rating,recieveing_support,notes)
        db.session.add(reg)
        db.session.commit()
    return render_template('data_submitted.html')
