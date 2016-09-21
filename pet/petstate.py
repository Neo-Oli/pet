# coding=utf-8
import datetime,json,os,math
class petstate(object):


	def load(self):
		state={}
		if os.path.exists(self.settings.configpath+self.savefile):
			with open (self.settings.configpath+self.savefile, "r") as openfile:
				statedata=openfile.read()
				if statedata:
					state=json.loads(statedata)
		self.state=state

# Save the current state to the savefile
	def save(self,savefile):
		with open (self.settings.configpath+savefile, "w") as openfile:
			openfile.write(json.dumps(self.state))


# Generates a new state, give it a name
	def birth(self,name,time):
		if not name:
			self.error.append(self.text("error-noname"))
		else:
			self.state={}
			self.state["name"]=name
			self.state["timeofbirth"]=time
			self.message.append(self.text("born"))

	def initialize(self,key,value):
		if not key in self.state:
			self.state[key]=value
	
	def getage(self,time):
		age=time-self.state["timeofbirth"]
		ageindays=math.floor(round(age)/60/60/24)
		self.message.append(self.text("age").replace("%t", str(ageindays)))

	def do(self,action="status"):
		# fix library calls sending empty strings
		if not action:
			action="status"
		action=action.lower()
		done=False
		if not self.error:
			time=float(datetime.datetime.now().strftime("%s.%f"))
			if action=="new":
				if "dead" in self.state:
					dead=self.state["dead"]
				else:
					dead=False
				if "name" not in self.state or dead:
					self.birth(self.settings.name,time)
					self.do()
				else:
					self.error.append(self.text("error-petexists"))
			elif not self.state:
					self.error.append(self.text("error-nostate"))
			else:
				if action in ["food","play","clean","learn","sleep","heal"]:
					self.getstatus(time)
					self.wait(action,time)
					self.getstatus(time)
				elif action == "cancel":
					# Force stop action
					self.getstatus(time,True)
				elif action=="status":
					self.getstatus(time)
				elif action=="age":
					self.getage(time)
					self.do()
				else:

					for key in ["food","play","sleep","heal","learn","cancel","clean","age"]:
						if action in self.settings.lang[key+"alt"]:
							self.do(key)
							done=True
					if not done:
						self.error.append(self.text("error-action"))

	def testaction(self,time, lasttime,forcestop=False):
		if self.state["action"]=="heal" and forcestop:
			self.message.append(self.text("error-forcestop"))
		timediff=time - self.state["actiontime"]
		timereq=self.settings.config[self.state["action"]+"time"] * self.settings.config["timemodifier"] 
		if self.settings.timeskip:
			timereq=0
		if timereq==0:
			percent=1
		else:
			percent=timediff/timereq
		if percent>1:
			percent=1
		if timediff>=timereq or forcestop:
			if self.state["action"]=="heal" and not forcestop:
				self.state["sick"]=False
				for key in ["food","sleep","clean","play","learn"]:
					self.state[key]=self.settings.config[key+"afterheal"]
			else:
				if self.state[self.state["action"]]<0:
					self.state[self.state["action"]]=0
				self.state[self.state["action"]]=self.state[self.state["action"]]+(self.settings.config[self.state["action"]+"improve"]*percent)
				self.effect(percent)
			lasttime=self.state["actiontime"]+timereq
			self.state["action"]=None
		return lasttime

	def sick(self,state,time):
		state["sick"]=True
		state["sicktime"]=time
		state["action"]=None
		self.message.append(self.text("sick-message"))
		return state

	def getstatus(self,time,forcestop=False):
		state=self.initialize("time",time)
		state=self.initialize("sick",False)
		state=self.initialize("sicktime",0)
		state=self.initialize("action",None)
		state=self.initialize("actiontime",0)
		state=self.initialize("dead",False)
		state=self.initialize("grow",0)
		state=self.initialize("growtime",time)


		lasttime=self.state["time"]
		self.state["time"]=time
		timediff=self.state["time"]-lasttime
		if self.state["action"]:
			# Don't deteriorate during actions
			lasttime=self.testaction(time,lasttime,forcestop)
			timediff=self.state["time"]-lasttime
		if not self.state["dead"]:
			for key in ["food","sleep","clean","play","learn"]:
				self.initialize(key,self.settings.config["defaultvalue"])
				self.state[key]=self.state[key]-((timediff / self.settings.config["timemodifier"]) * self.settings.config[key+"mod"])
				if key+"sick" in self.settings.config and not self.state["sick"]:
					low,high,lowsick,highsick=self.settings.config[key+"sick"].split(",")
					if self.state[key]<int(low):
						if lowsick.lower()=="true":
							self.sick(self.state,time)
						else:
							self.state[key]=0
					if self.state[key]>int(high):
						if highsick.lower()=="true":
							self.sick(self.state,time)
						else:
							self.state[key]=100

			if ((self.getmood()=="happy" and self.state["time"]-self.state["growtime"]>self.settings.config["growtime"]*self.settings.config["timemodifier"]) or self.settings.grow) and self.state["grow"]<self.settings.config["maxgrow"]:
				self.settings.grow=False
				self.state["grow"]+=1
				self.message.append(self.text("grown"))
				self.state["growtime"]=time
			elif time-self.state["sicktime"]>self.settings.config["sicktime"]*self.settings.config["timemodifier"] and self.state["sick"]:
				if not self.state["dead"]:
					self.message.append(self.text("died"))
				self.state["dead"]=True











	def wait(self,action,time):
		if action=="heal" and not self.state["sick"]:
			self.message.append(self.text("notsick"))
		elif not self.state["action"]:
			if not self.state["dead"] and (not self.state["sick"] or action=="heal"):
				self.state["action"]=action
				self.state["actiontime"]=time
		else:
			self.message.append(self.text("busy"))

	def getmood(self):
		if self.state["dead"]:
			mood="dead"
		elif self.state["sick"] and self.state["action"]!="heal":
			mood="sick"
		elif self.state["action"]=="learn":
			mood="learning"
		elif self.state["action"]=="sleep":
			mood="sleeping"
		elif self.state["action"]=="food":
			mood="eating"
		elif self.state["action"]=="play":
			mood="playing"
		elif self.state["action"]=="heal":
			mood="healing"
		elif self.state["action"]=="clean":
			mood="cleaning"
		elif self.state["clean"]<self.settings.config["unhappyat"]:
			mood="dirty"
		elif self.state["sleep"]<self.settings.config["unhappyat"]:
			mood="sleepy"
		elif self.state["food"]<self.settings.config["unhappyat"]:
			mood="hungry"
		elif self.state["play"]<self.settings.config["unhappyat"] or self.state["learn"] < self.settings.config["unhappyat"]:
			mood="sad"
		else:
			mood="happy"
		return mood



	def effect(self,percent):
		for key in ["food","sleep","clean","play","learn"]:
			effectkey=self.state["action"]+"-"+key
			if effectkey in self.settings.config:
				self.state[key]=self.state[key] - (self.settings.config[effectkey]*percent)
			effectkey=self.state["action"]+"+"+key
			if effectkey in self.settings.config:
				self.state[key]=self.state[key] + (self.settings.config[effectkey]*percent)
	
	def __init__(self,savefile,settings):
		self.state={}
		self.message=[]
		self.error=[]
		self.savefile=savefile
		self.settings=settings
	
	def text(self, key):
		text=self.settings.text(key)
		if "name" in self.state:
			text=text.replace("%n", self.state["name"])
		return text
