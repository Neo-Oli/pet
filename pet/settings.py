# coding=utf-8
import yaml
import os,sys
from pkg_resources import resource_stream, Requirement
class settings(object):
	
	def __init__(self,configfile):
		self.configpath=os.path.expanduser("~/.config/pet/")
		self.configfile=configfile
		self.config=self.loadconfig()
		self.lang=self.loadlang()

	# def __getattr__( self, name ):
		# if name == "lang":
			# return self.lang
		# elif name == "config":
			# return self.config

	def loadconfig(self):
		if os.path.dirname(sys.argv[0]):
			os.chdir(os.path.dirname(sys.argv[0]))
		if not os.path.exists(self.configpath+self.configfile):
			if not os.path.exists(self.configpath):
				os.makedirs(self.configpath)
			configdata = resource_stream(Requirement.parse("pet"), "config/default.yml").read().decode("utf-8")
			with open(self.configpath+self.configfile, "w") as openfile:
				openfile.write(configdata)
		else:
			with open (self.configpath+self.configfile, "r") as openfile:
				configdata=openfile.read()
		config=yaml.load(configdata)
		return config

	def loadlang(self):
		openfile = resource_stream(Requirement.parse("pet"), "translations/"+self.config["lang"]+".yml")
		langdata=openfile.read()
		return yaml.load(langdata)


	def text(self,key):

		return self.lang[key]

	
