import re
from collections import OrderedDict

from exceptions import (NotFileException,
						InvalidPathCharactersException,
						MissingEqualCharacterException,
						OnlyOneEqualCharacterException,
						OnlyOneAttributeInSourcePathException,
						OnlyOneAttributeInDestinationPathException,
						OnlyOneFilterInSourcePathException,
						CantApplyFilterInDestinationPathException)

PATH_SEPARATOR = ">"
XPATH_SELECTOR = "/"


class PathSanitizer:

	def __new__(cls, path):
		return path.decode('utf-8').replace(" ", "")


class PathValidator:
	allowed_characters = re.compile('[^a-zA-Z\.>@]')

	def __init__(self, path):
		if self.allowed_characters.match(path):
			raise InvalidPathCharactersException(path)

		if not "=" in path:
			raise MissingEqualCharacterException(path)

		if path.count("=") > 1:
			raise OnlyOneEqualCharacterException(path)

		source_path, destination_path = path.split("=")

		if source_path.count(".") > 1:
			raise OnlyOneAttributeInSourcePathException(path)

		if destination_path.count(".") > 1:
			raise OnlyOneAttributeInDestinationPathException(path)

		if source_path.count("@") > 1:
			raise OnlyOneFilterInSourcePathException(path)

		if destination_path.count("@"):
			raise CantApplyFilterInDestinationPathException(path)

		self.validated_path = path
		self.source_path = source_path
		self.destination_path = destination_path


class XPath:

	def __new__(cls, path):
		try:
			return path.split(PATH_SEPARATOR, 1)[1].replace(PATH_SEPARATOR, XPATH_SELECTOR)
		except IndexError:
			return path.split(PATH_SEPARATOR, 1)[0]


class PathParser:

	def __init__(self, path):
		sanitized_path = PathSanitizer(path)
		path_validator = PathValidator(sanitized_path)
		validated_path = path_validator.validated_path
		source_path = path_validator.source_path
		destination_path = path_validator.destination_path

		self.root_xpath = "//{}".format(source_path.split(PATH_SEPARATOR, 1)[0])
		self.splitted_path = source_path.split(PATH_SEPARATOR)
		self.source_path = source_path
		self.xpath = XPath(source_path)
		self.source_xpath = source_path.replace(PATH_SEPARATOR, XPATH_SELECTOR)
		self.destination_path = destination_path


class PathDict:

	def __new__(cls, path, value={}):
		spplited_path = path.split(PATH_SEPARATOR)
		default = spplited_path[-1]

		cls.path_dict = value

		for key in reversed(spplited_path):
			cls.path_dict = OrderedDict(sorted({key.strip(): cls.path_dict}.items()))

		return cls.path_dict