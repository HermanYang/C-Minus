from c_minus_utils import *
from collections import deque
from c_minus_symbol_table import *

class Generator:
	def __init__(self):
		self._codes = []

	def generate(self, syntax_tree):
		self._handleProgram(syntax_tree)
		for code in self._codes:
			print(code)


	def _handleProgram(self, node):
		assert node.type == 'program'

		declaration_list_node = node.getFirstChildByType('declaration-list')
		assert declaration_list_node

		self._handleDeclarationList(declaration_list_node)


	def _handleDeclarationList(self, node):
		assert node.type == 'declaration-list'

		declaration_node = node.getFirstChildByType('declaration')
		assert declaration_node

		self._handleDeclaration(declaration_node)

		declaration_others_node = node.getFirstChildByType('declaration-others')
		assert declaration_others_node

		self._handleDeclarationOthers(declaration_others_node)


	def _handleDeclarationOthers(self, node):
		assert node.type == 'declaration-others'

		declaration_node = node.getFirstChildByType('declaration')
		if declaration_node != None:
			 self._handleDeclaration(declaration_node)
			 declaration_others_node = node.getFirstChildByType('declaration-others')

			 assert declaration_others_node
			 self._handleDeclarationOthers(declaration_others_node)


	def _handleDeclaration(self, node):
		assert node.type == 'declaration'

		var_declaration_node = None
		var_fun_declaration_node = None

		if ( node.children[0].type == 'var-declaration' ):
			var_declaration_node = node.children[0]
		else:
			assert node.children[0].type == 'fun-declaration'
			var_fun_declaration_node = node.children[0]

		if var_declaration_node:
			assert var_fun_declaration_node == None
			self._handleVarDeclaration(var_declaration_node)
		else:
			assert var_fun_declaration_node 
			self._handleFunDeclaration(var_fun_declaration_node)


	def _handleVarDeclaration(self, node):
		assert node.type == 'var-declaration'

		type = node.getFirstChildByType('keyword').value
		id = node.getFirstChildByType('identifier').value

		if (node.getFirstChildByValue('[') != None):
			array_num = int(node.getFirstChildByType('number').value)
			SymbolTable[id] = ArraySymbol(type, id, array_num)
		else:
			SymbolTable[id] = Symbol(type, id)


	def _handleFunDeclaration(self, node):
		assert node.type == 'fun-declaration'

		type = node.getFirstChildByType('keyword').value
		id = node.getFirstChildByType('identifier').value
		params = node.getChildrenByType('param')
		param_list = []

		for e in params:

			e_type = e.getFirstChildByType('keyword').value
			e_id = e.getFirstChildByType('identifier').value

			if(e.getFirstChildByType('[') != None):
				e_array_num = int(e.getFirstChildByType('number').value)
				param_list.append(ArraySymbol(e_type, e_id, e_array_num))
			else:
				if(e_type == 'void'):
					continue
				param_list.append(Symbol(e_type, e_id))

		SymbolTable[id] = FunSymbol(type, id, param_list)

		compound_stmt_node = node.getFirstChildByType('compound-stmt')
		assert compound_stmt_node
		self._handleCompoundStmt(compound_stmt_node)


	def _handleCompoundStmt(self, node):
		assert node.type == 'compound-stmt'

		local_declaration_node = node.getFirstChildByType('local-declarations')
		assert local_declaration_node
		self._handleLocalDeclarations(local_declaration_node)

		statement_list_node = node.getFirstChildByType('statement-list')
		assert statement_list_node
		self._handleStatementList(statement_list_node)


	def _handleLocalDeclarations(self, node):
		assert node.type == 'local-declarations'

		local_declaration_others_node = node.getFirstChildByType('local-declarations-others')
		assert local_declaration_others_node
		self._handleLocalDeclarationsOthers(local_declaration_others_node)


	def _handleLocalDeclarationsOthers(self, node):
		assert node.type == 'local-declarations-others'

		var_declaration_node = node.getFirstChildByType('var-declaration')

		if var_declaration_node:
			self._handleVarDeclaration(var_declaration_node)

			local_declaration_others_node = node.getFirstChildByType('local-declarations-others')
			assert local_declaration_others_node
			self._handleLocalDeclarationsOthers(local_declaration_others_node)



	def _handleStatementList(self, node):
		assert node.type == 'statement-list'

		statement_list_others_node = node.getFirstChildByType('statement-list-others')
		assert statement_list_others_node
		self._handleStatementListOthers(statement_list_others_node)



	def _handleStatementListOthers(self, node):
		assert node.type == 'statement-list-others'

		statement_node = node.getFirstChildByType('statement')
		if statement_node:
			self._handleStatement(statement_node)

			statement_list_others_node = node.getFirstChildByType('statement-list-others')
			assert statement_list_others_node
			self._handleStatementListOthers(statement_list_others_node)


	def _handleStatement(self, node):
		assert node.type == 'statement'

		expression_stmt_node = node.getFirstChildByType('expression-stmt')
		if expression_stmt_node:
			self._handleExpressionStmt(expression_stmt_node)

		compound_stmt_node = node.getFirstChildByType('compound-stmt')
		if compound_stmt_node:
			self._handleCompoundStmt(compound_stmt_node)

		selection_stmt_node = node.getFirstChildByType('selection-stmt')
		if selection_stmt_node:
			self._handleSelectionStmt(selection_stmt_node)

		iteration_stmt_node = node.getFirstChildByType('iteration-stmt')
		if iteration_stmt_node:
			self._handleIterationStmt(iteration_stmt_node)

		return_stmt_node = node.getFirstChildByType('return-stmt')
		assert return_stmt_node
		self._handleReturnStmt(return_stmt_node)



	def _handleExpressionStmt(self, node):
		assert node.type == 'expression-stmt'

		if node.children[0].type == 'expression':
			self._handleExpression(node.children[0])


	def _handleIterationStmt(self, node):
		assert node.type == 'iteration-stmt'
		return

	def _handleSelectionStmt(self, node):
		assert node.type == 'selection-stmt'
		return

	def _handleReturnStmt(self, node):
		assert node.type == 'return-stmt'
		return

	def _handleExpression(self, node):
		assert node.type == 'expression'

		child = node.children[0]

		if child.type == 'var':
			var_node = child
			expression_node = node.children[2]

			self._handleExpression(expression_node)
			src = self._getLastCode().des

			self._handleVar(child)
			des = self._getLastCode().des

			self._appendCode(Code('=', src, None, des))

		assert child.type == 'simple-expression'

		self._handleSimpleExpression(child)


	def _handleSimpleExpression(self, node):
		assert node.type == 'simple-expression'
		return 

	def _handleVar(self, node):
		assert node.type == 'var'

		child = node.children[0]

		if len(node.children) > 1:
			self._handleExpression(child.getFirstChildByType('expression'))
			addr = newAddress()
			self._appendCode(Code('+', child.value, self._getLastCode().des, addr))

		self._appendCode(Code('=', child.vale, None, child.vale))

	def _getLastCode(self):
		length = len(self._codes)
		last_index = length - 1

		if last_index > 0:
			return self._codes[last_index]
		else:
			return None

	def _appendCode(self, code):
		self._codes.append(code)

	def _appendCodes(self, codes):
		for c in codes:
			self._code.append(c)
