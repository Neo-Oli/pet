# coding=utf-8
from pet import interfacehelper
import datetime,sys
class interface():
	
	def showstatus(self,pet,settings):
		sep=" "
		statout=" "
		if pet.state["dead"]==True:
			statout+=settings.lang["dead"]+sep
		elif pet.state["sick"]==True and pet.state["action"]!="heal":
			statout+=settings.lang["sick"]+sep
		else:
			if pet.state["action"]:
				timeleft=(settings.config[pet.state["action"]+"time"]*settings.config["timemodifier"]) - (pet.state["time"] - pet.state["actiontime"]) 
				self.interfacemessages.append(settings.lang["remainingtime"]+":"+str(datetime.timedelta(seconds=round(timeleft))))
			statout+="Fd:"+interfacehelper.displayvalue(pet.state["food"])+sep
			statout+="zZz:"+interfacehelper.displayvalue(pet.state["sleep"])+sep
			statout+="cln:"+interfacehelper.displayvalue(pet.state["clean"])+sep
			statout+="fun:"+interfacehelper.displayvalue(pet.state["play"])+sep
			statout+="lrn:"+interfacehelper.displayvalue(pet.state["learn"])+sep
		return statout

	def showgraphics(self,pet,settings):
		global graphout
		mood=pet.getmood()
		graphic=self.graphics[pet.state["grow"]][mood]
		graphic=graphic.ljust(7)
		return graphic

	def __init__(self,pet,config):
		self.interfacemessages=[]
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
		graphout=self.showgraphics(pet,config)	
		statout=self.showstatus(pet,config)
		print(graphout + " ("+ pet.state["name"] + ") " +statout + " " +\
				interfacehelper.parsemessages(self.interfacemessages) + \
				interfacehelper.parsemessages(pet.message) + \
				interfacehelper.parsemessages(pet.error))
		if pet.error:
			sys.exit(1)

