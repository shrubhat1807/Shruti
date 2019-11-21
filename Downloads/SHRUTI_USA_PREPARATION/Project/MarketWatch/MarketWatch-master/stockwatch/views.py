# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render,redirect
from django.http import HttpResponse

#from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.globalstockquotes import GlobalStockQuotes
import json
#from pprint import pprint

#from nsetools import Nse
from nasdaq_stock_quote import Share

from .models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as auth_logout

from email.MIMEMultipart import MIMEMultipart
from .safe import usermail,upassword
from email.MIMEText import MIMEText
import smtplib
import hashlib
import ast
import datetime
from django.http import JsonResponse
import requests



# Create your views here.


def home(request):
	#gsq = TimeSeries(key='EODCNM4ZVVCTQPY0')
	# data, meta_data = gsq.get_intraday(symbol='NSE:INFY')
	# pprint(data)
    if request.user.is_authenticated():





		a =[
			# "DDD",
			# "MMM",
			# "WBAI",
			# "WUBA",
			# # "AHC",
			# "ATEN",
			# "AAC",
			# # "AIR",
			# "AAN",
			# "ABB",
			# "ABT",
			# "ABBV",
			# "ANF",
			# "GCH",
			# "JEQ",
			# "SGF",
			# "ABM",
			# "AKR",
			# # "ACN",
			# "ACCO",
			# # "ATV",
			# "ATU",
			# "AYI",
			# "GOLF",
			# "ADX",
			# "PEO",
			# "AGRO",
			# "ADNT",
			# "ATGE",
			# "AAP",
			# "ADSW",
			# # "WMS",
			# "ASX",
			# "ASIX",
			# "AAV",
			# "AVK",
			# # "AGC",
			# "LCM",
			# "ACM",
			# "ANW",
			# "AEB",
			# "AED",
			# "AEG",
			# # "AEH",
			# "AEK",
			# "AER",
			# # "HIVE",
			# "AJRD",
			# "AET",
			# "AMG",

		] 
		for i in a:
			share = Share(i)
			prev = share.get_prev_close()
			price = share.get_price()
			name = share.get_name()
			volume = share.get_volume()
			perct = share.get_percent_change()
			high = share.get_day_high()
			low = share.get_day_low()
			perct = float(perct)
			perct = perct*100
			perct = str(perct)
			print name
			if Stock.objects.filter(name=i).exists():
				stock = Stock.objects.filter(name=i).update(name=name,price=price,volume=volume,perct=perct,high=high,low=low,prev=prev)
			else:

				stock = Stock.objects.create(name=name,price=price,volume=volume,perct=perct,high=high,low=low,prev=prev)
				stock.save()


		stock = Stock.objects.all()
		print request.user.first_name
		print request.user
			

		# print request.user
		# user_pro = user_profile.objects.get(user_detail=request.user)

		# nse = Nse()

		# all_stock_codes = nse.get_stock_codes()
		# top_gainers = nse.get_top_gainers()
		# top_gainers = json.dumps(top_gainers)
		# print top_gainers
		user_pro = user_profile.objects.get(user_detail=request.user)
		return render(request,"home.html",{'stock':stock,'user':request.user ,'user_pro' : user_pro})



def register(request):
	if request.method == 'POST':
		fname = request.POST['fname']
		lname = request.POST['lname']
		email = request.POST['email']
		password = request.POST['password']
		try:
			pic = request.FILES['pic']

		except:
			pass
		
		hash=hashlib.sha1()
                now=datetime.datetime.now()
                hash.update(str(now)+email+'asdasdas')
                tp=hash.hexdigest()
                print tp
		
		user = tempUser.objects.create(fname=fname,lname=lname,email=email,password=password,tp=tp,pic=pic)
		
		user.save()
		print user

		fromaddr=usermail
                toaddr=email
                print fromaddr
                print toaddr
                msg=MIMEMultipart()
                msg['From']=fromaddr
                msg['To']=toaddr
                msg['Subject']='Confirmational Email'
                domain = request.get_host()
                scheme = request.is_secure() and "https" or "http"
                body = "Please Click On The Link To complete registration: {0}://{1}/{2}/registeration_comp".format(scheme,domain,tp) 
                part1 = MIMEText(body, 'plain')
                msg.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, upassword)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                return render(request,'b.html')
	else:

		return render(request,"login.html")


def login_site(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username = email, password = password)
		if user:
			login(request, user)
			return redirect('/home/')
		else:
			return HttpResponse('invalid')

	else:	
		return render(request, 'login.html')
	
def registeration_comp(request,p):
	tp=p
	u = tempUser.objects.get(tp=tp)
	user = User.objects.create(username=u.email,first_name=u.fname,last_name=u.lname,email=u.email)
	user.set_password(u.password)
	user.save()
	user_pro = user_profile.objects.create(user_detail=user,pic=u.pic)
	user_pro.save()
	tempUser.objects.filter(tp=tp).delete()

	login(request, user)
	return redirect('/home/')

def wishlisttable(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			s = json.loads(request.body.decode('utf-8'))
			name = s['name']
			stock = Stock.objects.get(name=name)
			print stock
			print request.user
			if wishlist.objects.filter(stock=stock,user=request.user).exists():
				pass
			else:
				Wishlist = wishlist.objects.create(user=request.user,stock=stock)
				Wishlist.save()
			return JsonResponse({'success' : 'true'})
		else:
			return HttpResponse("dfgdghdh")
	else:
		return redirect('/login_site/')

def watchlist(request):
	if request.user.is_authenticated():
		print request.user
		Wishlist = wishlist.objects.filter(user=request.user)

		user_pro = user_profile.objects.get(user_detail=request.user)
		
		return render(request,"watchlist.html",{'wishlist' : Wishlist,'user_pro' : user_pro })

	else:
		return redirect('/login_site/')



def detail(request,p):
	if request.user.is_authenticated():
		print p
		stock = Stock.objects.get(stock_id=p)
		print stock
		r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock.name+'&apikey=EODCNM4ZVVCTQPY0')
		stock_json = r.json()
		print stock_json['Time Series (Daily)']
		stock_detail = json.dumps(stock_json['Time Series (Daily)'])
		user_pro = user_profile.objects.get(user_detail=request.user)
		return render(request,"index.html",{'stock':stock,'stock_detail':stock_detail,'user_pro' : user_pro})



	else:
		return redirect('/login/')


def news(request):
	if request.user.is_authenticated():
		description=[]
		title=[]
		url=[]
		urltoimg=[]
		news = requests.get('https://newsapi.org/v1/articles?source=cnbc&sortBy=top&apiKey=e469736fcf9c4b22bf6c50657ea1e9a8')
		news = news.json()
		articles = news['articles']
		print articles

		user_pro = user_profile.objects.get(user_detail=request.user)
		return render(request,"news.html",{'articles' : articles,'user_pro' : user_pro})
	else:
		return redirect('/login_site/')


def remove(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			s = json.loads(request.body.decode('utf-8'))
			name = s['name']
			stock = Stock.objects.get(name=name)
			print stock
			print request.user
			rstock = wishlist.objects.get(user=request.user,stock=stock)
			rstock.delete()
		return JsonResponse({'success': 'true'})
	else:
		return redirect('/login_site/')


def contact(request):
	if request.user.is_authenticated():
		
		if request.method == 'POST' :
			name = request.POST['name']
			email = request.POST['email']
			message = request.POST['message']
			number = request.POST['number']
			fromaddr=usermail
		        toaddr=usermail
		        print fromaddr
		        print toaddr
		        msg=MIMEMultipart()
		        msg['From']=fromaddr
		        msg['To']=toaddr
		        msg['Subject']='Feedback Email'
		        domain = request.get_host()
		        scheme = request.is_secure() and "https" or "http"
		        body = "Name: {0} \n Email: {1} \n Message: {2} \n Contact Number: {3}".format(name,email,message,number) 
		        part1 = MIMEText(body, 'plain')
		        msg.attach(MIMEText(body, 'plain'))
		        server = smtplib.SMTP('smtp.gmail.com', 587)
		        server.starttls()
		        server.login(fromaddr, upassword)
		        text = msg.as_string()
		        server.sendmail(fromaddr, toaddr, text)
		        server.quit()
			return render(request,"feedback.html")

		else:
			user_pro = user_profile.objects.get(user_detail=request.user)
			return render(request,"contact.html",{'user_pro' : user_pro})

		
	else:
		return redirect('/login_site/')



def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
    else:
        return HttpResponse("invalid")
    
    return render(request,'login.html')


