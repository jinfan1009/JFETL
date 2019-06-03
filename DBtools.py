import os,sys

import mysql.connector

class DB:
	def __init__(self):
		config ={'host':'localhost',
				'user':'root',
				'password':'root',
				'port':3306,
				'database':'bmi_old_and_new',
				'charset':'utf8',
				}
		self.cx=mysql.connector.connect( **config )
		self.cursor=self.cx.cursor()
	def update(self,sql):
		try:
			self.cursor.execute(sql)
			self.cx.commit()
		except :
			print ('error')
	def update_trans(self,sql):
		try:
			self.cursor.execute(sql)
		except Exception as e:
			print (e)
			pass
	def query(self,sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()
	def commit(self):
		self.cx.commit()
	def close(self):
		self.cursor.close()
		self.cx.close()
