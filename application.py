import datetime
import time
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import scoped_session,sessionmaker
engine=create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
db=scoped_session(sessionmaker(bind=engine))

class text():
	def __init__(self):
		print("1..sign up...")
		print("2..sign in...")
		a=int(input("choice:"))
		if a==1:
			text.signup(self)
		elif a==2:
			text.signin(self)
		else:
			print("invalid choice!")

	def signup(self):
		engine=create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
		db=scoped_session(sessionmaker(bind=engine))
		
		uname=str(input("enter username:"))
		password=str(input("set password:"))
		name=str(input("enter name:"))
		dob=str(input("enter dob:"))
		db.execute(f"insert into users (uname,password) values (:uname,:password);",{"uname":uname,"password":password})
		db.commit()

		u=db.execute(f"select uno from users where uname=:uname;",{"uname":uname})
		for u in u:
			uno=u[0]
		db.execute(f"insert into users_info (uno,name,friends) values (:uno,:name,:friends);",{"uno":uno,"name":name,"friends":0})
		db.commit()

		db.execute(f"call inse(:uno,:friends,:dob);",{"uno":uno,"friends":"","dob":dob})
		db.commit()

		db.execute("commit")
		db.execute(f"create database {uname};")

		engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{uname}")
		db=scoped_session(sessionmaker(bind=engine))
			
		db.execute(f"create table friends (uno integer primary key,friends varchar);")			
		db.execute(f"create table request_sent (to_ integer primary key,status varchar);")
		db.execute(f"create table request_recieved (from_ integer primary key,status varchar);")
		db.commit()
		print("signup successfull...")

		text()

	def signin(self):
		engine=create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
		db=scoped_session(sessionmaker(bind=engine))

		uname=str(input("username:"))
		password=str(input("password:"))
		user=db.execute("select * from users join users_info on users.uno=users_info.uno where uname=:uname and password=:password;",{"uname":uname,"password":password})
		if user is None:	
			print("you don't have an account!!!")
		else:
			for user in user:
				user_(user)

class user_():
	def __init__(self,user):
		os.system("cls")
		print(f"\t\t\t hey {user.name} @ {user.uname}\n")
		print("1..initiate chat...\n2..send request...\n3..notifications...\n4..people...\n5..search...")
		q=int(input(":"))
		if q==1:
			user_.chat(self,user)
		elif q==2:
			user_.request(self,user)
		elif q==3:
			user_.notifications(self,user)
		elif q==4:
			user_.people(self,user)
		elif q==5:
			user_.search(self,user)

	def chat(self,user):
		engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{user.uname}")
		db=scoped_session(sessionmaker(bind=engine))

		f=[]
		friends=db.execute(f"select * from friends;")
		print("friends")
		for friends in friends:
			f.append(friends.friends)
		for a in f:
			print(a)	

		chat_with=str(input("chat with:"))
		if chat_with in f:
			user_.chat_(self,user,chat_with)

		else:
			print(f"you're not friends with {chat_with}")
			user_.chat(self,user)

	def chat_(self,user,chat_with):
		ip=""
		while ip!="exit":
			os.system("cls")
			print(f"you're in chatbox with {chat_with}")

			engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{chat_with}")
			db=scoped_session(sessionmaker(bind=engine))

			data_2=db.execute(f"select * from {chat_with}{user.uname}")

			engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{user.uname}")
			db=scoped_session(sessionmaker(bind=engine))		
			
			data_1=db.execute(f"select * from {user.uname}{chat_with};")

			data={}
			for data_1 in data_1:
				data[data_1.time_stamp]="\t\t"+data_1.texts
			for data_2 in data_2:
				data[data_2.time_stamp]=data_2.texts

			for a in sorted(data):
				print(data[a])

			time.sleep(0.5)

			ip=str(input("\n:"))
			if ip=="exit":
				break
			ip_ts=datetime.datetime.now()
			db.execute(f"insert into {user.uname}{chat_with} (time_stamp,texts) values (:ip_ts,:ip);",{"ip_ts":ip_ts,"ip":ip})
			db.commit()
		user_(user)

	def request(self,user):
		engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")
		db=scoped_session(sessionmaker(bind=engine))		

		to=db.execute("select * from users where uname=:uname;",{"uname":str(input("send request to:"))})
		for to in to:
			to_=to
		if to_ is not None:
			engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{user.uname}")
			db=scoped_session(sessionmaker(bind=engine))		

			db.execute(f"insert into request_sent (to_,status) values (:to_,:status);",{"to_":to_.uno,"status":"pending"})
			db.commit()

			engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{to_.uname}")
			db=scoped_session(sessionmaker(bind=engine))

			db.execute(f"insert into request_recieved (from_,status) values (:from_,:status);",{"from_":user.uno,"status":"pending"})
			db.commit()

			engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")
			db=scoped_session(sessionmaker(bind=engine))

			print("request sent...")
		if to_ is None:
			print("this user doesnt exist!!!")

		a=str(input("go home (y/n):"))
		if a=="y":
			user_(user)
		elif a=="n":
			chat_.request(user)

	def notifications(self,user):
		engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{user.uname}")
		db=scoped_session(sessionmaker(bind=engine))

		a=db.execute(f"select * from request_recieved;")
		
		if a is not None:
			for aa in a:

				engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")
				db=scoped_session(sessionmaker(bind=engine))			

				aaaa=db.execute(f"select * from users join users_info on users.uno=users_info.uno where users.uno={aa.from_}")
				for aaaa in aaaa:
					aaa=aaaa

				print(f"friend request from {aaa.name} @ {aaa.uname}\n")
				ad=str(input("y/n:"))
				if ad=="y":

					engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{user.uname}")
					db=scoped_session(sessionmaker(bind=engine))

					db.execute(f"create table {user.uname}{aaa.uname} (time_stamp varchar not null,texts varchar not null);")
					db.commit()
					db.execute(f"delete from request_recieved where from_=:uno;",{"uno":aaa.uno})
					db.commit()
					db.execute(f"insert into friends (uno,friends) values (:uno,:friends);",{"uno":aaa.uno,"friends":aaa.uname})
					db.commit()

					engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{aaa.uname}")
					db=scoped_session(sessionmaker(bind=engine))

					db.execute(f"create table {aaa.uname}{user.uname} (time_stamp varchar not null,texts varchar);")
					db.commit()
					db.execute(f"delete from request_sent where to_=:uno;",{"uno":user.uno})
					db.commit()
					db.execute(f"insert into friends (uno,friends) values (:uno,:friends);",{"uno":user.uno,"friends":user.uname})
					db.commit()

					engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")
					db=scoped_session(sessionmaker(bind=engine))

					ff=db.execute(f"select friends from users_info where uno=:uno;",{"uno":user.uno})
					for ff in ff:
						fff=ff[0]
					db.execute(f"update users_info set friends=:f where uno=:u",{"f":fff+1,"u":user.uno})
					db.commit()

					ff=db.execute(f"select friends from users_info where uno=:uno",{"uno":aaa.uno})
					for ff in ff:
						fff=ff[0]
					db.execute(f"update users_info set friends=:f where uno=:u",{"f":fff+1,"u":aaa.uno})
					db.commit()

					old=db.execute(f"select * from users_info_ where uno=:uno;",{"uno":user.uno})
					for old in old:
						o=old
					new=o.friends+(",")+aaa.name+(" @ ")+aaa.uname
					db.execute(f"update users_info_ set friends=:fr where uno=:uno;",{"fr":new,"uno":user.uno})
					db.commit()

					oldd=db.execute(f"select * from users_info_ where uno=:uno;",{"uno":aaa.uno})
					for oldd in oldd:
						oo=old
					new=oo.friends+(",")+user.name+(" @ ")+user.uname
					db.execute(f"update users_info_ set friends=:fr where uno=:uno;",{"fr":new,"uno":aaa.uno})
					db.commit()

				elif ad=="n":
					engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{user.uname}")
					db=scoped_session(sessionmaker(bind=engine))

					db.execute(f"delete from request_recieved where from_=:from;",{"from":aaa.uno})	
					db.commit()	

					engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{aaa.uname}")
					db=scoped_session(sessionmaker(bind=engine))

					db.execute(f"delete from request_sent where to_=:to;",{"to":user.uno})	
					db.commit()	
				else:
					print("wrong choice")	
		else:
			print("no notifications")
		
		r=str(input("return home?(y/n):"))
		if r=="y":
			user_(user)

	def people(self,user):

		os.system("cls")

		engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/{user.uname}")
		db=scoped_session(sessionmaker(bind=engine))

		myf=db.execute(f"select * from friends;")

		engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")
		db=scoped_session(sessionmaker(bind=engine))

		print(f"\t my friends")
		for myf in myf:
			f=myf[0]
			my=db.execute(f"select * from users join users_info on users.uno=users_info.uno where users.uno=:uno;",{"uno":f})
			for my in my:

				print(f"{my.name} @ {my.uname}")

		people=db.execute(f"select * from users join users_info on users.uno=users_info.uno;")
		
		print(f"\n\npeople\t\t\tfriends")
		for people in people:
			print(f"{people.name} @ {people.uname} \t\t {people.friends}\t")

		print(f"\n1..return home...\n2..filter...\n")
		i=int(input(":"))
		if i==1:
			user_(user)
		if i==2:
			nof=int(input(f"filter by number of friends : "))

			fil=db.execute(f"select * from users join users_info on users.uno=users_info.uno where users.uno in (select uno from users_info where friends=:friends);",{"friends":nof})
			print(f"people\t\tfriends")
			for fil in fil:
				print(f"{fil.name} @ {fil.uname} \t\t {fil.friends}\t")

		gh=str(input("\ngo home (y/n):"))
		if gh=="y":
			user_(user)

	def search(self,user):
		os.system("cls")

		engine=create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")
		db=scoped_session(sessionmaker(bind=engine))	

		s=str(input("search:"))

		puser=db.execute(f"select * from users join users_info on users.uno=users_info.uno where users.uname=:uun;",{"uun":s})	
		for puser in puser:
			pu=puser
		pui=db.execute(f"select * from users_info_ where uno=:no;",{"no":pu.uno})

		print(f"\n\t{puser.name} @ {puser.uname}\n")
		print(f"friends....")
		for pui in pui:
			f=pui.friends
		ff=f.split(",")
		for ff in ff:
			print(ff)

		print("\nBirthday..")
		print(pui.dob)

		gh=str(input("\ngo home (y/n):"))
		if gh=="y":
			user_(user)

obj=text()