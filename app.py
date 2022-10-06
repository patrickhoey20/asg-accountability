from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/asg-data'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zzgbanrolxeoql:8d9526e98359fc9b676443479d91ef329343b06010795271cedaa32be19a5693@ec2-3-214-2-141.compute-1.amazonaws.com:5432/dlglent4m7pik'
db = SQLAlchemy(app)

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
        db.execute("INSERT INTO accountability (stakeholder) VALUES (:stakeholder)",
              {"stakeholder":stakeholder})
        db.commit()
    return render_template('home.html')
