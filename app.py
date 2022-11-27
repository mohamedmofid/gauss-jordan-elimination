import sys
from PySide2.QtWidgets import (QApplication, QWidget,QMessageBox)
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex
# from PyQt5.uic import loadUiType
from mainwindow import Ui_Form as ui
from solution import Ui_Form as solution_ui
from solver import gaussjordan

# ui, _= loadUiType('startwindow.ui')
# solution_ui, _= loadUiType('solutionwindow.ui')

class MatrixModel(QAbstractTableModel):
	def __init__(self, data):
		super().__init__()
		self._data = data
		

	def rowCount(self, parent=QModelIndex()):
		return len(self._data)

	def columnCount(self, parent=QModelIndex()):
		try:
			if len(self._data)==0:
				return 0
			return len(max(self._data, key=len))
		except:
			return 0
	
	def is_empty(self):
		return False if self._data else True

	def headerData(self, col, orientation, role):
        # if orientation == Qt.Horizontal and role == Qt.DisplayRole:
        #     return self._data.columns[col]
		return 0

	def data(self, index, role=Qt.DisplayRole):
		# display data
		if role == Qt.DisplayRole:
			# print('Display role:', index.row(), index.column())
			try:
				return self._data[index.row()][index.column()]
			except IndexError:
				return ''
	@staticmethod
	def RepresentsInt(s):
		try: 
			int(s)
			return True
		except ValueError:
			return False

	def setData(self, index, value, role=Qt.EditRole):		
		if role in (Qt.DisplayRole, Qt.EditRole):
			# print('Edit role:', index.row(), index.column())
			# if value is blank
			if not value:
				return False
			elif not self.RepresentsInt(value):
				return False
			self._data[index.row()][index.column()] = value
			self.dataChanged.emit(index, index)
		return True

	def flags(self, index):
		return super().flags(index) | Qt.ItemIsEditable
        
	def addColumn(self):
		# newColumn = self.columnCount()
		# self.beginInsertColumns(QModelIndex(), 0, newColumn)
		for row in self._data:
			row.append(0)
		self.layoutChanged.emit()
		# self.endInsertColumns()

	def addrow(self):
		# newRow = self.rowCount()
		# self.beginInsertRows(QModelIndex(), newRow, newRow)
		self._data.append([0 for i in range(len(self._data[0]))]) # no need to use max becaus we are using a square matrix
		self.layoutChanged.emit()
		# self.endInsertRows()
	def remove_column(self):
		if self.is_empty()!=True:		
			for row in self._data:
				row.pop()
				if len(row)==0:
					self._data.remove(row)
			self.layoutChanged.emit()
		
	def remove_row(self):
		if not self.is_empty():
			self._data.pop() 
			self.layoutChanged.emit()

	def add_dir(self):
		self.addColumn()
		self.addrow()

	def get_data(self):
		return self._data

	def rest(self):
		self._data = [[0]]
		self.layoutChanged.emit()

class Solution_window(solution_ui,QWidget):
	def __init__(self,text=None,parent=None):
		super(Solution_window, self).__init__(parent)
		# QWidget.__init__(self)
		self.setupUi(self)
		self.window_width, self.window_height = 400, 250
		self.setWindowTitle("Results")
		self.setMinimumSize(self.window_width, self.window_height)
		self.rewrite_solution(text)
		self.handel_buttons()
	def rewrite_solution(self,text):
		self.solution_text.setText(text)
	def ok(self):
		self.close()
	def handel_buttons(self):
		self.ok_button.clicked.connect(self.ok)

class MainApp(ui,QWidget):
	def __init__(self,parent=None):
		super(MainApp , self).__init__(parent)
		# QWidget.__init__(self)
		self.setupUi(self)
		self.window_width, self.window_height = 443, 333
		self.setMinimumSize(self.window_width, self.window_height)
		self.setWindowTitle("Matrix Solover")
		self.setStyleSheet('''
			QWidget {
				font-size: 10px;
			}
            QTableView {
                padding:0px;
                text-align:center;
                color: #5a5a5a;
                border :None;
            }
            QTableView::item {
                padding:0px;
                text-align:center;
                color: #5a5a5a;
                border :None;
                }
		''')		
		
		self.a_data_model = MatrixModel(data)
		self.b_data_model = MatrixModel(data2)
		self.matrix_a.setModel(self.a_data_model)
		self.matrix_b.setModel(self.b_data_model)
		# self.matrix_a.sizeHintForColumn(30)
		# self.matrix_b.sizeHintForColumn(30)
		# QTableView.sizeHintForIndex(30)
    	# view.setColumnWidth(1, 100)
		self.solution = Solution_window()
		self.Handel_Buttons()
	@staticmethod
	def is_zero_list(ls):
		return True if ls.count(0) == len(ls) else False
		# is_zero = False
		# for i in ls:
		# 	if i!=0:
		# 		is_zero = False
		# 	else:
		# 		is_zero = True
		# 		break
		# return is_zero
	def solve(self):
		a = self.a_data_model.get_data()
		b = self.b_data_model.get_data()
		b = list(map(lambda b:int(b[0]),b))
		# b = list(map(lambda b:int(b[0]),b))
		# print(a,b)
		# print(type(b[-1]))
		if self.is_zero_list(a[-1]) and b[-1] == 0:
			return QMessageBox.warning(self ,'Bad Input', "A system infinite solutions")
		elif self.is_zero_list(a[-1]) and b[-1] != 0:
			return QMessageBox.warning(self ,'Bad Input', "A system has no solution")

		if self.is_zero_list(b) and len(a[0])>len(a):
			return QMessageBox.warning(self ,'Bad Input', "A system infinite solutions")
		elif self.is_zero_list(b) and len(a[0])<len(a):
			return QMessageBox.warning(self ,'Bad Input', "A system trivial solutions")
		
		solution_str = gaussjordan(a=a,b=b)
		# print(solution_str)
		self.solution.rewrite_solution(solution_str)
		self.solution.show()
		# QMessageBox.information(self ,'solution',solution_str)

	def add_rows(self):
		self.a_data_model.addrow()
		self.b_data_model.addrow()
	def remove_rows(self):
		self.a_data_model.remove_row()
		self.b_data_model.remove_row()
	def rest(self):
		self.a_data_model.rest()
		self.b_data_model.rest()
	def Handel_Buttons(self):
        ## handel all buttons in the app
		self.add_row.clicked.connect(self.add_rows)
		self.add_column.clicked.connect(self.a_data_model.addColumn)
		self.remove_row.clicked.connect(self.remove_rows)
		self.remove_column.clicked.connect(self.a_data_model.remove_column)
		self.clear_a.clicked.connect(self.rest)
		self.solve_button.clicked.connect(self.solve)
		

if __name__ == '__main__':
	data = [[0,0,0],[0,0,0],[0,0,0]]
	data2 = [[0],[0],[0]]

	app = QApplication(sys.argv)
	
	myApp = MainApp()
	myApp.show()

	try:
		sys.exit(app.exec_())
	except SystemExit:
		print('Closing Window...')
