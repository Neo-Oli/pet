# coding=utf-8
from pet import interfacehelper
import datetime,sys
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
		graphic=self.graphics[self.pet.state["grow"]][mood]
		# graphic=graphic.ljust(7)
		return graphic



	def __init__(self,pet,settings):
		self.interfacemessages=[]
		self.pet=pet
		self.settings=settings
	
	def output(self, shortmode):
		graphout=self.showgraphics()	
		statout=self.showstatus()
		if shortmode:
			return graphout
		else:
			return "{} ({}) {} {} {}".format(
				graphout,
				self.pet.state["name"],
				statout,
				interfacehelper.parsemessages(self.interfacemessages),
				interfacehelper.parsemessages(self.pet.message))

	def interface(self, action, shortmode):
		self.pet.do(action)
		if self.pet.error:
			return(interfacehelper.parsemessages(self.pet.error),True)
		if self.pet.error:
			error=True
		else:
			error=False
		return self.output(shortmode),error
			
