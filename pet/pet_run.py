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
	parser.add_argument('-g', action='store_true', help="Enable graphics" )
	parser.add_argument('-q', action='store_true')
	parser.add_argument('--grow', action='store_true')
	parser.add_argument('--timeskip', action='store_true')
	args = parser.parse_args()

	output,error=main(args.action,args.name,args.c,args.s,args.timeskip,args.grow,args.q,args.g)
	print(output)
	if error:
		sys.exit(1)

def main(action="",name="",configfile="default.config.yml",statefile="default.state.json",timeskip=False,grow=False, shortmode=False,graphics=False):
	from pet import settings 
	from pet import petstate

	settings=settings.settings(configfile)
	if not settings.config["debug"]:
		if timeskip or grow:
			return settings.text("nodebug"),True
		settings.grow=False
		settings.timeskip=False
	else:
		settings.grow=grow
		settings.timeskip=timeskip
	pet=petstate.petstate(statefile,settings)
	pet.load()
	settings.name=name
	if graphics:
		from pet import interfacegraphics
		interface=interfacegraphics.interface(pet,settings)
		output,error=interface.interface(action,shortmode)
	else:
		from pet import interfaceoneline
		interface=interfaceoneline.interface(pet,settings)
		output,error=interface.interface(action,shortmode)
	pet.save(statefile)
	return output,error
