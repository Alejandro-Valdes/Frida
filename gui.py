import sys
import time
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QPlainTextEdit, QWidget, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from lineText import LineTextWidget

# <a href="https://es.icons8.com/web-app/13120/Prismáticos">Prismáticos créditos de icono</a>
# <a href="https://es.icons8.com/web-app/11949/Cortar">Cortar créditos de icono</a>

class LineNumberArea(QWidget):

	def __init__(self, editor):
		super().__init__(editor)
		self.myeditor = editor


	def sizeHint(self):
		return Qsize(self.editor.lineNumberAreaWidth(), 0)


	def paintEvent(self, event):
		self.myeditor.lineNumberAreaPaintEvent(event)

# ------ Code editor ---------------------------

class FridaCodeEditor(QPlainTextEdit):
	"""docstring for FridaCodeEditor"""

	origin = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.lineNumberArea = LineNumberArea(self)

		self.origin.connect(self.updateLineNumberAreaWidth)
		self.origin.connect(self.updateLineNumberArea)
		self.origin.connect(self.highlightCurrentLine)

		self.updateLineNumberAreaWidth(0)

	def lineNumberAreaWidth(self):
		digits = 1
		count = max(1, self.blockCount())
		while count >= 10:
			count /= 10
			digits += 1
		space = 3 + self.fontMetrics().width('9') * digits
		return space


	def updateLineNumberAreaWidth(self, _):
		self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


	def updateLineNumberArea(self, rect, dy):

		if dy:
			self.lineNumberArea.scroll(0, dy)
		else:
			self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
					   rect.height())

		if rect.contains(self.viewport().rect()):
			self.updateLineNumberAreaWidth(0)


	def resizeEvent(self, event):
		super().resizeEvent(event)

		cr = self.contentsRect();
		self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
					self.lineNumberAreaWidth(), cr.height()))


	def lineNumberAreaPaintEvent(self, event):
		mypainter = QPainter(self.lineNumberArea)

		mypainter.fillRect(event.rect(), Qt.lightGray)

		block = self.firstVisibleBlock()
		blockNumber = block.blockNumber()
		top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
		bottom = top + self.blockBoundingRect(block).height()

		print(top)
		print("somthing")

		# Just to make sure I use the right font
		height = self.fontMetrics().height()
		while block.isValid() and (top <= event.rect().bottom()):
			if block.isVisible() and (bottom >= event.rect().top()):
				number = str(blockNumber + 1)
				mypainter.setPen(Qt.black)
				mypainter.drawText(0, top, self.lineNumberArea.width(), height,
				 Qt.AlignRight, number)

			block = block.next()
			top = bottom
			bottom = top + self.blockBoundingRect(block).height()
			blockNumber += 1


	def highlightCurrentLine(self):
		extraSelections = []

		if not self.isReadOnly():
			selection = QTextEdit.ExtraSelection()

			lineColor = QColor(Qt.yellow).lighter(160)

			selection.format.setBackground(lineColor)
			selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			selection.cursor = self.textCursor()
			selection.cursor.clearSelection()
			extraSelections.append(selection)
		self.setExtraSelections(extraSelections)
			 
			 
	
	def Dedent(self):
		tab = "\t"
		cursor = self.text.textCursor()
	
		start = cursor.selectionStart()
		end = cursor.selectionEnd()
	
		cursor.setPosition(end)
		cursor.movePosition(cursor.EndOfLine)
		end = cursor.position()
	
		cursor.setPosition(start)
		cursor.movePosition(cursor.StartOfLine)
		start = cursor.position()
	
	
		while cursor.position() < end:
			global var
			 
			cursor.movePosition(cursor.StartOfLine)
			cursor.deleteChar()
			cursor.movePosition(cursor.EndOfLine)
			cursor.movePosition(cursor.Down)
			end -= len(tab)
	
			'''if cursor.position() == end:
				var +=1
	
			if var == 2:
				break'''
	
	def BulletList(self):
		print("bullet connects!")
		self.text.insertHtml("<ul><li> ...</li></ul>")
	
	def NumberedList(self):
		print("numbered connects!")
		self.text.insertHtml("<ol><li> ...</li></ol>")



# ---------------- Main Window -----------------------

class FridaMainWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		exitAction = QAction(QIcon('exit.png'), '&Salir', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Salir de la aplicación')
		exitAction.triggered.connect(qApp.quit)

		newAction = QAction(QIcon("icons/new.png"),"Nuevo",self)
		newAction.setShortcut("Ctrl+N")
		newAction.setStatusTip("Crea un documento en blanco")
		newAction.triggered.connect(self.New)
		
		openAction = QAction(QIcon("icons/open.png"),"Abrir",self)
		openAction.setStatusTip("Abrir un documento existente")
		openAction.setShortcut("Ctrl+O")
		openAction.triggered.connect(self.Open)
		
		saveAction = QAction(QIcon("icons/save.png"),"Guardar",self)
		saveAction.setStatusTip("Guardar documento")
		saveAction.setShortcut("Ctrl+S")
		saveAction.triggered.connect(self.Save)
		
		findAction = QAction(QIcon("icons/find.png"),"Buscar",self)
		findAction.setStatusTip("Busca palabras en tu documento")
		findAction.setShortcut("Ctrl+F")
		findAction.triggered.connect(self.Find)
		
		cutAction = QAction(QIcon("icons/cut.png"),"Cortar",self)
		cutAction.setStatusTip("Borra y copia texto al clipboard")
		cutAction.setShortcut("Ctrl+X")
		cutAction.triggered.connect(self.Cut)
		
		copyAction = QAction(QIcon("icons/copy.png"),"Copiar",self)
		copyAction.setStatusTip("Copiar texto al clipboard")
		copyAction.setShortcut("Ctrl+C")
		copyAction.triggered.connect(self.Copy)
		
		pasteAction = QAction(QIcon("icons/paste.png"),"Pegar",self)
		pasteAction.setStatusTip("Pega texto del clipboard")
		pasteAction.setShortcut("Ctrl+V")
		pasteAction.triggered.connect(self.Paste)
		
		undoAction = QAction(QIcon("icons/undo.png"),"Deshacer",self)
		undoAction.setStatusTip("Deshacer la última acción")
		undoAction.setShortcut("Ctrl+Z")
		undoAction.triggered.connect(self.Undo)
		
		redoAction = QAction(QIcon("icons/redo.png"),"Rehacer",self)
		redoAction.setStatusTip("Rehacer la última acción hecha")
		redoAction.setShortcut("Ctrl+Y")
		redoAction.triggered.connect(self.Redo)
		
		printAction = QAction(QIcon("icons/print.png"),"Imprimir",self)
		printAction.setStatusTip("Imprimir documento")
		printAction.setShortcut("Ctrl+P")
		printAction.triggered.connect(self.Print)

		self.toolbar = self.addToolBar("Opciones")
		self.toolbar.addAction(newAction)
		self.toolbar.addAction(openAction)
		self.toolbar.addAction(saveAction)
		self.toolbar.addSeparator()
		self.toolbar.addAction(printAction)
		self.toolbar.addSeparator()
		self.toolbar.addAction(findAction)
		self.toolbar.addAction(cutAction)
		self.toolbar.addAction(copyAction)
		self.toolbar.addAction(pasteAction)
		self.toolbar.addAction(undoAction)
		self.toolbar.addAction(redoAction)
		self.toolbar.addSeparator()

		self.addToolBarBreak()

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&Archivo')
		fileMenu.addAction(exitAction)

		self.setGeometry(300, 300, 300, 200)
		self.setWindowTitle('Frida')
		self.showMaximized()

#------- Text Edit ----------------------------------- 

		self.text = LineTextWidget()
		self.text.getTextEdit().setTabStopWidth(12)
		self.setCentralWidget(self.text)

#-------- Toolbar slots -----------------------------------

	def New(self):
		self.text.clear()
 
	def Open(self):
		filename = QFileDialog.getOpenFileName(self, 'Open File')
		f = open(filename, 'r')
		filedata = f.read()
		self.text.setText(filedata)
		f.close()
 
	def Save(self):
		filename = QFileDialog.getSaveFileName(self, 'Save File')
		f = open(filename, 'w')
		filedata = self.text.toPlainText()
		f.write(filedata)
		f.close()
 
	def Print(self):
		dialog = QPrintDialog()
		if dialog.exec_() == QDialog.Accepted:
			self.text.document().print_(dialog.printer())
 
	def Find(self):
		global f
		 
		find = Find(self)
		find.show()
 
		def handleFind():
 
			f = find.te.toPlainText()
			print(f)
			 
			if cs == True and wwo == False:
				flag = QTextDocument.FindBackward and QTextDocument.FindCaseSensitively
				 
			elif cs == False and wwo == False:
				flag = QTextDocument.FindBackward
				 
			elif cs == False and wwo == True:
				flag = QTextDocument.FindBackward and QTextDocument.FindWholeWords
				 
			elif cs == True and wwo == True:
				flag = QTextDocument.FindBackward and QTextDocument.FindCaseSensitively and QTextDocument.FindWholeWords
			 
			self.text.find(f,flag)
 
		def handleReplace():
			f = find.te.toPlainText()
			r = find.rp.toPlainText()
 
			text = self.text.toPlainText()
			 
			newText = text.replace(f,r)
 
			self.text.clear()
			self.text.append(newText)
		 
		find.src.clicked.connect(handleFind)
		find.rpb.clicked.connect(handleReplace)
 
 
	def Undo(self):
		self.text.undo()
 
	def Redo(self):
		self.text.redo()
 
	def Cut(self):
		self.text.cut()
 
	def Copy(self):
		self.text.copy()
 
	def Paste(self):
		self.text.paste()
 
	def DateTime(self):
 
		date = Date(self)
		date.show()
 
		date.ok.clicked.connect(self.insertDate)
 
	def insertDate(self):
		global choiceStr
		print(choiceStr)
		self.text.append(choiceStr)
		 
	def CursorPosition(self):
		line = self.text.textCursor().blockNumber()
		col = self.text.textCursor().columnNumber()
		linecol = ("Line: "+str(line)+" | "+"Column: "+str(col))
		self.status.showMessage(linecol)
 
	def FontFamily(self,font):
		font = QFont(self.fontFamily.currentFont())
		self.text.setCurrentFont(font)
 
	def FontSize(self, fsize):
		size = (int(fsize))
		self.text.setFontPointSize(size)
 
	def FontColor(self):
		c = QColorDialog.getColor()
 
		self.text.setTextColor(c)
		 
	def FontBackColor(self):
		c = QColorDialog.getColor()
 
		self.text.setTextBackgroundColor(c)
			 
	def lThrough(self):
		lt = QFont.style()
 
	def Indent(self):
		tab = "\t"
		cursor = self.text.textCursor()
 
		start = cursor.selectionStart()
		end = cursor.selectionEnd()
 
		cursor.setPosition(end)
		cursor.movePosition(cursor.EndOfLine)
		end = cursor.position()
 
		cursor.setPosition(start)
		cursor.movePosition(cursor.StartOfLine)
		start = cursor.position()
 
 
		while cursor.position() < end:
			global var
 
			print(cursor.position(),end)
			 
			cursor.movePosition(cursor.StartOfLine)
			cursor.insertText(tab)
			cursor.movePosition(cursor.Down)
			end += len(tab)
 
			'''if cursor.position() == end:
				var +=1
 
			if var == 2:
				break'''
	

# def window():
# 	app = QApplication(sys.argv)

# 	w = QWidget()
# 	# b = QLabel(w)
# 	# b.setText("Hello World!")
# 	w.setGeometry(100, 100, 200, 50)
# 	# b.move(50, 20)
# 	w.setWindowTitle("Frida")
# 	w.show()
# 	sys.exit(app.exec())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = FridaMainWindow()
	sys.exit(app.exec_())