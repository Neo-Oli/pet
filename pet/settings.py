import yaml
import os,sys,shutil
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
			os.makedirs(self.configpath,exist_ok=True)
			shutil.copyfile("pet/default.yml",self.configpath+self.configfile)
		with open (self.configpath+self.configfile, "r") as openfile:
			configdata=openfile.read()
		config=yaml.load(configdata)
		return config

	def loadlang(self):
		with open ("lang_"+self.config["lang"]+".yml", "r") as openfile:
			langdata=openfile.read()
		return yaml.load(langdata)

	
