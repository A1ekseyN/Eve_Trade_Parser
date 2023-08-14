# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import time


from lp_store_parser import items_prices, lp_calculator, view_result, items_2_table
from settings import sort_list, version


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        progress_bar = 0

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 867)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setObjectName("label")
        self.calculate = QtWidgets.QPushButton(self.centralwidget)
        self.calculate.setGeometry(QtCore.QRect(990, 100, 89, 27))
        self.calculate.setObjectName("Calculate")
        self.checkBox_Sort_Sell = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Sort_Sell.setGeometry(QtCore.QRect(280, 100, 78, 20))
        self.checkBox_Sort_Sell.setObjectName("checkBox_Sort_Sell")
        self.checkBox_Sort_Buy = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Sort_Buy.setGeometry(QtCore.QRect(220, 100, 78, 20))
        self.checkBox_Sort_Buy.setObjectName("checkBox_Sort_Buy")
        self.Text_Sort = QtWidgets.QLabel(self.centralwidget)
        self.Text_Sort.setGeometry(QtCore.QRect(220, 70, 55, 16))
        self.Text_Sort.setObjectName("Text_Sort")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(990, 0, 255, 16))
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 40, 1071, 20))
        self.line.setMinimumSize(QtCore.QSize(118, 0))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.checkBox_Filter_All = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Filter_All.setGeometry(QtCore.QRect(420, 100, 78, 20))
        self.checkBox_Filter_All.setObjectName("checkBox_Filter_All")
        self.Text_Filter = QtWidgets.QLabel(self.centralwidget)
        self.Text_Filter.setGeometry(QtCore.QRect(420, 70, 91, 16))
        self.Text_Filter.setObjectName("Text_Filter")
        self.checkBox_market_buy = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_market_buy.setGeometry(QtCore.QRect(20, 100, 78, 20))
        self.checkBox_market_buy.setObjectName("checkBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 121, 16))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(600, 70, 91, 16))
        self.label_4.setObjectName("label_4")
        self.checkBox_results_view = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_results_view.setGeometry(QtCore.QRect(600, 100, 78, 20))
        self.checkBox_results_view.setObjectName("checkBox_2")
        self.result_lp_table = QtWidgets.QTableWidget(self.centralwidget)
        self.result_lp_table.setGeometry(QtCore.QRect(30, 220, 1031, 591))
        self.result_lp_table.setObjectName("result_lp_table")
        self.result_lp_table.setColumnCount(0)
        self.result_lp_table.setRowCount(0)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 180, 1031, 23))
        self.progressBar.setProperty("value", progress_bar)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1090, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.calculate_result_button()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Eve Trade Parser"))
        self.label.setText(_translate("MainWindow", "State Protectorate"))
        self.calculate.setText(_translate("MainWindow", "Calculate"))
        self.checkBox_Sort_Sell.setText(_translate("MainWindow", "Sell"))
        self.checkBox_Sort_Buy.setText(_translate("MainWindow", "Buy"))
        self.checkBox_Sort_Sell.setChecked(True)                                    # Устанавливаем галочку в checkbox
        self.Text_Sort.setText(_translate("MainWindow", "Sort:"))
        self.label_3.setText(_translate("MainWindow", f"Version: {version}"))
        self.checkBox_Filter_All.setText(_translate("MainWindow", "All"))
        self.checkBox_Filter_All.setChecked(True)                                   # Устанавливаем галочку в checkbox
        self.Text_Filter.setText(_translate("MainWindow", "Items Filter:"))
        self.checkBox_market_buy.setText(_translate("MainWindow", "Jita"))
        self.checkBox_market_buy.setChecked(True)
        self.label_2.setText(_translate("MainWindow", "Buy Items Location:"))
        self.label_4.setText(_translate("MainWindow", "Results View:"))
        self.checkBox_results_view.setText(_translate("MainWindow", "All"))
        self.checkBox_results_view.setChecked(True)                                 # Галочка для отображения checkbox

    def calculate_result_button(self):
    # Функции для связи интерфейса и действий. Кнопка Calculate
        self.calculate.clicked.connect(self.view_results)

    def view_table(self):
        # Предположим, что у вас есть список results с результатами вычислений
        global items_2_table

        items_prices()
        lp_calculator()
        view_result()

        items_2_table = sorted(items_2_table, key=lambda x: x[sort_list], reverse=True)
#        print(f'items_2_table: {items_2_table}')

        # Установите количество строк и столбцов таблицы
        self.result_lp_table.setRowCount(len(items_2_table))
        self.result_lp_table.setColumnCount(len(items_2_table[0]) - 1)          # -1 потому, что одну таблицу я не учитываю

        # Установите заголовки столбцов
        column_headers = ["Item Name", "Item Buy Price", "Item Sell Price",
#                          "Item Total Price",
                          "Buy LP Profit", "Sell LP Profit", "Buy Volume"]
        self.result_lp_table.setHorizontalHeaderLabels(column_headers)

        # Заполните таблицу данными из списка results
        for row_index, row_data in enumerate(items_2_table):
            # Получите значения из словаря по ключам и заполните таблицу
            item_name = row_data['item_name']
            item_buy_price = row_data['item_buy_price']
            item_sell_price = row_data['item_sell_price']
#            item_total_price = row_data['item_total_price']
            buy_lp_profit = row_data['buy_lp_profit']
            sell_lp_profit = row_data['sell_lp_profit']
            buy_volume = row_data['buy_volume']
            # Добавьте остальные ключи и значения по необходимости

            # Создайте элементы QTableWidgetItem с полученными значениями
            try:
                item_name_item = QTableWidgetItem(str(item_name))
                item_buy_price_item = QTableWidgetItem(str(int(item_buy_price)))
                item_sell_price_item = QTableWidgetItem(str(int(item_sell_price)))
#                item_total_price = QTableWidgetItem(str(item_total_price))
                buy_lp_profit = QTableWidgetItem(str(buy_lp_profit))
                sell_lp_profit = QTableWidgetItem(str(sell_lp_profit))
                buy_volume = QTableWidgetItem(str(buy_volume))
            except:
                pass
            # Цвет для Sell ордеров
#            if item_sell_price_item >= 1000:
#                item_sell_price_item.setBackground(QtGui.QColor(0, 255, 0))

            # Установите ширину столбца с названием предмета
            self.result_lp_table.setColumnWidth(0, 350)
            self.result_lp_table.setColumnWidth(3, 100)
            self.result_lp_table.setColumnWidth(4, 100)
            self.result_lp_table.setColumnWidth(5, 100)

            # Установите элементы в таблицу на соответствующие позиции
            try:
                self.result_lp_table.setItem(row_index, 0, item_name_item)
                self.result_lp_table.setItem(row_index, 1, item_buy_price_item)
                self.result_lp_table.setItem(row_index, 2, item_sell_price_item)
#                self.result_lp_table.setItem(row_index, 3, item_total_price)
                self.result_lp_table.setItem(row_index, 3, buy_lp_profit)
                self.result_lp_table.setItem(row_index, 4, sell_lp_profit)
                self.result_lp_table.setItem(row_index, 5, buy_volume)
            except:
                pass

#            for col_index, cell_data in enumerate(row_data):
#                item = QTableWidgetItem(str(cell_data))
#                print(f'item: {item}')
#                print(f'row_index: {row_index}')
#                print(f'col_index: {col_index}')
#                print(f'Cell_data: {cell_data}')
##                self.result_lp_table.setItem(row_index, col_index, item)

    def view_results(self):
        # Получение и вычисление данных
        print('Test calculate_results button')
#        items_prices()
#        lp_calculator()
        self.view_table()
        #view_result()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
