import argparse
import sys
def main():
	from pet import settings 
	from pet import petstate

	parser = argparse.ArgumentParser()
	parser.description="Play with the pet"
	parser.add_argument('action', help="Action to do",nargs='?',default="")
	parser.add_argument('name', help="Name (used together with 'new' action)",nargs='?',default="")
	parser.add_argument('-s', nargs='?', help="Settings file to use (in ~/.config/pet/)",default="default.state.json")
	parser.add_argument('-c', nargs='?', help="Settings file to use (in ~/.config/pet/)",default="default.config.yml")
	parser.add_argument('--grow', action='store_true')
	parser.add_argument('--timeskip', action='store_true')
	args = parser.parse_args()

	settings=settings.settings(args.c)
	if not settings.config["debug"]:
		if args.timeskip or \
				args.grow:
			sys.exit(settings.lang["nodebug"])
		settings.grow=False
		settings.timeskip=False
	else:
		settings.grow=args.grow
		settings.timeskip=args.timeskip
	pet=petstate.petstate(args.s,settings)
	pet.load(args.s)
	settings.name=args.name
	pet.do(args.action)

	pet.save(args.s)
	from pet import interfaceoneline
	interface=interfaceoneline.interface(pet,settings)

