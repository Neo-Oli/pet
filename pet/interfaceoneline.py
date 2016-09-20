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
			statout+="Fd:"+interfacehelper.displayvalue(self.pet.state["food"])+sep
			statout+="zZz:"+interfacehelper.displayvalue(self.pet.state["sleep"])+sep
			statout+="cln:"+interfacehelper.displayvalue(self.pet.state["clean"])+sep
			statout+="fun:"+interfacehelper.displayvalue(self.pet.state["play"])+sep
			statout+="lrn:"+interfacehelper.displayvalue(self.pet.state["learn"])+sep
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
		
		graphics={}
		graphics[0]={}
		graphics[0]['happy']=":)"
		graphics[0]['sad']=":("
		graphics[0]['dirty']=":(.°"
		graphics[0]['sleepy']="¦o"
		graphics[0]['sleeping']="¦. zZ"
		graphics[0]['learning']="[:|]"
		graphics[0]['hungry']=":O"
		graphics[0]['sick']=":&"
		graphics[0]['dead']="x("
		graphics[0]['healing']=":& +"
		graphics[0]['eating']=":O*"
		graphics[0]['playing']=":D  o ]"
		graphics[0]['cleaning']=":) ~~¬"
		graphics[1]={}
		graphics[1]['happy']=":-)"
		graphics[1]['sad']=":-("
		graphics[1]['dirty']=":-(.°"
		graphics[1]['sleepy']="¦-o"
		graphics[1]['sleeping']="¦-. zZ"
		graphics[1]['learning']="[:-|]"
		graphics[1]['hungry']=":-O"
		graphics[1]['sick']=":-&"
		graphics[1]['dead']="x-("
		graphics[1]['healing']=":-& +"
		graphics[1]['eating']=":-O*"
		graphics[1]['playing']=":-D  o ]"
		graphics[1]['cleaning']=":-) ~~¬"
		self.graphics=graphics

	
	def output(self, shortmode):
		graphout=self.showgraphics()	
		statout=self.showstatus()
		if shortmode:
			return graphout
		else:
			return "{} ({}) {} {}".format(
				graphout,
				self.pet.state["name"],
				statout,
				interfacehelper.parsemessages(self.interfacemessages),
				interfacehelper.parsemessages(self.pet.message))
