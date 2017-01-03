FILTER_SEPARATOR = "@"


class Filter:

	def __init__(self, name, function):
		self.name = name
		self.function = function

	def apply(self, input):
		return self.function(input)


class Filters:

	def __init__(self):
		self.filters = {}

	def add(self, filter):
		self.filters.update({filter.name: filter})

	def apply(self, name, input):
		return self.filters[name].apply(input)


strip_filter = Filter("strip", str.strip)
lower_filter = Filter("lower", str.lower)
upper_filter = Filter("upper", str.upper)