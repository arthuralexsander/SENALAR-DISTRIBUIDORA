import sys
import keyword
from PyQt5 import uic, QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QErrorMessage, QTableWidgetItem, QLineEdit, QDialog, QMainWindow, QMessageBox, QApplication, QStackedWidget, QTabWidget
from PyQt5.QtCore import Qt
from typing import final
from sqlite3 import Cursor
import mysql
import mysql.connector
from mysql.connector import Error

from login import Ui_login
from telainicial import Ui_inicial

# Conectar com a Database
banco = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        port = '3306',
        password = '123456',
        database = 'senalar'
)

class paginicial(QMainWindow):
    def __init__(self,*args,**argvs):
        super(paginicial,self).__init__(*args,**argvs)
        self.ui = Ui_inicial()
        self.ui.setupUi(self)
        
         #aqui se chama a stacked widget pages
        self.pag = QStackedWidget()
        self.pag_cad = QTabWidget()
        self.tabWidget = QTabWidget()
        # Adiciona as telas à QStackedWidget
        self.inicio_pag = QWidget()
        self.cadastro_pag = QWidget()
        
        #botoes
        self.ui.cad_botao.clicked.connect(self.irparacad)
        self.ui.cad_botao_2.clicked.connect(self.irparacad)
        self.ui.inicio_botao.clicked.connect(self.irparainicio)
        self.ui.inicio_botao_2.clicked.connect(self.irparainicio)
        self.ui.nf_botao.clicked.connect(self.irparanf)
        self.ui.nf_botao_2.clicked.connect(self.irparanf)
        self.ui.estoque_botao.clicked.connect(self.irparaestoque)
        self.ui.estoque_botao_2.clicked.connect(self.irparaestoque)
        self.ui.saida_botao.clicked.connect(self.irparasaida)
        self.ui.saida_botao_2.clicked.connect(self.irparasaida)
        
    #funções para chamar as telas
    def irparainicio(self):
        self.ui.pag.setCurrentIndex(0)

    def irparacad(self):
        self.ui.pag.setCurrentIndex(1)
        self.ui.tab_cad.setCurrentIndex(0)

    def irparanf(self):
        self.ui.pag.setCurrentIndex(2)
        self.ui.tabWidget.setCurrentIndex(0)
    
    def irparaestoque(self):
        self.ui.pag.setCurrentIndex(3)

    def irparasaida(self):
        self.ui.pag.setCurrentIndex(4) 

    def fechar_menu(self):
        self.ui.menu_icones.setHidden(True)
    
    
class login(QMainWindow):
    def __init__(self,*args,**argvs):
        super(login,self).__init__(*args,**argvs)
        self.ui = Ui_login()
        self.ui.setupUi(self)
        self.ui.bt_vsenha.clicked.connect(self.mostrar_senha)
        self.ui.bt_login.clicked.connect(self.entrar)


    
    def mostrar_senha(self):
        if self.ui.senha.echoMode()==QLineEdit.Normal:
            self.ui.senha.setEchoMode(QLineEdit.Password)
        else:
            self.ui.senha.setEchoMode(QLineEdit.Normal)


    def entrar(self):
        usuario = self.ui.usuario.text()
        senha = self.ui.senha.text()

        #iniciar o cursor
        Cursor = banco.cursor()

        busca = "SELECT ra, cpf from funcionarios WHERE ra = %s and cpf = %s"
        busca2 = (usuario,senha)

        Cursor.execute(busca,busca2)
        for(ra,cpf) in Cursor.fetchall():
                if usuario == ra and senha == cpf:
                        msg = QMessageBox()
                        msg.setText("LOGIN EFETUADO COM SUCESSO!")
                        msg.setWindowTitle("SENALAR")
                        msg.setWindowIcon(QtGui.QIcon("Logo sem circulo.png"))
                        msg.setStyleSheet("background-color: rgb(0, 0, 0);")
                        msg.setStyleSheet("color: rgb(0, 0, 0);")
                        msg.exec_() 
                        self.tela = paginicial()
                        self.tela.show()
                        login.hide(self)
                        self.tela.fechar_menu()
                        self.tela.irparainicio()
                else:
                        QMessageBox.critical(login, "Erro", "Usuário ou senha incorretos!")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = login()
    window.show()
    sys.exit(app.exec_())