# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.

class Stock(models.Model):
	stock_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=10)
	price = models.CharField(max_length=10)
	volume = models.CharField(max_length=10)
	perct = models.CharField(max_length=10)
	high = models.CharField(max_length=10)
	low = models.CharField(max_length=10)
	prev = models.CharField(max_length=10)



	def __str__(self):
		return self.name



class tempUser(models.Model):
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	tp = models.CharField(max_length=100)
	pic = models.ImageField(upload_to = 'media/',blank=True,null=True)


	def __str__(self):
		return self.email


class wishlist(models.Model):

	user = models.ForeignKey(User)
	stock = models.ForeignKey(Stock)


class user_profile(models.Model):
	"""docstring for user_profile"""
	pic = models.ImageField(upload_to = 'media/',blank=True,null=True)
	user_detail = models.ForeignKey(User)

	
