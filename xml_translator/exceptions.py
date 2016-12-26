class NotFileException(Exception):
	
	def __init__(self, filename):
		message = "{filename} isn't a valid file like object".format(filename=filename)
		super().__init__(message)