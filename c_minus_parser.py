from collections import deque
from c_minus_lexer import Lexer
from c_minus_node import Node
from c_minus_utils import *
from c_minus_symbol_table import *

class Parser:
	def parse(self, program):
		lexer = Lexer()
		lexer.parse(program)

		self._tokenList = lexer.getTokens()
		# printTokenList(self._tokenList)

		self._root = self._program()

		if not self._root:
			print('Error: "{0}" at line {1} raise error'.format(self._currentToken.value, self._currentToken.lineNum))
			return None

		# printSyntaxTree(self._root, 0)

		for key in SymbolTable:
			print(SymbolTable[key])

		return self._root

	def _program(self):
		node = Node('program')
		tokens_duplicates = deque(self._tokenList)

		child = self._declarationList();

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node

	def _declarationList(self):
		node = Node('declaration-list')
		tokens_duplicates = deque(self._tokenList)

		child = self._declaration()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		child = self._declarationOthers()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node


	def _declarationOthers(self):
		node = Node('declaration-others')

		if len(self._tokenList) == 0:
			return node

		tokens_duplicates = deque(self._tokenList)

		child = self._declaration()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return Node('declaration-others')

		child = self._declarationOthers()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return Node('declaration-others')

		return node

	def _declaration(self):
		node = Node('declaration')
		tokens_duplicates = deque(self._tokenList)

		child = self._varDeclaration()

		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)

		child = self._funDeclaration()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node


	def _varDeclaration(self):
		node = Node('var-declaration')

		tokens_duplicates = deque(self._tokenList)

		child = self._typeSpecifier()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		token = self._match('identifier')
		if token:
			node.addChild(Node('identifier', token.value))
		else:
			return None

		token = self._match('op',';')
		if token:
			node.addChild(Node('op', ';'))

			return node

		token = self._match('op','[')
		if token:
			node.addChild(Node('op', '['))

			token = self._match('number')
			if token:
				node.addChild(Node('number', token.value))
			else:
				return None

			token = self._match('op',']')
			if token:
				node.addChild(Node('op', ']'))
			else:
				return None

			token = self._match('op',';')
			if token:
				node.addChild(Node('op', ';'))
			else:
				return None
		else:
			return None

		return node

	def _typeSpecifier(self):
		node = Node('type-specifier')

		tokens_duplicates = deque(self._tokenList)

		token = self._match('keyword','int')
		if token:
			node.addChild(Node('keyword', 'int'))
			return node

		token = self._match('keyword', 'void')
		if token:
			node.addChild(Node('keyword', 'void'))
			return node
		
		return None

	def _funDeclaration(self):
		node = Node('fun-declaration')

		tokens_duplicates = deque(self._tokenList)

		child = self._typeSpecifier()

		if child:
			node.addChild(child)

			token = self._match('identifier')
			if token:
				node.addChild(Node('identifier', token.value))
			else:
				return None

			token = self._match('op','(')
			if token:
				node.addChild(Node('op', token.value))
			else:
				return None

			child = self._params()

			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			token = self._match('op', ')')
			if token:
				node.addChild(Node('op', token.value))
			else:
				return None

		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		child = self._compoundStmt()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node

	def _params(self):
		node = Node('params')

		tokens_duplicates = deque(self._tokenList)

		child = self._paramsList()

		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)

		token = self._match('keyword', 'void')
		if token:
			node.addChild(Node('keyword', token.value))
		else:
			return None

		return node

	def _paramsList(self):
		node = Node('param-list')
		tokens_duplicates = deque(self._tokenList)

		child = self._param()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		child = self._paramOthers()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node


	def _paramOthers(self):
		node = Node('param-others')

		tokens_duplicates = deque(self._tokenList)

		token = self._match('op', ',')
		if token:
			node.addChild(Node('op', token.value))

			child = self._param()

			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			child = self._paramOthers()

			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None
		else:
			return Node('param-others')

		return node

	def _param(self):
		node = Node('param')
		tokens_duplicates = deque(self._tokenList)

		child = self._typeSpecifier()

		if child:
			node.addChild(child)
		else:
			self._tokenList == deque(tokens_duplicates)
			return None

		token = self._match('identifier')
		if token:
			node.addChild(Node('identifier', token.value))
		else:
			return None

		token = self._match('op', '[')
		if token:
			node.addChild(Node('op', token.value))

			token = self._match('op', ']')
			if token:
				node.addChild(Node('op', token.value))
			else:
				return None

		return node


	def _compoundStmt(self):
		node = Node('compound-stmt')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('op', '{')
		if token:
			node.addChild(Node('op', '{'))

			child = self._localDeclarations()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			child = self._statementList()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			token = self._match('op', '}')
			if token:
				node.addChild(Node('op', '}'))
			else:
				return None
		else:
			return None

		return node


	def _localDeclarations(self):
		node = Node('local-declarations')
		tokens_duplicates = deque(self._tokenList)

		child = self._localDeclarationsOthers()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node

	def _localDeclarationsOthers(self):
		node = Node('local-declarations-others')
		tokens_duplicates = deque(self._tokenList)

		child = self._varDeclaration()

		if child:
			node.addChild(child)
		else:
			self._tokenList = tokens_duplicates
			return Node('local-declarations-others')

		child = self._localDeclarationsOthers()
		if child:
			node.addChild(child)
		else:
			self._tokenList = tokens_duplicates
			return Node('local-declarations-others')

		return node

	def _statementList(self):
		node = Node('statement-list')
		tokens_duplicates = deque(self._tokenList)

		child = self._statementListOthers()
		if child:
			node.addChild(child)
		else:
			self._tokenList = tokens_duplicates
			return None

		return node


	def _statementListOthers(self):
		node = Node('statement-list-others')
		tokens_duplicates = deque(self._tokenList)

		child = self._statement()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return Node('statement-list-others')

		child = self._statementListOthers()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return Node('statement-list-others')

		return node


	def _statement(self):
		node = Node('statement')
		tokens_duplicates = deque(self._tokenList)

		child = self._expressionStmt()
		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)

		child = self._compoundStmt()
		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)

		child = self._selectionStmt()
		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)


		child = self._iterationStmt()
		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)


		child = self._returnStmt()
		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)

		return None



	def _expressionStmt(self):
		node = Node('expression-stmt')
		tokens_duplicates = deque(self._tokenList)

		child = self._expression()

		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)

		token = self._match('op', ';')
		if token:
			node.addChild(Node('op', ';'))
		else:
			return None

		return node

	def _selectionStmt(self):
		node = Node('selection-stmt')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('keyword', 'if')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		token = self._match('op', '(')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		child = self._expression()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		token = self._match('op', ')')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		child = self._statement()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		token = self._match('keyword', 'else')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return node

		child = self._statement()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node

	def _iterationStmt(self):
		node = Node('iteration-stmt')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('keyword', 'while')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		token = self._match('op', '(')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		child = self._expression()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		token = self._match('op', ')')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		child = self._statement()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node


	def _returnStmt(self):
		node = Node('return-stmt')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('keyword', 'return')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		child = self._expression()
		if child:
			node.addChild(child)
		else:
			self._tokenList = tokens_duplicates

		token = self._match('op', ';')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		return node

	def _expression(self):
		node = Node('expression')
		tokens_duplicates = deque(self._tokenList)

		child = self._var()
		if child:
			token = self._match('op', '=')
			if token:
				node.addChild(child)
				node.addChild(Node(token.type, token.value))

				child = self._expression()
				if child:
					node.addChild(child)

					return node

		self._tokenList = deque(tokens_duplicates)

		child = self._simpleExpression()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node


	def _var(self):
		node = Node('var')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('identifier')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		token = self._match('op', '[')
		if token:
			node.addChild(Node(token.type, token.value))

			child = self._expression()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			token = self._match('op', ']')
			if token:
				node.addChild(Node(token.type, token.value))
			else:
				return None

		return node

	def _simpleExpression(self):
		node = Node('simple-expression')
		tokens_duplicates = deque(self._tokenList)

		child = self._additiveExpression()
		if child:
			node.addChild(child)

			tokens_duplicates = deque(self._tokenList)
			child = self._relop()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return node

			child = self._additiveExpression()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node


	def _relop(self):
		node = Node('relop')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('op', '<=')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		token = self._match('op', '<')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		token = self._match('op', '>')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		token = self._match('op', '>=')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		token = self._match('op', '==')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		token = self._match('op', '!=')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		return None


	def _additiveExpression(self):
		node = Node('additive-expression')
		tokens_duplicates = deque(self._tokenList)

		child = self._term()
		if child:
			node.addChild(child)

			child = self._additiveExpressionOthers()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node


	def _additiveExpressionOthers(self):
		node = Node('additive-expression-others')
		tokens_duplicates = deque(self._tokenList)

		child = self._addop()
		if child:
			node.addChild(child)

			child = self._term()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			child = self._additiveExpressionOthers()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None
		else:
			self._tokenList = deque(tokens_duplicates)
			return Node('additive-expression-others')

		return node

	def _addop(self):
		node = Node('addop')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('op', '+')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		token = self._match('op', '-')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		return None

	def _term(self):
		node = Node('term')
		tokens_duplicates = deque(self._tokenList)

		child = self._factor()
		if child:
			node.addChild(child)

			child = self._termOthers()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		return node


	def _termOthers(self):
		node = Node('term-others')
		tokens_duplicates = deque(self._tokenList)

		child = self._mulop()
		if child:
			node.addChild(child)

			child = self._factor()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			child = self._termOthers()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None
		else:
			self._tokenList = deque(tokens_duplicates)
			return Node('term-others')

		return node

	def _mulop(self):
		node = Node('mulop')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('op', '*')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		token = self._match('op', '/')
		if token:
			node.addChild(Node(token.type, token.value))
			return node	

		return None


	def _factor(self):
		node = Node('factor')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('number')
		if token:
			node.addChild(Node(token.type, token.value))
			return node

		token = self._match('op', '(')
		if token:
			node.addChild(Node(token.type, token.value))

			child = self._expression()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			token = self._match('op', ')')
			if token:
				node.addChild(token.type, token.value)
			else:
				return None

			return node

		child = self._call()
		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)

		child = self._var()
		if child:
			node.addChild(child)
			return node
		else:
			self._tokenList = deque(tokens_duplicates)
		
		return None

	def _call(self):
		node = Node('call')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('identifier')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		token = self._match('op', '(')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		child = self._args()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return None

		token = self._match('op', ')')
		if token:
			node.addChild(Node(token.type, token.value))
		else:
			return None

		return node


	def _args(self):
		node = Node('args')
		tokens_duplicates = deque(self._tokenList)

		child = self._argsList()
		if child:
			node.addChild(child)
		else:
			self._tokenList = deque(tokens_duplicates)
			return Node('args')

		return node

	def _argsList(self):
		node = Node('args-list')
		tokens_duplicates = deque(self._tokenList)

		child = self._expression()
		if child:
			node.addChild(child)

			child = self._argsListOthers()
			if child:
				node.addChild(child)
			else:
				self._tokenList = tokens_duplicates
				return None
		else:
			self._tokenList = tokens_duplicates
			return None

		return node

	def _argsListOthers(self):
		node = Node('args-list-others')
		tokens_duplicates = deque(self._tokenList)

		token = self._match('op', ',')
		if token:
			node.addChild(Node(token.type, token.value))

			child = self._expression()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None

			child = self._argsListOthers()
			if child:
				node.addChild(child)
			else:
				self._tokenList = deque(tokens_duplicates)
				return None
		else:
			return Node('args-list-others')

		return node


	def _match(self, type, value = None):
		token = self._tokenList.popleft()
		self._currentToken = token

		if token.type == type:
			if value:
				if token.value == value:
					return token
				else:
					self._tokenList.appendleft(token)
					return None
			else:
				return token
		else:
			self._tokenList.appendleft(token)
			return None
