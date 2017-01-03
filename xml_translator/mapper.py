from collections import OrderedDict
from lxml import etree

from path import PathParser, PathDict
from helpers import recursive_dict_update

SOURCE_PATH_TYPE = "source_path"
DESTINATION_PATH_TYPE = "destination_path"


class Mapper:

	def __init__(self, mapping, xml):
		self.mapping = mapping
		self.xml = xml
		self.xml_root = etree.parse(self.xml)
		self.mapped = {}

	def get_mapping(self, path_type=SOURCE_PATH_TYPE):
		self.mapping.seek(0)
		mapping = {}

		for path in self.mapping:
			parsed_path = PathParser(path)
			mapping = recursive_dict_update(mapping, PathDict(getattr(parsed_path, path_type)))

		return mapping

	def map(self, source_mapping=None):
		source_mapping = self.get_mapping()
		mapped_elements = []

		for element_xpath, element_childrens in source_mapping.items():
			elements = self.xml_root.xpath("//{}".format(element_xpath))
			filtered_elements = self.filter(elements, element_childrens)
			mapped_elements.append(filtered_elements)

		self.mapped = mapped_elements
		return self.mapped

	def filter(self, filter_elements, filter_childrens):
		filtered_elements = []

		for filter_element in filter_elements:
			childrens = None

			for element_xpath, element_childrens in filter_childrens.items():
				if not childrens:
					childrens = []

				elements = filter_element.xpath(element_xpath)
				childrens += self.filter(elements, element_childrens) 

			element = {filter_element.tag: {}}

			element_name = filter_element.tag
			element_text = filter_element.text

			if element_text:
				element[element_name]["text"] = element_text

			if childrens:
				element[element_name]["childrens"] = childrens

			filtered_elements.append(OrderedDict(sorted(element.items())))	

		return filtered_elements
