from flask import Blueprint, jsonify, render_template,request,flash
from flask_login import login_required,current_user
from .models import Note
from . import db
from .compound import compound_interest
import json
import requests
 
views = Blueprint('views',__name__)

@views.route("/",methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')
        if len(note)<1:
            flash('Note is empty',category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added',category='success')
    return render_template('home.html', user=current_user)
@views.route("/compound",methods=['GET','POST'])
@login_required
def compound():
    amount=0
    if request.method=='POST':
        try:
            principal=float(request.form.get('principal'))
            interest=float(request.form.get('interest'))
            time=float(request.form.get('time'))
        except:
            principal=0
            interest=0
            time=0    
        amount=compound_interest(principal=principal,interest=interest,time=time)
    return render_template('compound.html', user=current_user,amount=amount)
@views.route("/stocks",methods=['GET','POST'])
@login_required
def stocks():
    value=0
    url="https://api.freeapi.app/api/v1/public/stocks/"
    if request.method=='POST':
        symbol=request.form.get('symbol')
        response=requests.get(url+symbol)
        data=response.json()
        print(data["data"]["CurrentPrice"])
        value=data["data"]["CurrentPrice"]
    return render_template('stocks.html', user=current_user,value=value)
@views.route('/delete-note',methods=['POST'])
def delete_note():
    note =json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
