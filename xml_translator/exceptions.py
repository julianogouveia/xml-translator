class NotFileException(Exception):
	
	def __init__(self, filename):
		message = "{filename} isn't a valid file like object".format(filename=filename)
		super().__init__(message)


class InvalidPathCharactersException(Exception):
	
	def __init__(self, c):
		message = "Your path has invalid characters, only [a-zA-Z.@] are allowed in the path {path}".format(path=path)
		super().__init__(message)


class MissingEqualCharacterException(Exception):
	
	def __init__(self, c):
		message = "You forgot to put the equal(=) character in the path {path}".format(path=path)
		super().__init__(message)


class OnlyOneEqualCharacterException(Exception):
	
	def __init__(self, c):
		message = "You can have only one equal(=) character in the path {path}".format(path=path)
		super().__init__(message)


class OnlyOneAttributeInSourcePathException(Exception):
	
	def __init__(self, c):
		message = "You can map only one attribute in the source path {path}".format(path=path)
		super().__init__(message)


class OnlyOneAttributeInDestinationPathException(Exception):
	
	def __init__(self, c):
		message = "You can map only one attribute in the destination path {path}".format(path=path)
		super().__init__(message)


class OnlyOneFilterInSourcePathException(Exception):
	
	def __init__(self, c):
		message = "You can have only one filter in the source path {path}".format(path=path)
		super().__init__(message)


class CantApplyFilterInDestinationPathException(Exception):
	
	def __init__(self, c):
		message = "You can't apply filters in the destination path {path}".format(path=path)
		super().__init__(message)
