def displayvalue(value):
	value=minmax(value)
	value=value/25
	value=round(value)
	# segments=""
	# for i in range(value):
		# segments+="#"
	# value="["+segments.ljust(4)+"]"
	value=str(value)
	return value


def minmax(number):
	if number < 0:
		number=0
	elif number > 100:
		number=100
	return number


def parsemessages(messages):
	message=""
	for entry in messages:
		message+=entry+" "
	return message
