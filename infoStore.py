class infoLink:
	def _int_(self):
		self.parent = "";
		self.child = "";
		self.depth = None;
		self.text = ""
	def info(self, parent, child, depth, text):
		self.parent = parent;
		self.child = child
		self.depth = depth;
		self.text = text;