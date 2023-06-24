from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math
import asyncio
import websockets
import socket
from base64 import b64decode
import wave
import json
from datetime import datetime
import requests
import json
import ast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///potholes.db' #postavljanje baze
db = SQLAlchemy(app) #inicijalizacija baze

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default="user")

    def __repr__(self):
        return '<User %r>' % self.id

class Pothole(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    accel = db.Column(db.Float, nullable=False)
    strength = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return '<Pothole %r>' % self.id
    
with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = User.query.all()
        
        for user in users:
            if user.username == username and user.password == password:
                if user.role == "admin":
                    return redirect('/adminpage')
                else:
                    return redirect('/adminpage')
        
        return render_template('login.html', error='Invalid username or password')
    
    else:
        return render_template('login.html', form_id="login-form")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        new_user = User(username=username, password=password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return render_template('login.html', form_id="login-form") 
    return render_template('register.html', form_id="register-form")

@app.route('/show-potholes', methods=['GET'])
def show_potholes():
    potholes = Pothole.query.all()
    return render_template('adminpage.html', potholes=potholes)

@app.route('/userpage', methods=['GET','POST'])
def userpage():
    if request.method == 'POST':
        # plong = 45.5
        # plat = 45.544343
        # paccel = 666
        # pstr = "Mild"
        # new_pothole = Pothole(longitude = plong, latitude = plat, accel = paccel, strength = pstr)

        with open('server/accelerometer.txt', 'r') as file1, open('server/gyroscope.txt', 'r') as file2, open('server/location.txt', 'r') as file3: 
            for line1, line2, line3 in zip(file1, file2, file3): 
                adict = ast.literal_eval(line1)
                gdict = ast.literal_eval(line2)
                ldict = ast.literal_eval(line3)

                if abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) > 1.5 and abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) < 3:
                    print(abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])))
                    accel = round(math.sqrt(float(adict['z'])**2 + float(adict['x'])**2 +float(adict['y'])**2) *0.1)
                    long = float(ldict['longitude'])
                    lat = float(ldict['latitude'])
                
                    new_pothole = Pothole(strength = 'Mild', accel = accel, longitude = long, latitude = lat)
                    try:
                        db.session.add(new_pothole)
                        db.session.commit()
                        return redirect('/')
                    except:
                        return "There was an issue adding your pothole"

                elif abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) >= 3 and abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) < 6:
                    print(abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])))
                    accel = round(math.sqrt(float(adict['z'])**2 + float(adict['x'])**2 +float(adict['y'])**2) *0.1)
                    long = float(ldict['longitude'])
                    lat = float(ldict['latitude'])
                
                    new_pothole = Pothole(strength = 'Intermediate', accel = accel, longitude = long, latitude = lat)
                    try:
                        db.session.add(new_pothole)
                        db.session.commit()
                        return redirect('/')
                    except:
                        return "There was an issue adding your pothole"
                elif abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) >=6:
                    print(abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])))
                    accel = round(math.sqrt(float(adict['z'])**2 + float(adict['x'])**2 +float(adict['y'])**2) *0.1)
                    long = float(ldict['longitude'])
                    lat = float(ldict['latitude'])
                
                    new_pothole = Pothole(strength = 'Severe', accel = accel, longitude = long, latitude = lat)
                    try:
                        db.session.add(new_pothole)
                        db.session.commit()
                        return redirect('/')
                    except:
                        return "There was an issue adding your pothole"
                else:
                    pass
    else:
        potholes = Pothole.query.order_by(Pothole.strength).all()
        return render_template('userpage.html', potholes = potholes)

@app.route('/adminpage', methods=['GET','POST'])
def adminpage():
    if request.method == 'POST':
        # plong = 45.5
        # plat = 45.544343
        # paccel = 666
        # pstr = "Mild"
        # new_pothole = Pothole(longitude = plong, latitude = plat, accel = paccel, strength = pstr)

        with open('server/accelerometer.txt', 'r') as file1, open('server/gyroscope.txt', 'r') as file2, open('server/location.txt', 'r') as file3: 
            for line1, line2, line3 in zip(file1, file2, file3): 
                adict = ast.literal_eval(line1)
                gdict = ast.literal_eval(line2)
                ldict = ast.literal_eval(line3)

                if abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) > 1.5 and abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) < 3:
                    print(abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])))
                    accel = round(math.sqrt(float(adict['z'])**2 + float(adict['x'])**2 +float(adict['y'])**2) *0.1)
                    long = float(ldict['longitude'])
                    lat = float(ldict['latitude'])
                
                    new_pothole = Pothole(strength = 'Mild', accel = accel, longitude = long, latitude = lat)
                    try:
                        db.session.add(new_pothole)
                        db.session.commit()
                        return redirect('/')
                    except:
                        return "There was an issue adding your pothole"

                elif abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) >= 3 and abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) < 6:
                    print(abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])))
                    accel = round(math.sqrt(float(adict['z'])**2 + float(adict['x'])**2 +float(adict['y'])**2) *0.1)
                    long = float(ldict['longitude'])
                    lat = float(ldict['latitude'])
                
                    new_pothole = Pothole(strength = 'Intermediate', accel = accel, longitude = long, latitude = lat)
                    try:
                        db.session.add(new_pothole)
                        db.session.commit()
                        return redirect('/')
                    except:
                        return "There was an issue adding your pothole"
                elif abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) >=6:
                    print(abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])))
                    accel = round(math.sqrt(float(adict['z'])**2 + float(adict['x'])**2 +float(adict['y'])**2) *0.1)
                    long = float(ldict['longitude'])
                    lat = float(ldict['latitude'])
                
                    new_pothole = Pothole(strength = 'Severe', accel = accel, longitude = long, latitude = lat)
                    try:
                        db.session.add(new_pothole)
                        db.session.commit()
                        return redirect('/')
                    except:
                        return "There was an issue adding your pothole"
                else:
                    pass
    else:
        potholes = Pothole.query.order_by(Pothole.strength).all()
        return render_template('adminpage.html', potholes = potholes)

@app.route('/delete/<int:id>')
def delete(id):
    pothole_to_delete = Pothole.query.get_or_404(id)
    try:
         #SQLAlchemy query API
         db.session.delete(pothole_to_delete)
         db.session.commit()
         return redirect('/adminpage')
    except:
         db.session.rollback()
         return 'There was a problem deleting that pothole'
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
     pothole_to_update = Pothole.query.get_or_404(id)
     if request.method == 'POST':
         pothole_to_update.longitude = request.form['longitude']
         pothole_to_update.latitude = request.form['latitude']
         pothole_to_update.velocity = request.form['velocity']
         pothole_to_update.strength = request.form['strength']
         try:
             db.session.commit()
             return redirect('/')
         except:
             return 'There was an issue updating your pothole'
     else:
         return render_template('update.html', pothole=pothole_to_update)

if __name__ == '__main__':
    app.run(debug=True)