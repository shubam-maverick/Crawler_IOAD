class trieNode(object):
	def __init__(self,char):
		self.char=char
		self.children = []
		self.end=False

def insert(root,string):
	node = root
	for char in string:
		found = False
		for child in node.children:
			if char == child.char:
				node = child
				found = True
				break
		if found == False:
			new_node = trieNode(char)
			node.children.append(new_node)
			node = new_node

	node.end=True

def find(root,string):
	node = root
	for char in string:
		found = False
		for child in node.children:
			if char == child.char:
				found = True
				node = child
				break
		if found == False:
			return False
	if node.end == True:
		return True
	else:
		return False


#main = trieNode('*')
#add(main,"hello")
#print find(main,"hell")