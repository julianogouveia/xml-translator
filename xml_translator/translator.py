from collections import OrderedDict
from lxml import etree

from path import PathParser, PathDict
from helpers import recursive_dict_update
from filters import FILTER_SEPARATOR, Filter, Filters, strip_filter, lower_filter, upper_filter

SOURCE_PATH_TYPE = "source_path"
DESTINATION_PATH_TYPE = "destination_path"


class XMLTranslator:

	def __init__(self, mapping, xml):
		self.mapping = mapping
		self.xml = xml
		self.xml_root = etree.parse(self.xml)
		self.document = {}
		self.filters = Filters()

	def get_mapping(self, path_type=SOURCE_PATH_TYPE):
		self.mapping.seek(0)
		mapping = {}

		for path in self.mapping:
			parsed_path = PathParser(path)
			mapping = recursive_dict_update(mapping, PathDict(getattr(parsed_path, path_type)))

		return mapping

	def set_filters(self):
		self.filters.add(strip_filter)
		self.filters.add(lower_filter)
		self.filters.add(upper_filter)

	def add_filter(self, filter):
		self.filters.add(filter)

	def create_document(self):
		self.set_filters()

		source_mapping = self.get_mapping()
		translated_elements = []

		for element_xpath, element_childrens in source_mapping.items():
			elements = self.xml_root.xpath("//{}".format(element_xpath))
			filtered_elements = self.translate(elements, element_childrens, None)
			translated_elements.append(filtered_elements)

		self.document = translated_elements
		return self.document

	def translate(self, elements, childrens, filter_name):
		translated_elements = []

		for element in elements:
			new_childrens = None
			element_filter = None

			for element_xpath, element_childrens in childrens.items():
				if not new_childrens:
					new_childrens = []

				if len(element_xpath.split("@")) > 1:
					element_xpath, element_filter = element_xpath.split(FILTER_SEPARATOR)

				elements = element.xpath(element_xpath)
				new_childrens += self.translate(elements, element_childrens, element_filter)
			
			element_name = element.tag
			element_data = element.text.strip()
			new_element = {element_name: {}}

			if element_data:
				if filter_name:
					element_data = self.filters.apply(filter_name, element_data)

				new_element[element_name]["data"] = element_data

			if new_childrens:
				new_element[element_name]["childrens"] = new_childrens

			translated_elements.append(OrderedDict(sorted(new_element.items())))	

		return translated_elements
