"""routine at server start"""
import os


def create_paths():
	"""Create directories for images"""
	dirpaths = [
		'app/static/portraits/large/1',
		'app/static/portraits/medium/1',
		'app/static/portraits/thumbnail/1'
	]
	for path in dirpaths:
		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))


def make_routines():
	create_paths()
