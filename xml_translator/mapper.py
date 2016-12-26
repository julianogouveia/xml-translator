from lxml import etree
import re


class PathParser:

	def __init__(self, path):
		path_sanitized = path.decode('utf-8').replace(" ", "")
		allowed_path_characters = re.compile('[^a-zA-Z\.>@]')

		if allowed_path_characters.match(path_sanitized):
			# Your path has invalid characters, only [a-zA-Z.@] are allowed in the path {path}
			pass

		if not "=" in path_sanitized:
			# You forgot to put the equal(=) character in the path {path}
			pass

		if path_sanitized.count("=") > 1:
			# You can have only one equal(=) character in the path {path}
			pass

		source_path, destination_path = path_sanitized.split("=")

		if source_path.count(".") > 1:
			# You can map only one attribute in the source path {path}
			pass

		if destination_path.count(".") > 1:
			# You can map only one attribute in the destination path {path}
			pass

		if source_path.count("@") > 1:
			# You can have only one filter in the source path {path}
			pass

		if destination_path.count("@"):
			# You can't apply filters in the destination path {path}
			pass

		self.root_xpath = "//{}".format(source_path.split(">", 1)[0])
		self.splitted_path = source_path.split(">")
		self.source_path = source_path
		self.source_xpath = self.source_path.replace(">", "/")

		try:
			self.xpath = self.source_path.split(">", 1)[1].replace(">", "/")
		except IndexError:
			self.xpath = self.root_xpath

		self.destination_path = destination_path
		

	def to_dict(self, value=None, many=False):
		spplited_path = self.destination_path.split(">")
		default = spplited_path[-1]

		if many:
			value = [elem.text for elem in value]

		dict_path = value

		for key in reversed(spplited_path):
			dict_path = {key.strip(): dict_path}

		return dict_path

def recursive_dict_update(original, update):
    for key, value in original.items(): 
        if key not in update:
            update[key] = value
        elif isinstance(value, dict):
            recursive_dict_update(value, update[key])

    return update


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
					dict_element = parsed_path.to_dict(elements, many=True)
				else:
					element = element[0]
					dict_element = parsed_path.to_dict(element.text)

				mapped_item = recursive_dict_update(mapped_item, dict_element)

			self.mapped_data.append(mapped_item)



XML_DUMPER_XML = "xml"
XML_DUMPER_DICT = "dict"
XML_DUMPER_JSON = "json"


class XMLDumper:

	def __init__(self, type=XML_DUMPER_XML):
		self.type = type


mapping = open("example.map", "rb")
xml = open("table.xml", "rb")
mapper = Mapper(mapping, xml, PathParser)
print(mapper.map())