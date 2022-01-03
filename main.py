#-*- encoding: utf-8 -*-
from flask import Flask, redirect, jsonify,  url_for, render_template, session, request
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
from wtforms.fields import TextAreaField, StringField
from datetime import datetime, timedelta
import time
from apps.initdata import GetContracts 

app = Flask(__name__)
app.config['SECRET_KEY'] = '#$%^&*'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/monitor',methods=['GET'])
def monitor():
    dtmsg = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    contracts = GetContracts()
    contracts.run()
    data = {
        'dtmsg':dtmsg,
        'long_groups':contracts.long_groups, 
        'short_groups':contracts.short_groups,
        'change_counts':contracts.change_counts,
        'exchange_diff':contracts.exchange_overviews[0],
        'exchange_overviews':contracts.exchange_overviews[1],
        'long_stocks':contracts.long_stocks, 
        'short_stocks':contracts.short_stocks,
        'amount_top20':contracts.amount_top20,
        'marketvalue_top':contracts.marketvalue_top,
        
    }
    
    return render_template('index.html', data=data)

@app.route('/startmonitor',methods=['GET'])
def startmonitor():
    dtmsg = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    contracts = GetContracts()
    contracts.run()
    data = {
        'dtmsg':dtmsg,
        'change_counts':contracts.change_counts,
        'exchange_diff':contracts.exchange_overviews[0],
        'exchange_overviews':contracts.exchange_overviews[1],
        'long_groups':contracts.long_groups, 
        'short_groups':contracts.short_groups,
        'long_stocks':contracts.long_stocks, 
        'short_stocks':contracts.short_stocks,
        'amount_top20':contracts.amount_top20,
        'marketvalue_top':contracts.marketvalue_top,

    }
    return data
