def create_dict_by_path(path, value=None):
	spplited_path = path.split(">")
	default = spplited_path[-1]
	dict_path = value

	for key in reversed(spplited_path):
		dict_path = {key: dict_path}

	return dict_path