# coding=utf-8
from pet import interfacehelper
import datetime,sys
from pkg_resources import resource_stream, Requirement
import time
import os
class interface():
	
	def showstatus(self):
		sep=" "
		statout=" "
		if self.pet.state["dead"]==True:
			statout+=self.settings.lang["dead"]+sep
		elif self.pet.state["sick"]==True and self.pet.state["action"]!="heal":
			statout+=self.settings.lang["sick"]+sep
		else:
			if self.pet.state["action"]:
				timeleft=(self.settings.config[self.pet.state["action"]+"time"]*self.settings.config["timemodifier"]) - (self.pet.state["time"] - self.pet.state["actiontime"]) 
				self.interfacemessages.append(self.settings.lang["remainingtime"]+":"+str(datetime.timedelta(seconds=round(timeleft))))
			statout="Fd:{} zZz:{} cln:{} fun:{} lrn:{}".format(
					interfacehelper.displayvalue(self.pet.state["food"]),
					interfacehelper.displayvalue(self.pet.state["sleep"]),
					interfacehelper.displayvalue(self.pet.state["clean"]),
					interfacehelper.displayvalue(self.pet.state["play"]),
					interfacehelper.displayvalue(self.pet.state["learn"]))
		return statout

	def showgraphics(self):
		global graphout
		mood=self.pet.getmood()
		run=True
		i=0
		while run:
			graphic=self.parsexpm(self.pet.state["grow"],mood,i)
			if not graphic:
				run=False
			else:
				i+=1
				output="{}{}".format("\033[6;3H",graphic)
				print(output)
				time.sleep(1)
		return ""



	def __init__(self,pet,settings):
		self.interfacemessages=[]
		self.pet=pet
		self.settings=settings
		self.graphics={}
	
	def output(self, shortmode):
		graphout=self.showgraphics()	
	
		
	def parsexpm(self,size,mood,frame):
		filename=	"graphics/set-1/{}-{}-{}.xpm".format(mood,size,frame)
		if filename in self.graphics:
			return self.graphics[filename]
		try:
			xpm  = resource_stream(Requirement.parse("pet"), filename).read().decode("utf-8")
		except FileNotFoundError:
			return False
		lines=xpm.split('\n')
		pixels=False
		fileinfo=False
		noarray=[]
		yesarray=[]
		graphics=""
		for line in lines:
			charsinline=list(line)
			try:
				wordsinline=line.split(' ')
				if not pixels:
					if line=="/* pixels */":
						pixels=True
					if not charsinline[0]=="/":
						if not wordsinline[0]=="static":
							if charsinline[3]=="c":
								if charsinline[1]==" ":
									wordnum=3
								else:
									wordnum=2
								if wordsinline[wordnum].lower()[:-2] in ["none","black","000000","000"]:
									yesarray.append(charsinline[1])
								else:
									noarray.append(charsinline[1])
				else:
					if line=="};":
						pixels=False
					else:
						line=line.replace("\"","")
						line=line.replace(",","")
						for char in yesarray:
							line=line.replace(char,self.settings.config["graphicschar"])
						for char in noarray:
							line=line.replace(char,self.settings.config["graphicsnochar"])
						graphics="{}{}\n".format(graphics,line)
			except IndexError:
				pass
			
		self.graphics[filename]=graphics
		return graphics	

	def interface(self, action, shortmode):
		os.system("tput civis")
		os.system("clear")
		while True:
			self.pet.do(action)
			if self.pet.error:
				return(interfacehelper.parsemessages(self.pet.error),True)
			if self.pet.error:
				error=True
			else:
				error=False
			self.output(shortmode),error
		return "",False
			
