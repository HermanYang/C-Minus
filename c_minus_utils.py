counter = 0

def printSyntaxTree(node, depth):
	if node:
		print(' ' * depth + str(node))

		nodes = node.children
		for child in nodes:
			printSyntaxTree(child, depth + 1)

def printTokenList(tokenList):
	for token in tokenList:
		print(token)
		
def newAddress():
	i = i + 1
	return 't' + str(i)
