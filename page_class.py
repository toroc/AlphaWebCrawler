class web_page:
	"""docstring for web_page"""
	def __init__(self, url, title, parent):
		self.url = url
		self.title = title
		self.parent = parent


	@property
	def asDict(self):
		d = self.__dict__
		#print(d)
		return d


class pages:
	def __init__(self):
		self.visited = list()


	
