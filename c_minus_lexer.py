from collections import deque
from c_minus_token import Token
import re

class Lexer:

	def parse(self, program):

		queue = deque()

		i = 0
		for c in program:
			queue.append(c)

		queue.append('$')

		stateHandler = {}

		stateHandler['start'] = self._startStateHandler
		stateHandler['comment'] = self._commentStateHandler
		stateHandler['word'] = self._wordStateHandler
		stateHandler['op'] = self._opStateHandler
		stateHandler['done'] = self._doneStateHander

		self._state = 'start'

		self._opList = ['+', '-', '*', '/', '>', '<', '=', '!', '(', ')', '[', ']', '{', '}', ',', ';']
		self._whitespaceList = [' ', '\t', '\n']
		self._keywordList = ['if', 'else', 'int', 'return', 'void', 'while']


		self._tokenList = deque()
		self._token = ''
		self._lineNum = 1
		self._peek = queue.popleft()

		while self._state != 'finish':
			if not stateHandler[self._state](queue):
				print('Error raise by "{1}" in line {2}'.format(self._state, self._peek, self._lineNum))
				print('Lexer state is {0}'.format(self._state));
				return False

		return True

	def getTokens(self):
		return self._tokenList

	def _isWord(self, c):
		assii = ord(c)
		if assii >= ord('0') and assii <= ord('9'):
			return True

		if assii >= ord('a') and assii <= ord('z'):
			return True

		if assii >= ord('A') and assii <= ord('Z'):
			return True

	def _isOp(self, c):
		if c in self._opList:
			return True

		return False

	def _isWhiteSpace(self, c):
		if c in self._whitespaceList:
			return True

		return False

	def _isKeyword(self, w):
		if w in self._keywordList:
			return True

		return False

	def _isIdentifier(self, w):
		if re.match(r'^([a-z]|[A-Z])+$', w):
			return True

		return False

	def _isNumber(self, w):
		return w.isdigit()


	def _startStateHandler(self, queue):
		if self._peek == '\n':
			self._lineNum += 1

		# filter white space
		while self._isWhiteSpace(self._peek):
			if queue: self._peek = queue.popleft()

		if( self._isWord(self._peek) ):
			self._state = 'word'
			return True

		if( self._isOp(self._peek) ):
			self._state = 'op'
			return True
			
		if self._peek == '$':
			self._state = 'done'
			return True


		return False

	def _wordStateHandler(self, queue):
		if( self._isWord(self._peek) ):
			self._token += self._peek
			if queue: self._peek = queue.popleft()
			return True
		else:
			self._state = 'done'

			# keyword
			if self._isKeyword(self._token):
				self._tokenList.append(Token('keyword', self._token, self._lineNum))
				self._token = ''
				return True

			#identifer
			if self._isIdentifier(self._token):
				self._tokenList.append(Token('identifier', self._token, self._lineNum))
				self._token = ''
				return True

			# number
			if self._isNumber(self._token):
				self._tokenList.append(Token('number', self._token, self._lineNum))
				self._token = ''
				return True
		
		return False

	def _opStateHandler(self, queue):
		if self._isOp(self._peek):
			# due with comment
			if self._peek == '/':
				if queue: self._peek = queue.popleft()
				if self._peek == '*':
					if queue: self._peek = queue.popleft()
					self._state = 'comment'
					return True
				else:
					self._tokenList.append(Token('op', '/', self._lineNum))
					self._state = 'done'
					return True

			# due with double op
			if self._peek == '<' or self._peek == '>' or self._peek == '=':
				self._token = self._peek
				if queue: self._peek = queue.popleft()

				if self._peek == '=':
					self._token += self._peek 
					if queue: self._peek = queue.popleft();
					self._tokenList.append(Token('op', self._token, self._lineNum))
					self._token = ''
					self._state = 'done'
					return True
				else:
					self._tokenList.append(Token('op', self._token, self._lineNum))
					self._token = ''
					self._state = 'done'
					return True
			else:
				self._tokenList.append(Token('op', self._peek, self._lineNum))
				if queue: self._peek = queue.popleft()
				self._state = 'done'
				return True

		return False

	def _commentStateHandler(self, queue):
		if self._peek == '\n':
			self._lineNum += 1

		if self._peek == '*':
			assert queue
			self._peek = queue.popleft()
			if self._peek == '/':
				if queue: self._peek = queue.popleft()
				self._state = 'done'
				return True
			else:
				return True

		if not queue:
			return False

		self._peek = queue.popleft()
		return True

	def _doneStateHander(self, queue):

		if not queue:
			if self._peek == '$':
				self._state = 'finish'
				return True
			else:
				return False

		self._state = 'start'
		return True


