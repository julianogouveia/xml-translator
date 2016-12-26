from lxml import etree

from path import PathParser, PathDict
from helpers import recursive_dict_update

class Mapper:

	def __init__(self, mapping, xml, path_parser):
		self.mapped_data = []
		self.mapping = mapping
		self.xml = xml
		self.xml_root = etree.parse(self.xml)
		self.path_parser = path_parser
		self.first_path_parsed = self.path_parser(mapping.readline())

		# Back to the beginning of the file
		self.mapping.seek(0)

	def map(self):
		if not ">" in self.first_path_parsed.source_path:
			self.create_mapped_data()
		else:
			self.create_mapped_items()

		return self.mapped_data

	def create_mapped_data(self):
		elements = root.findall(self.first_path_parsed.source_xpath)

		for element in elements:
			dict_path = self.first_path_parsed.to_dict(element.text)
			self.mapped_data.append(dict_path)

	def create_mapped_items(self):
		main_elements = self.xml_root.xpath(self.first_path_parsed.root_xpath)
		parsed_paths = [self.path_parser(path) for path in self.mapping]

		for main_element in main_elements:
			mapped_item = {}

			for parsed_path in parsed_paths:
				element = main_element.xpath(parsed_path.xpath)

				if not len(element):
					continue
				elif len(element) > 1:
					elements = element
					dict_element = PathDict(parsed_path.source_path, elements, many=True)
				else:
					element = element[0]
					dict_element = PathDict(parsed_path.source_path, element.text)

				mapped_item = recursive_dict_update(mapped_item, dict_element)

			self.mapped_data.append(mapped_item)
