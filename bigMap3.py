import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtWidgets import  QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt

from api_utils import get_coords, get_degree_size
from map_utils import get_map

class myMap:
    def __init__(self):
        self.z = 9
        self.lat = 35.005
        self.lon = 35.005
        self.dw = 35.009
        self.dh = 35.007
my_map = myMap()    
    
# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(600, 600))            # Устанавливаем размеры
        self.setWindowTitle("Большая задача")           # Устанавливаем заголовок окна
        self.central_widget = QWidget(self)             # Создаём центральный виджет
        self.setCentralWidget(self.central_widget)      # Устанавливаем центральный виджет
        self.grid_layout = QGridLayout()                # Создаём QGridLayout
        self.central_widget.setLayout(self.grid_layout) # Устанавливаем данное размещение в центральный виджет
        # метка и кнопки
        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setText("Адрес:")
        self.grid_layout.addWidget(self.label, 0, 0, 1, 2)   # Добавляем метку в сетку 
        #карта
        self.image = QLabel()
        self.grid_layout.addWidget(self.image, 1, 3, 10, 10)
        #self.pixmap = QPixmap("data//map.png")
        #self.image.setPixmap(self.pixmap)
        
        self.plus = QPushButton("+", self)
        self.grid_layout.addWidget(self.plus, 1, 14, 1, 1) 
        self.plus.clicked.connect(self.plus_z)
        self.plus.hide()
        
        self.minus = QPushButton("-", self)
        self.grid_layout.addWidget(self.minus, 1, 0, 1, 1) 
        self.minus.clicked.connect(self.minus_z)
        self.minus.hide()
        
        self.left = QPushButton("Влево", self)
        self.grid_layout.addWidget(self.left, 1, 4, 1, 2) 
        self.left.clicked.connect(self.shiftL)        
        self.left.hide()
        self.up = QPushButton("Вверх", self)
        self.grid_layout.addWidget(self.up, 1, 6, 1, 2) 
        self.up.clicked.connect(self.shiftU)        
        self.up.hide()
        self.right = QPushButton("Вправо", self)
        self.grid_layout.addWidget(self.right, 1, 8, 1, 2) 
        self.right.clicked.connect(self.shiftR)        
        self.right.hide()
        self.down = QPushButton("Вниз", self)
        self.grid_layout.addWidget(self.down, 1, 10, 1, 2) 
        self.down.clicked.connect(self.shiftD)        
        self.down.hide()
        
        # поле
        self.adress = QLineEdit()
        self.adress.setFont(font)
        self.grid_layout.addWidget(self.adress, 0, 3, 1, 10)   # Добавляем поле в сетку
        self.adress.setText('Пестеля, 5')
        # поле для вывода изображения карты
        # кнопка Найти
        self.btn2 = QPushButton("Найти", self)
        self.grid_layout.addWidget(self.btn2, 0, 13, 1, 2)   # Добавляем кнопку в сетку
        self.btn2.clicked.connect(self.new_search)    

    def new_search(self):
        toponym_to_find = self.adress.text()
        print(toponym_to_find)
        self.left.show()
        self.right.show()
        self.up.show()
        self.down.show()
        self.plus.show()
        self.minus.show()
        # Получаем координаты центра карты
        my_map.lat, my_map.lon = get_coords(toponym_to_find).split()
        my_map.dw, my_map.dh  = get_degree_size(toponym_to_find)
        print(my_map.dw)
        print(my_map.dh)
        
        # обновить изображение
        self.change_z()
    
    # уменьшить  
    def minus_z(self):
        if my_map.z > 0: 
            my_map.z = my_map.z - 1
        self.change_z()
    # увеличить    
    def plus_z(self):
        if my_map.z < 17:
            my_map.z = my_map.z + 1
        self.change_z() 
    # вправо   
    def shiftR(self):
        pass
        
    # влево
    def shiftL(self):
        pass 
    
    # вверх
    def shiftU(self):
        # считаем смещение центра карты, с учетом коэф. маштабирования z
        my_map.lon = float(my_map.lon) + float(my_map.dh) * 2 ** int(my_map.z)
        my_map.lon = my_map.lon - float(my_map.dh)
        self.change_z()
    
    # вниз
    def shiftD(self):
        my_map.lon = float(my_map.lon) - float(my_map.dh) * 2 ** int(my_map.z)
        my_map.lon = my_map.lon + float(my_map.dh)
        self.change_z()
  
        
    def change_z(self):      
        
        params = {
        "ll": ",".join([str(my_map.lat), str(my_map.lon)]),
        "z":str(my_map.z),
        "l":"map"
        }
        
        # обновить изображение
        self.pixmap = QPixmap(get_map(params))
        self.image.setPixmap(self.pixmap)
        self.btn2.setEnabled(True) # включить кнопку "Найти"
              

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
