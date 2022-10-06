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

    def __init__(self, stakeholder, date, num_meetings_admin_since_last):
        self.stakeholder = stakeholder
        self.date = date
        self.num_meetings_admin_since_last = num_meetings_admin_since_last

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
        num_meetings_admin_since_last = request.form['num_meetings_admin_since_last']
        reg = Accountability(stakeholder,date,num_meetings_admin_since_last)
        db.session.add(reg)
        db.session.commit()
    return render_template('home.html')
