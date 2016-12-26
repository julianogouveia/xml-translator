from .translator import XMLTranslator


with open('example.map') as mapping, open('example.xml') as xml:
	xml_translator = XMLTranslator(mapping, xml)