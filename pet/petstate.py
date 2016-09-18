import datetime,json,sys
class petstate(object):


	def load(self, savefile):
		state={}
		try:
			with open (self.settings.configpath+savefile, "r") as openfile:
				statedata=openfile.read()
				if statedata:
					state=json.loads(statedata)
		except FileNotFoundError:
			pass
		self.state=state

# Save the current state to the savefile
	def save(self,savefile):
		with open (self.settings.configpath+savefile, "w") as openfile:
			openfile.write(json.dumps(self.state))


# Generates a new state, give it a name
	def birth(self,name):
		if not name:
			print(self.settings.lang["error-noname"])
			import sys
			sys.exit(1)
		self.state={}
		self.state["name"]=name
		self.message.append(self.settings.lang["born"])

	def initialize(self,key,value):
		if not key in self.state:
			self.state[key]=value

	def do(self,action):
		time=float(datetime.datetime.now().strftime("%s.%f"))
		if action=="new":
			if "dead" in self.state:
				dead=self.state["dead"]
			else:
				dead=False
			if "name" not in self.state and not dead:
				self.birth(self.settings.name)
				self.getstatus(time)
			else:
				print(self.settings.lang["error-petexists"])
				sys.exit(1)
		elif not self.state:
				print(self.settings.lang["error-nostate"])
				sys.exit(1)
		else:
			if action in ["food","play","clean","learn","sleep","heal"]:
				self.getstatus(time)
				self.wait(action,time)
				self.getstatus(time)
			elif action in ["feed","eat","Fd"]:
				self.do("food")
			elif action=="fun":
				self.do("play")
			elif action in ["teach","lrn"]:
				self.do("learn")
			elif action in ["cln","wash"]:
				self.do("clean")
			elif action in ["cancel", "stop", "wake","interrupt"]:
				# Force stop action
				self.getstatus(time,True)
			elif action=="status":
				self.getstatus(time)
			elif action:
				print(self.settings.lang["error-action"])
				sys.exit(1)
			else:
				self.do("status")

	def testaction(self,time, forcestop=False):
		if self.state["action"]=="heal" and forcestop:
			self.error.append(self.settings.lang["error_forcestop"])
		timediff=time - self.state["actiontime"]
		timereq=self.settings.config[self.state["action"]+"time"] * self.settings.config["timemodifier"] 
		percent=timediff/timereq
		if percent>1:
			percent=1
		if timediff>timereq or forcestop:
			if self.state["action"]=="heal" and not forcestop:
				self.state["sick"]=False
				for key in ["food","sleep","clean","play","learn"]:
					self.state[key]=self.settings.config[key+"afterheal"]
			else:
				if self.state[self.state["action"]]<0:
					self.state[self.state["action"]]=0
				self.state[self.state["action"]]=self.state[self.state["action"]]+(self.settings.config[self.state["action"]+"improve"]*percent)
				self.decrease(percent)
			self.state["action"]=None

	def sick(self,state,time):
		state["sick"]=True
		state["sicktime"]=time
		state["action"]=None
		self.message.append(self.settings.lang["sick-message"])
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
			timediff=0
			self.testaction(time,forcestop)
		if not self.state["dead"]:
			for key in ["food","sleep","clean","play","learn"]:
				self.initialize(key,50)
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

			if self.getmood()=="happy" and self.state["time"]-self.state["growtime"]>self.settings.config["growtime"]*self.settings.config["timemodifier"] and self.state["grow"]<self.settings.config["maxgrow"] or self.settings.grow:
				self.state["grow"]+=1
				self.message.append(self.settings.lang["grown"])
		elif time-self.state["sicktime"]>self.settings.config["sicktime"]*self.settings.config["timemodifier"]:
			if not self.state["dead"]:
				self.error.append(settings.lang["died"])
			self.state["dead"]=True













	def wait(self,action,time):
		if action=="heal" and not self.state["sick"]:
			self.error.append(settings.lang["notsick"])
		elif not self.state["action"]:
			if not self.state["dead"] and (not self.state["sick"] or action=="heal"):
				self.state["action"]=action
				self.state["actiontime"]=time
		else:
			self.error.append(self.settings.lang["busy"])

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



	def decrease(self,percent):
		for key in ["food","sleep","clean","play","learn"]:
			decreasekey=self.state["action"]+"-"+key
			if decreasekey in self.settings.config:
				self.state[key]=self.state[key] - (self.settings.config[decreasekey]*percent)
	
	def __init__(self,savefile,settings):
		self.state={}
		self.message=[]
		self.error=[]
		self.savefile=savefile
		self.settings=settings
