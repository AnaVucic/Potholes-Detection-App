from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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


class Pothole(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    accel = db.Column(db.Float, nullable=False)
    strength = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return '<Pothole %r>' % self.id
    
# with app.app_context():
#    db.create_all()




@app.route('/', methods=['GET','POST'])
def index():
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

                if abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])) > 1.5:
                    print(abs(float(gdict['x'])) + abs(float(gdict['y'])) + abs(float(gdict['z'])))
                    accel = abs(float(adict['z']))
                    long = float(ldict['longitude'])
                    lat = float(ldict['latitude'])
                
                    new_pothole = Pothole(strength = 'Mild', accel = accel, longitude = long, latitude = lat)
                    try:
                        db.session.add(new_pothole)
                        db.session.commit()
                        return redirect('/')
                    except:
                        return "There was an issue adding your pothole"
    else:
        return render_template('index.html')

# @app.route('/delete/<int:id>')
# def delete(id):
#     book_to_delete = Book.query.get_or_404(id)
#     try:
#         #SQLAlchemy query API
#         db.session.delete(book_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that book'
    

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     book_to_update = Book.query.get_or_404(id)
#     if request.method == 'POST':
#         book_to_update.title = request.form['title']
#         book_to_update.author = request.form['author']
#         book_to_update.published = datetime. strptime(request.form['published'], '%Y-%m-%d')
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your book'
#     else:
#         return render_template('update.html', book=book_to_update)

if __name__ == '__main__':
    app.run(debug=True)