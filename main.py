from c_minus_parser import Parser
from c_minus_generator import Generator

def main():
	f = open('simple.c-', 'r')
	program = f.read()
	parser = Parser()
	generator = Generator()

	syntax_tree = parser.parse(program)
	generator.generate(syntax_tree)

	return

if __name__ == '__main__':
	main()