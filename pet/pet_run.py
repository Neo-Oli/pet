# coding=utf-8
def cli():
	from pet import settings 
	import argparse,sys
	from pet import petstate

	parser = argparse.ArgumentParser()
	parser.description="Virtual pet symulator. Initialize with: pet new [name]"
	parser.add_argument('action', help="Action to do: eat, play, sleep, learn, heal, clean",nargs='?',default="")
	parser.add_argument('name', help="Name (used together with 'new' action)",nargs='?',default="")
	parser.add_argument('-s', nargs='?', help="Settings file to use (in ~/.config/pet/)",default="default.state.json")
	parser.add_argument('-c', nargs='?', help="Settings file to use (in ~/.config/pet/)",default="default.config.yml")
	parser.add_argument('--grow', action='store_true')
	parser.add_argument('--timeskip', action='store_true')
	args = parser.parse_args()

	output,error=main(args.action,args.name,args.c,args.s,args.timeskip,args.grow)
	print(output)
	if error:
		sys.exit(1)

def main(action="",name="",configfile="default.config.yml",statefile="default.state.json",timeskip=False,grow=False):
	from pet import settings 
	from pet import petstate

	settings=settings.settings(configfile)
	if not settings.config["debug"]:
		if timeskip or grow:
			return settings.text("nodebug")
		settings.grow=False
		settings.timeskip=False
	else:
		settings.grow=grow
		settings.timeskip=timeskip
	pet=petstate.petstate(statefile,settings)
	pet.load()
	settings.name=name
	pet.do(action)
	if pet.error:
		from pet import interfacehelper
		return(interfacehelper.parsemessages(pet.error),True)
	pet.save(statefile)
	from pet import interfaceoneline
	interface=interfaceoneline.interface(pet,settings)
	if pet.error:
		error=True
	else:
		error=False
	return interface.output(),error

