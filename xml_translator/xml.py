from io import TextIOBase

from .exceptions import NotFileException


class XMLTranslator:

	def __init__(self, mapping, xml):
		self.mapping = mapping
		self.xml = xml

		if not issubclass(self.mapping, TextIOBase):
			raise NotFileException("Mapping")

		if not issubclass(self.xml, TextIOBase):
			raise NotFileException("XML")