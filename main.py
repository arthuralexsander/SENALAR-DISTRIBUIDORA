import sys
import keyword
from PyQt5 import uic, QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QErrorMessage, QTableWidgetItem, QLineEdit, QDialog, QMainWindow, QMessageBox, QApplication, QStackedWidget, QTabWidget, QTableWidget
from PyQt5.QtCore import Qt
from typing import final
from sqlite3 import Cursor
import mysql
import mysql.connector, webbrowser
from mysql.connector import Error

from login import Ui_login
from telainicial import Ui_inicial

# Conectar com a Database
banco = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        port = '3306',
        password = 'Senac2023',
        database = 'senalar'
)

class paginicial(QMainWindow):
    def __init__(self,*args,**argvs):
        super(paginicial,self).__init__(*args,**argvs)
        self.ui = Ui_inicial()
        self.ui.setupUi(self)
        #vetor para armazenar codigos e quantidades tela de vendas
        self.vetor1 = []
        self.vetor2 = []
        #vetor para armazenar codigos e quantidades tela de nota fiscal
        self.vetorcodnf = []
        self.vetorqtdnf = []
        
        self.setWindowTitle("SENALAR")
        self.setWindowIcon(QtGui.QIcon("Logo sem circulo.png"))
         #aqui se chama a stacked widget pages
        self.pag = QStackedWidget()
        self.pag_cad = QTabWidget()
        self.tabWidget = QTabWidget()
        # Adiciona as telas à QStackedWidget
        self.inicio_pag = QWidget()
        self.cadastro_pag = QWidget()


        #mascaras 
        self.ui.dtnasc_func.setInputMask('99/99/9999')
        self.ui.cpf_func.setInputMask('999.999.999-99')
        self.ui.admissao_func.setInputMask('99/99/9999')
        self.ui.telefone_func.setInputMask('(99)99999-9999')
        self.ui.cep_func.setInputMask('99999-999')
        self.ui.cpf_cliente.setInputMask('999.999.999-99')
        self.ui.cnpj_transp.setInputMask('99.999.999/9999-99')
        self.ui.cep_transp.setInputMask('99999-999')
        self.ui.cep_cliente.setInputMask('99999-999')
        self.ui.cep_remetente.setInputMask('99999-999')
        self.ui.emissao_dn.setInputMask('99/99/9999')
        self.ui.entrada_dn.setInputMask('99/99/9999')
        self.ui.cadastro_dn.setInputMask('99/99/9999')
        
        #self.ui.desconto_campo.setInputMask('000%')
        self.ui.cnpj_remetente.setInputMask('99.999.999/9999-99')

        #botoes navegação
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
        
        #botoes cadastro
        self.ui.cadastrar_func.clicked.connect(self.cadastrarfunc)
        self.ui.bt_alternar.clicked.connect(self.alternar)
        self.ui.cadastrar_prod.clicked.connect(self.cad_produtos)
        self.ui.cadastrar_cliente.clicked.connect(self.cadastrar_cliente)
        self.ui.cadastrar_transp.clicked.connect(self.cad_transp)
        self.ui.adicionar_prod.clicked.connect(self.addprodnf)

        #botoes consulta
        self.ui.bt_consultar2.clicked.connect(self.consultarfunc)
        self.ui.consultar_prod.clicked.connect(self.consulta_prod)
        self.ui.busca_codprod.clicked.connect(self.consultaprodnf)
        self.ui.adicionar_prod.clicked.connect(self.tabelanf)


        #botoes atualizar
        self.ui.atualizar_func.clicked.connect(self.atualizarfunc)
        self.ui.atualizar_prod.clicked.connect(self.att_produtos)


        #botoes excluir
        self.ui.excluir_func.clicked.connect(self.excluirfunc)
        self.ui.excluir_prod.clicked.connect(self.excluir_prod)
        self.ui.remover_prod.clicked.connect(self.removerinsercaonf)

        #botoes lançar 
        self.ui.lancar_prod.clicked.connect(self.lancarremet)
        self.ui.lancar_prod.clicked.connect(self.dados_nota)
        self.ui.lancar_prod.clicked.connect(self.lancarnf)


        #botao pdf
        self.ui.manual_inicial.clicked.connect(self.chamar_pdf)

        #botoes limpar
        self.ui.limpar_cliente.clicked.connect(self.limparcli)
        self.ui.limpar_remetente.clicked.connect(self.limparremet)
        self.ui.limpar_transp.clicked.connect(self.limpar_transp)
        self.ui.limpar_prod.clicked.connect(self.limpar_prod)
        self.ui.busca_botao.clicked.connect(self.buscar_estoque)

        #vendas
        self.ui.cod_campo.editingFinished.connect(self.addvendas)
        self.ui.quantidade_campo.editingFinished.connect(self.subtotal)
        self.ui.desconto_campo.editingFinished.connect(self.desconto)
        self.ui.desconto_campo.editingFinished.connect(self.zerar)
        self.ui.bt_adicionar.clicked.connect(self.adicionarcarrinho)
        self.ui.bt_adicionar.clicked.connect(self.somartotal)
        self.ui.bt_remover.clicked.connect(self.removercarrinho)
        self.ui.bt_remover.clicked.connect(self.somartotal)
        self.ui.bt_cancelar_cupom.clicked.connect(self.cancelarcompra)


        #dec estoque
        self.ui.bt_finalizar_cupom.clicked.connect(self.finalizarcompra)


    #funções para mudar as paginas
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
    # Função de cadastrar funcionarios
    def cadastrarfunc(self):
        rafunc = self.ui.ra_func.text()
        emailfunc = self.ui.email_func.text()
        cpffunc = self.ui.cpf_func.text()
        nomefunc = self.ui.nome_func.text()
        dtnasc = self.ui.dtnasc_func.text()
        admissaofunc = self.ui.admissao_func.text()
        telefonefunc = self.ui.telefone_func.text()
        cepfunc = self.ui.cep_func.text()
        cidadefunc = self.ui.cidade_func.text()
        bairrofunc = self.ui.bairro_func.text()
        ruafunc = self.ui.rua_func.text()
        numerofunc = self.ui.numero_func.text()
        estadofunc = self.ui.estado_func.currentText()
        Cursor = banco.cursor()
        # caso os campos nao estejam preenchidos irá mostrar uma tela de erro
        if not rafunc or not dtnasc or not cpffunc or not nomefunc or not admissaofunc or not telefonefunc or not cepfunc or not cidadefunc or not bairrofunc or not ruafunc or not numerofunc or not emailfunc:
            msg = QMessageBox()
            msg.setText('PREENCHA TODOS OS CAMPOS!')
            msg.setWindowTitle("ATENÇÃO")
            msg.setWindowIcon(QtGui.QIcon("Logo sem circulo.png"))

            msg.setStyleSheet("color: rgb(0, 0, 0);")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        # caso a condicao de ter os campos for satisfeita o usuario sera cadastrado
        else:
            inserirtabela = ("INSERT INTO funcionarios VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            formatacao = (rafunc,cpffunc,emailfunc,nomefunc,dtnasc,admissaofunc,telefonefunc,cepfunc,cidadefunc,bairrofunc,ruafunc,numerofunc,estadofunc)
            Cursor.execute(inserirtabela,formatacao)
            msg = QMessageBox()
            msg.setText('CADASTRO ATUALIZADO')
            rafunc = self.ui.ra_func.setText('')
            dtnasc = self.ui.dtnasc_func.setText('')
            cpffunc = self.ui.cpf_func.setText('')
            nomefunc = self.ui.nome_func.setText('')
            admissaofunc = self.ui.admissao_func.setText('')
            telefonefunc = self.ui.telefone_func.setText('')
            cepfunc = self.ui.cep_func.setText('')
            cidadefunc = self.ui.cidade_func.setText('')
            bairrofunc = self.ui.bairro_func.setText('')
            ruafunc = self.ui.rua_func.setText('')
            numerofunc = self.ui.numero_func.setText('')
            emailfunc = self.ui.email_func.setText('')
            banco.commit()
            Cursor.close()
    # função de consultar funcionarios pelo codigo
    def consultarfunc(self):
        crafunc = self.ui.ra_func.text()
        Cursor = banco.cursor()
        try:
            # faz o select e insere o texto nos campos
            consulta = (f"SELECT * from funcionarios WHERE ra = {crafunc}")
            Cursor.execute(consulta)
            selecao = Cursor.fetchall()
            rafunc = self.ui.ra_func.setText(selecao[0][0])
            cpffunc = self.ui.cpf_func.setText(selecao[0][1])
            emailfunc = self.ui.email_func.setText(selecao[0][2])
            nomefunc = self.ui.nome_func.setText(selecao[0][3])
            dtnasc = self.ui.dtnasc_func.setText(selecao[0][4])
            admissaofunc = self.ui.admissao_func.setText(selecao[0][5])
            telefonefunc = self.ui.telefone_func.setText(selecao[0][6])
            cepfunc = self.ui.cep_func.setText(selecao[0][7])
            cidadefunc = self.ui.cidade_func.setText(selecao[0][8])
            bairrofunc = self.ui.bairro_func.setText(selecao[0][9])
            ruafunc = self.ui.rua_func.setText(selecao[0][10])
            numerofunc = self.ui.numero_func.setText(selecao[0][11])
            estadofunc = self.ui.estado_func.setCurrentText(selecao[0][12])
            Cursor.close()
            # Enviar mensagem de erro caso nao existir funcionario com este codigo
        except:
            msg = QMessageBox()
            msg.setText('CODIGO NAO ENCONTRADO')
            msg.setWindowTitle("ATENÇÃO")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QtGui.QIcon("Logo sem circulo.png"))
            msg.setStyleSheet("color: rgb(0, 0, 0);")
            msg.exec_()
            return
    # Atualizar dados do funcionario
    def atualizarfunc(self):
        rafunc = self.ui.ra_func.text()
        dtnasc = self.ui.dtnasc_func.text()
        cpffunc = self.ui.cpf_func.text()
        nomefunc = self.ui.nome_func.text()
        admissaofunc = self.ui.admissao_func.text()
        telefonefunc = self.ui.telefone_func.text()
        cepfunc = self.ui.cep_func.text()
        cidadefunc = self.ui.cidade_func.text()
        bairrofunc = self.ui.bairro_func.text()
        ruafunc = self.ui.rua_func.text()
        numerofunc = self.ui.numero_func.text()
        emailfunc = self.ui.email_func.text()
        estadofunc = self.ui.estado_func.currentText()

        Cursor = banco.cursor()
        # Realizar a atualização dos dados 
        try:
            atualizar = (f"UPDATE funcionarios SET ra = %s, cpf = %s, email = %s, nome = %s, data_nascimento = %s, admissao = %s, telefone = %s, cep = %s, cidade = %s, bairro = %s, rua = %s, numero = %s, estado = %s WHERE ra = {rafunc}")
            campos = (rafunc,cpffunc, emailfunc, nomefunc, dtnasc, admissaofunc, telefonefunc, cepfunc, cidadefunc, bairrofunc, ruafunc, numerofunc, estadofunc)
            Cursor.execute(atualizar,campos)
            banco.commit()
            Cursor.close()
        except:
            return
        rafunc = self.ui.ra_func.setText('')
        dtnasc = self.ui.dtnasc_func.setText('')
        cpffunc = self.ui.cpf_func.setText('')
        nomefunc = self.ui.nome_func.setText('')
        admissaofunc = self.ui.admissao_func.setText('')
        telefonefunc = self.ui.telefone_func.setText('')
        cepfunc = self.ui.cep_func.setText('')
        cidadefunc = self.ui.cidade_func.setText('')
        bairrofunc = self.ui.bairro_func.setText('')
        ruafunc = self.ui.rua_func.setText('')
        numerofunc = self.ui.numero_func.setText('')
        emailfunc = self.ui.email_func.setText('')

    # excluir funcionario
    def excluirfunc(self):
        #Puxar o ra do funcionario para realizar a deleção
        crafunc = self.ui.ra_func.text()
        Cursor = banco.cursor()
        excluir = f"DELETE from funcionarios WHERE ra = {crafunc}"
        Cursor.execute(excluir)
        banco.commit()
        Cursor.close()

        rafunc = self.ui.ra_func.setText('')
        dtnasc = self.ui.dtnasc_func.setText('')
        cpffunc = self.ui.cpf_func.setText('')
        nomefunc = self.ui.nome_func.setText('')
        admissaofunc = self.ui.admissao_func.setText('')
        telefonefunc = self.ui.telefone_func.setText('')
        cepfunc = self.ui.cep_func.setText('')
        cidadefunc = self.ui.cidade_func.setText('')
        bairrofunc = self.ui.bairro_func.setText('')
        ruafunc = self.ui.rua_func.setText('')
        numerofunc = self.ui.numero_func.setText('')

    # alternar mascara de cpf e cnpj
    def alternar(self):
        if self.ui.bt_alternar.isChecked():
            self.ui.cpf_cliente_2.setInputMask('99.999.999/9999-99')
            self.ui.bt_alternar.setText('CNPJ')
        else: 
            self.ui.cpf_cliente_2.setInputMask('999.999.999-99')
            self.ui.bt_alternar.setText('CPF')


    #Função para cadastrar os clientes por meio da tela
    def cadastrar_cliente(self):
        #Coletar as informações da tela
        codigo = self.ui.codigo_cliente.text()
        cpf = self.ui.cpf_cliente.text()
        nome = self.ui.nome_cliente.text()
        email = self.ui.email_cliente.text()
        telefone = self.ui.telefone_cliente.text()
        dtnasc = self.ui.dtnasc_cliente.text()
        cep = self.ui.cep_cliente.text()
        cidade = self.ui.cidade_cliente.text()    
        bairro = self.ui.bairro_cliente.text()
        rua = self.ui.rua_cliente.text()
        numero = self.ui.numero_cliente.text()
        estado = self.ui.estado_cliente.currentText()
        Cursor = banco.cursor()

        #Caso não houver um nome digitado, irá ocorrer um erro
        if nome == '':
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Insira todos os valores para alterar.')
            errorMessage.exec_()

        #Senão
        else:
            sql = 'INSERT INTO clientes (nome, data_nasc, cpf, email, telefone, cep, estado, cidade, bairro, rua, numero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            valores = (nome, dtnasc, cpf, email, telefone, cep, estado, cidade, bairro, rua, numero)
            Cursor.execute(sql, valores)
            banco.commit()
            Cursor.close()

            codigo = self.ui.codigo_cliente.setText('')
            cpf = self.ui.cpf_cliente.setText('')
            nome = self.ui.nome_cliente.setText('')
            email = self.ui.email_cliente.setText('')
            telefone = self.ui.telefone_cliente.setText('')
            dtnasc = self.ui.dtnasc_cliente.setText('')
            cep = self.ui.cep_cliente.setText('')
            cidade = self.ui.cidade_cliente.setText('')
            bairro = self.ui.bairro_cliente.setText('')
            rua = self.ui.rua_cliente.setText('')
            numero = self.ui.numero_cliente.setText('')
            estado = self.ui.estado_cliente.setCurrentText('AC')


        

    #Modificar ítens da tabela cliente
    def atualizar_cliente(self):
        #Coletar as informações presentes na tela de cliente
        codigo = self.ui.codigo_cliente.text()
        cpf = self.ui.cpf_cliente.text()
        nome = self.ui.nome_cliente.text()
        email = self.ui.email_cliente.text()
        telefone = self.ui.telefone_cliente.text()
        dtnasc = self.ui.dtnasc_cliente.text()
        cep = self.ui.cep_cliente.text()
        cidade = self.ui.cidade_cliente.text()    
        bairro = self.ui.bairro_cliente.text()
        rua = self.ui.rua_cliente.text()
        numero = self.ui.numero_cliente.text()
        estado = self.ui.estado_cliente.currentText()
        Cursor = banco.cursor()

        #Todos os valores devem estar presentes 
        if nome == '' or codigo == '' or dtnasc == '' or cpf == '' or email == '' or telefone == '' or cep == '' or estado == '' or cidade == '' or bairro == '' or rua == '' or numero == '':
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Insira todos os valores para alterar.')
            errorMessage.exec_()

        #Senão
        else:
            #Código para atualizar: "UPDATE"
            sql = f"UPDATE clientes SET nome = '{nome}', data_nasc = '{dtnasc}', cpf = '{cpf}', email = '{email}', telefone = '{telefone}', cep = '{cep}', estado = '{estado}', cidade = '{cidade}', bairro = '{bairro}', rua = '{rua}', numero = '{numero}' WHERE codigo_cliente = '{codigo}'"
            Cursor.execute(sql)
            banco.commit()
            Cursor.close()
        
            codigo = self.ui.codigo_cliente.setText('')
            cpf = self.ui.cpf_cliente.setText('')
            nome = self.ui.nome_cliente.setText('')
            email = self.ui.email_cliente.setText('')
            telefone = self.ui.telefone_cliente.setText('')
            dtnasc = self.ui.dtnasc_cliente.setText('')
            cep = self.ui.cep_cliente.setText('')
            cidade = self.ui.cidade_cliente.setText('')
            bairro = self.ui.bairro_cliente.setText('')
            rua = self.ui.rua_cliente.setText('')
            numero = self.ui.numero_cliente.setText('')
            estado = self.ui.estado_cliente.setCurrentText('AC')

    #Função para consultar os clientes com base no nome ou código
    def consultar_cliente(self):
        #Coletar informações do campo nome e código
        codigo = self.ui.codigo_cliente.text()
        nome = self.ui.nome_cliente.text()
        Cursor = banco.cursor()

        #preguiça 
        if codigo == '' and nome == '':
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Insira um código ou nome para consulta.')
            errorMessage.exec_()

        #Caso apenas um dos dois não forem preenchidos:
        else:
            #Seleção do caso de nome inserido
            if codigo == '':
                sql = f"SELECT * FROM clientes WHERE nome = '{nome}'"
                Cursor.execute(sql)
                select = Cursor.fetchall()
                Cursor.close()

                #Se o código não existir
                if not select:
                    errorMessage = QtWidgets.QErrorMessage()
                    errorMessage.showMessage('Insira um código válido para consulta.')
                    errorMessage.exec_()

                else:
                    self.ui.codigo_cliente.setText(str(select[0][0]))
                    self.ui.nome_cliente.setText(str(select[0][1]))
                    self.ui.dtnasc_cliente.setText(str(select[0][2]))
                    self.ui.cpf_cliente.setText(str(select[0][3]))
                    self.ui.email_cliente.setText(str(select[0][4]))
                    self.ui.telefone_cliente.setText(str(select[0][5]))
                    self.ui.cep_cliente.setText(str(select[0][6]))
                    self.ui.estado_cliente.setCurrentText(str(select[0][7]))
                    self.ui.cidade_cliente.setText(str(select[0][8]))
                    self.ui.bairro_cliente.setText(str(select[0][9]))
                    self.ui.rua_cliente.setText(str(select[0][10]))
                    self.ui.numero_cliente.setText(str(select[0][11]))


        #Caso ambos forem digitados
            else:
                #Seleção total
                sql = f"SELECT * FROM clientes WHERE codigo_cliente = '{codigo}'"
                Cursor.execute(sql)
                select = Cursor.fetchall()
                Cursor.close()

                #Caso não existir os parâmetros
                if not select:
                    errorMessage = QtWidgets.QErrorMessage()
                    errorMessage.showMessage('Insira um código válido para consulta.')
                    errorMessage.exec_()

                else:
                    self.ui.codigo_cliente.setText(str(select[0][0]))
                    self.ui.nome_cliente.setText(str(select[0][1]))
                    self.ui.dtnasc_cliente.setText(str(select[0][2]))
                    self.ui.cpf_cliente.setText(str(select[0][3]))
                    self.ui.email_cliente.setText(str(select[0][4]))
                    self.ui.telefone_cliente.setText(str(select[0][5]))
                    self.ui.cep_cliente.setText(str(select[0][6]))
                    self.ui.estado_cliente.setCurrentText(str(select[0][7]))
                    self.ui.cidade_cliente.setText(str(select[0][8]))
                    self.ui.bairro_cliente.setText(str(select[0][9]))
                    self.ui.rua_cliente.setText(str(select[0][10]))
                    self.ui.numero_cliente.setText(str(select[0][11]))


    #Excluir o cliente do banco de dados
    def excluir_cliente(self):
        #Coletar los dados
        codigo = self.ui.codigo_cliente.text()
        nome = self.ui.nome_cliente.text()
        Cursor = banco.cursor()

        #Caso não estiverem inseridos nenhum dos parâmetros, ocorrerá um erro
        if codigo == '' and nome == '':
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Insira um código ou nome para ser excluido.')
            errorMessage.exec_()


        #Caso possuem parâmetros
        else:
            #Caso a consulta ocorra pelo código, irá acontecer pelo nome
            if codigo == '':
                sql = f"DELETE FROM clientes WHERE nome = '{nome}'"
                Cursor.execute(sql)
                banco.commit()
                Cursor.close()

                errorMessage = QtWidgets.QErrorMessage()
                errorMessage.showMessage('Cliente removido.')
                errorMessage.exec_()

            #Senão:
            else:
                sql = f"DELETE FROM clientes WHERE codigo_cliente = '{codigo}'"
                Cursor.execute(sql)
                banco.commit()
                Cursor.close()

                errorMessage = QtWidgets.QErrorMessage()
                errorMessage.showMessage('Cliente removido.')
                errorMessage.exec_()
        
        self.ui.codigo_cliente.setText('')
        self.ui.cpf_cliente.setText('')
        self.ui.nome_cliente.setText('')
        self.ui.email_cliente.setText('')
        self.ui.telefone_cliente.setText('')
        self.ui.dtnasc_cliente.setText('')
        self.ui.cep_cliente.setText('')
        self.ui.cidade_cliente.setText('')
        self.ui.bairro_cliente.setText('')
        self.ui.rua_cliente.setText('')
        self.ui.numero_cliente.setText('')
        self.ui.estado_cliente.setCurrentText('AC')
    # limpar campos          
    def limparcli(self):
        cod = self.ui.codigo_cliente.setText("")
        nome = self.ui.nome_cliente.setText("")
        dtn = self.ui.dtnasc_cliente.setText("")
        cpf = self.ui.cpf_cliente_2.setText("")
        email = self.ui.email_cliente.setText("")
        telefone = self.ui.telefone_cliente.setText("")
        cep = self.ui.cep_cliente.setText("")
        estado = self.ui.estado_cliente.setCurrentText("")
        cidade = self.ui.cidade_cliente.setText("")
        bairro = self.ui.bairro_cliente.setText("")
        rua = self.ui.rua_cliente.setText("")
        num = self.ui.numero_cliente.setText("")

    # atrelar botao da tela inicial para baixar o manual
    def chamar_pdf(self):
        webbrowser.open('https://drive.usercontent.google.com/u/0/uc?id=17k-VVooW3odleL_9rLqrGl9ISIbeuFIr&export=download')

    # cadastro da transportadora
    def cad_transp(self):
        codigo = self.ui.codigo_transp.text()
        cnpj = self.ui.cnpj_transp.text()
        nome = self.ui.nome_transp.text()
        telefone = self.ui.telefone_transp.text()
        cep = self.ui.cep_transp.text()
        cidade = self.ui.cidade_transp.text()
        bairro = self.ui.bairro_transp.text()
        rua = self.ui.rua_transp.text()
        numero = self.ui.numero_transp.text()
        estado = self.ui.estado_transp.currentText()
        Cursor = banco.cursor()
        # Se o campo estiver vazio, o cadastro não e feito.
        if not cnpj or not nome or not telefone or not cep or not cidade or not bairro or not rua or not numero or not estado:
            # Uma mensagem de erro é feita
            msg = QMessageBox()
            msg.setText('PREENCHA TODOS OS CAMPOS!')
            msg.setWindowTitle("ATENÇÃO")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QtGui.QIcon("Logo sem circulo.png"))
            msg.setStyleSheet("color: rgb(0, 0, 0);")
            msg.exec_()

        else:
            # caso o contrario realiza o cadastro da transportadora
            busca = "insert into transportadora (cnpj, nome, telefone, cep, cidade, bairro, rua, numero, estado) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            valores = (cnpj, nome, telefone, cep, cidade, bairro, rua, numero, estado)

            Cursor.execute(busca, valores)

            banco.commit()
            Cursor.close()



        # deixar os campos vazios
        codigo = self.ui.codigo_transp.setText('')
        cnpj = self.ui.cnpj_transp.setText('')
        nome = self.ui.nome_transp.setText('')
        telefone = self.ui.telefone_transp.setText('')
        cep = self.ui.cep_transp.setText('')
        cidade = self.ui.cidade_transp.setText('')
        bairro = self.ui.bairro_transp.setText('')
        rua = self.ui.rua_transp.setText('')
        numero = self.ui.numero_transp.setText('')
        estado = self.ui.estado_transp.itemText(1)

    # excluir a transportadora
    def excluir_transp(self):
        codigo = self.ui.codigo_transp.text()

        Cursor = banco.cursor()

        busca = f"delete from transportadora where tcodigo = '{codigo}'"

        Cursor.execute(busca)

        banco.commit()
        Cursor.close()

        codigo = self.ui.codigo_transp.setText('')

    # consultar transportadora
    def consultar_transp(self):
        codigo = self.ui.codigo_transp.text()

        Cursor = banco.cursor()
        try:
            busca = f"select * from transportadora where tcodigo = '{codigo}'"

            Cursor.execute(busca)

            busca = Cursor.fetchall()
            Cursor.close()

            cnpj = self.ui.cnpj_transp.setText(str(busca[0][1]))
            nome = self.ui.nome_transp.setText(str(busca[0][2]))
            telefone = self.ui.telefone_transp.setText(str(busca[0][3]))
            cep = self.ui.cep_transp.setText(str(busca[0][4]))
            cidade = self.ui.cidade_transp.setText(str(busca[0][5]))
            bairro = self.ui.bairro_transp.setText(str(busca[0][6]))
            rua = self.ui.rua_transp.setText(str(busca[0][7]))
            numero = self.ui.numero_transp.setText(str(busca[0][8]))
            uf = self.ui.estado_transp.setCurrentText(str(busca[0][9]))
        except: 
            return
        

        
    # atualizar a transportadora
    def atualizar_transp(self):
        codigo = self.ui.codigo_transp.text()
        cnpj = self.ui.cnpj_transp.text()
        nome = self.ui.nome_transp.text()
        telefone = self.ui.telefone_transp.text()
        cep = self.ui.cep_transp.text()
        cidade = self.ui.cidade_transp.text()
        bairro = self.ui.bairro_transp.text()
        rua = self.ui.rua_transp.text()
        numero = self.ui.numero_transp.text()
        estado = self.ui.estado_transp.currentText()

        Cursor = banco.cursor()
        
        busca = f"update transportadora set cnpj = '{cnpj}', nome = '{nome}', telefone = '{telefone}', cep = '{cep}', cidade = '{cidade}', bairro = '{bairro}', rua = '{rua}', numero = '{numero}', estado = '{estado}'"

        Cursor.execute(busca)

        banco.commit()
        Cursor.close

        codigo = self.ui.codigo_transp.setText('')
        cnpj = self.ui.cnpj_transp.setText('')
        nome = self.ui.nome_transp.setText('')
        telefone = self.ui.telefone_transp.setText('')
        cep = self.ui.cep_transp.setText('')
        cidade = self.ui.cidade_transp.setText('')
        bairro = self.ui.bairro_transp.setText('')
        rua = self.ui.rua_transp.setText('')
        numero = self.ui.numero_transp.setText('')
        estado = self.ui.estado_transp.itemText(1)

    # deixar os campos vazios
    def limpar_transp(self):
        codigo = self.ui.codigo_transp.setText('')
        cnpj = self.ui.cnpj_transp.setText('')
        nome = self.ui.nome_transp.setText('')
        telefone = self.ui.telefone_transp.setText('')
        cep = self.ui.cep_transp.setText('')
        cidade = self.ui.cidade_transp.setText('')
        bairro = self.ui.bairro_transp.setText('')
        rua = self.ui.rua_transp.setText('')
        numero = self.ui.numero_transp.setText('')


    #Função da tela de produtos
    #cadastro
    def cad_produtos(self):

        #campos da tela 
        nome = self.ui.nome_prod.text()
        marca = self.ui.marca_prod.text()
        estoquea = self.ui.estoque_a.text()
        estoquemin = self.ui.estoque_min.text()
        estoquemax = self.ui.estoque_max.text()
        unidade = self.ui.unidade_prod.text()
        precocusto = self.ui.precocusto_prod.text()
        precovenda = self.ui.precovenda_prod.text()
        sku = self.ui.sku_prod.text() 
        ncm = self.ui.ncm_prod.text()
        cean = self.ui.cean_prod.text()
        cfop = self.ui.cfop_prod.text()

        #caso algum dos campos esteja em branco não sera realizado o cadastro
        if nome == '' or marca == '' or estoquea == '' or estoquemin == '' or estoquemax == '' or unidade == '' or precocusto == '' or precovenda == '' or sku == '' or ncm == '' or cean == '' or cfop =='':
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Erro, preencha todos os campos corretamente.')
            errorMessage.exec_()
        
        #se os campos estiverem com informação sera realizado a função de cadastro
        else:
            #função de cadastro
            Cursor = banco.cursor()
            entrada = 'INSERT INTO produto (nome, marca, estoqueatual, estoquemin, estoquemax, unidade, precocusto, precovenda, sku, ncm, cean, cfop) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            valores = (nome, marca, estoquea, estoquemin, estoquemax, unidade, precocusto, precovenda, sku, ncm, cean, cfop)
            Cursor.execute(entrada,valores)
            banco.commit()
            Cursor.close()

            #limpar os campos após o cadastro
            nome = self.ui.nome_prod.setText('')
            marca = self.ui.marca_prod.setText('')
            estoquea = self.ui.estoque_a.setText('')
            estoquemin = self.ui.estoque_min.setText('')
            estoquemax = self.ui.estoque_max.setText('')
            unidade = self.ui.unidade_prod.setText('')
            precocusto = self.ui.precocusto_prod.setText('')
            precovenda = self.ui.precovenda_prod.setText('')
            sku = self.ui.sku_prod.setText('') 
            ncm = self.ui.ncm_prod.setText('')
            cean = self.ui.cean_prod.setText('')
            cfop = self.ui.cfop_prod.setText('')

    #atualizar
    def att_produtos(self):
        #campos da tela
        codigo = self.ui.codigo_prod.text()
        nome = self.ui.nome_prod.text()
        marca = self.ui.marca_prod.text()
        estoquea = self.ui.estoque_a.text()
        estoquemin = self.ui.estoque_min.text()
        estoquemax = self.ui.estoque_max.text()
        unidade = self.ui.unidade_prod.text()
        precocusto = self.ui.precocusto_prod.text()
        precovenda = self.ui.precovenda_prod.text()
        sku = self.ui.sku_prod.text() 
        ncm = self.ui.ncm_prod.text()
        cean = self.ui.cean_prod.text()
        cfop = self.ui.cfop_prod.text()

        #caso algum dos campos esteja em branco não sera efetuada a atualização
        if nome == '' or marca == '' or estoquea == '' or estoquemin == '' or estoquemax == '' or unidade == '' or precocusto == '' or precovenda == '' or sku == '' or ncm == '' or cean == '' or cfop =='':
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Erro, preencha todos os campos corretamente.')
            errorMessage.exec_()
        
        #se a condição dos campos preenchidos estiver correta sera efetuada a atualização
        else:
            #comando de atualização
            Cursor = banco.cursor()
            sql = f"UPDATE produto SET nome = '{nome}', marca = '{marca}', estoqueatual = '{estoquea}', estoquemin = '{estoquemin}', estoquemax = '{estoquemax}', unidade = '{unidade}', precocusto = '{precocusto}', precovenda = '{precovenda}', sku = '{sku}', ncm = '{ncm}', cean = '{cean}', cfop = '{cfop}' WHERE pcodigo ='{codigo}'"
            Cursor.execute(sql)
            banco.commit()
            Cursor.close()

            #limpar a tela após a atualização
            nome = self.ui.nome_prod.setText('')
            marca = self.ui.marca_prod.setText('')
            estoquea = self.ui.estoque_a.setText('')
            estoquemin = self.ui.estoque_min.setText('')
            estoquemax = self.ui.estoque_max.setText('')
            unidade = self.ui.unidade_prod.setText('')
            precocusto = self.ui.precocusto_prod.setText('')
            precovenda = self.ui.precovenda_prod.setText('')
            sku = self.ui.sku_prod.setText('') 
            ncm = self.ui.ncm_prod.setText('')
            cean = self.ui.cean_prod.setText('')
            cfop = self.ui.cfop_prod.setText('')

    #excluir da base de dados
    def excluir_prod(self):
        #Campos chave da tela
        codigo = self.ui.codigo_prod.text()
        nome = self.ui.nome_prod.text()

        #condição de erro: o nome ou o codigo estarem em branco
        if codigo == '' and nome == '':
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Erro.')
            errorMessage.exec_()

        else:
            #Função para a condicional codigo em branco, onde o nome será obrigatorio estar digitado para a exclusão do banco de dados
            if codigo == '':
                Cursor = banco.cursor()
                sql = f"DELETE  FROM produto WHERE nome = '{nome}'"
                Cursor.execute(sql)
                banco.commit()
                Cursor.close()

                errorMessage = QtWidgets.QErrorMessage()
                errorMessage.showMessage('Produto removido do sistema.')
                errorMessage.exec_()

                codigo = self.ui.codigo_prod.setText('')
                nome = self.ui.nome_prod.setText('')
                marca = self.ui.marca_prod.setText('')
                estoquea = self.ui.estoque_a.setText('')
                estoquemin = self.ui.estoque_min.setText('')
                estoquemax = self.ui.estoque_max.setText('')
                unidade = self.ui.unidade_prod.setText('')
                precocusto = self.ui.precocusto_prod.setText('')
                precovenda = self.ui.precovenda_prod.setText('')
                sku = self.ui.sku_prod.setText('') 
                ncm = self.ui.ncm_prod.setText('')
                cean = self.ui.cean_prod.setText('')
                cfop = self.ui.cfop_prod.setText('')

            #função condicional nome em branco, o codigo deve estar digitado para ser efetuada a exclusão do banco de dados
            elif nome == '':
                Cursor = banco.cursor()
                sql = f"DELETE  FROM produto WHERE pcodigo = '{codigo}'"
                Cursor.execute(sql)
                banco.commit()
                Cursor.close()

                errorMessage = QtWidgets.QErrorMessage()
                errorMessage.showMessage('Produto removido do sistema.')
                errorMessage.exec_()

                codigo = self.ui.codigo_prod.setText('')
                nome = self.ui.nome_prod.setText('')
                marca = self.ui.marca_prod.setText('')
                estoquea = self.ui.estoque_a.setText('')
                estoquemin = self.ui.estoque_min.setText('')
                estoquemax = self.ui.estoque_max.setText('')
                unidade = self.ui.unidade_prod.setText('')
                precocusto = self.ui.precocusto_prod.setText('')
                precovenda = self.ui.precovenda_prod.setText('')
                sku = self.ui.sku_prod.setText('') 
                ncm = self.ui.ncm_prod.setText('')
                cean = self.ui.cean_prod.setText('')
                cfop = self.ui.cfop_prod.setText('')

    #consulta
    def consulta_prod(self):
        #campos da tela
        codigo = self.ui.codigo_prod.text()
        nome = self.ui.nome_prod.text()
        Cursor = banco.cursor()

        #condição de erro: o nome ou o codigo estarem em branco
        if codigo == '' and nome == '':
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Insira um código ou nome válido para a consulta.')
            errorMessage.exec_()
        
        else:
            #condição para quando o codigo estar em branco efetuar a consulta por nome
            if codigo == '':
                sql = f"SELECT * FROM produto WHERE nome='{nome}'"
                Cursor.execute(sql)
                select = Cursor.fetchall()
                Cursor.close()
            
                if not select:
                    errorMessage = QtWidgets.QErrorMessage()
                    errorMessage.showMessage('Insira um código ou nome válido para a consulta.')
                    errorMessage.exec_()
            
                else:
                    codigo = self.ui.codigo_prod.setText(str(select[0][0]))
                    nome = self.ui.nome_prod.setText(str(select[0][1]))
                    marca = self.ui.marca_prod.setText(str(select[0][2]))
                    estoquea = self.ui.estoque_a.setText(str(select[0][3]))
                    estoquemin = self.ui.estoque_min.setText(str(select[0][4]))
                    estoquemax = self.ui.estoque_max.setText(str(select[0][5]))
                    unidade = self.ui.unidade_prod.setText(str(select[0][6]))
                    precocusto = self.ui.precocusto_prod.setText(str(select[0][7]))
                    precovenda = self.ui.precovenda_prod.setText(str(select[0][8]))
                    sku = self.ui.sku_prod.setText(str(select[0][9]))
                    ncm = self.ui.ncm_prod.setText(str(select[0][10]))
                    cean = self.ui.cean_prod.setText(str(select[0][11]))
                    cfop = self.ui.cfop_prod.setText(str(select[0][12]))

            #condição para quando o nome estar em branco efetuar a consulta por codigo
            else:
                sql = f"SELECT * FROM produto WHERE pcodigo='{codigo}'"
                Cursor.execute(sql)
                select = Cursor.fetchall()
                Cursor.close()

                if not select:
                    errorMessage = QtWidgets.QErrorMessage()
                    errorMessage.showMessage('Insira um código ou nome válido para a consulta.')
                    errorMessage.exec_()
            
                else:
                    nome = self.ui.nome_prod.setText(str(select[0][1]))
                    marca = self.ui.marca_prod.setText(str(select[0][2]))
                    estoquea = self.ui.estoque_a.setText(str(select[0][3]))
                    estoquemin = self.ui.estoque_min.setText(str(select[0][4]))
                    estoquemax = self.ui.estoque_max.setText(str(select[0][5]))
                    unidade = self.ui.unidade_prod.setText(str(select[0][6]))
                    precocusto = self.ui.precocusto_prod.setText(str(select[0][7]))
                    precovenda = self.ui.precovenda_prod.setText(str(select[0][8]))
                    sku = self.ui.sku_prod.setText(str(select[0][9]))
                    ncm = self.ui.ncm_prod.setText(str(select[0][10]))
                    cean = self.ui.cean_prod.setText(str(select[0][11]))
                    cfop = self.ui.cfop_prod.setText(str(select[0][12]))


    #limpar sem excluir da base de dados
    def limpar_prod(self):
        #define os campos limpos somente na tela
        self.ui.codigo_prod.setText('')
        self.ui.nome_prod.setText('')
        self.ui.marca_prod.setText('')
        self.ui.estoque_a.setText('')
        self.ui.estoque_min.setText('')
        self.ui.estoque_max.setText('')
        self.ui.unidade_prod.setText('')
        self.ui.precocusto_prod.setText('')
        self.ui.precovenda_prod.setText('')
        self.ui.sku_prod.setText('') 
        self.ui.ncm_prod.setText('')
        self.ui.cean_prod.setText('')
        self.ui.cfop_prod.setText('')





    def lancarremet(self):
        tipoNF = self.ui.tiponf_remetente.currentText()
        numeroremet = self.ui.numero_remetente.text()
        chaveremet = self.ui.chave_remetente.text()
        serieremet = self.ui.serie_remetente.text()
        razaosocial = self.ui.razao_remetente.text()
        cnpjremet = self.ui.cnpj_remetente.text()
        ufremet = self.ui.uf_remetente.currentText()
        inscestadual = self.ui.insc_estadual_remetente.text()
        inscmunicipal = self.ui.insc_municipal_remetente.text()
        ruaremet = self.ui.rua_remetente.text()
        numeroruaremet = self.ui.numero_remetente_2.text()
        bairroremet = self.ui.bairro_remetente.text()
        complementoremet = self.ui.complemento_remetente.text()
        cepremet = self.ui.cep_remetente.text()
        cidaderemet = self.ui.cidade_remetente.text()
        pagtoremet = self.ui.pagto_prest_servico_remetente.text()
        ufpgto = self.ui.uf_pagamento.currentText()
        Cursor = banco.cursor()
        try:
            inserir = "INSERT INTO remetente VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            valores = (tipoNF, numeroremet, chaveremet, serieremet, razaosocial, cnpjremet, ufremet, inscestadual, inscmunicipal, ruaremet, numeroruaremet, bairroremet, complementoremet, cepremet, cidaderemet, pagtoremet, ufpgto)
            Cursor.execute(inserir,valores)
            banco.commit()
        except:
            return

    # deixar os campos vazios
    def limparremet(self):    
        tipoNF = self.ui.tiponf_remetente.setCurrentText("")
        numeroremet = self.ui.numero_remetente.setText("")
        chaveremet = self.ui.chave_remetente.setText("")
        serieremet = self.ui.serie_remetente.setText("")
        razaosocial = self.ui.razao_remetente.setText("")
        cnpjremet = self.ui.cnpj_remetente.setText("")
        ufremet = self.ui.uf_remetente.setCurrentText("")
        inscestadual = self.ui.insc_estadual_remetente.setText("")
        inscmunicipal = self.ui.insc_municipal_remetente.setText("")
        ruaremet = self.ui.rua_remetente.setText("")
        numeroruaremet = self.ui.numero_remetente_2.setText("")
        bairroremet = self.ui.bairro_remetente.setText("")
        complementoremet = self.ui.complemento_remetente.setText("")
        cepremet = self.ui.cep_remetente.setText("")
        cidaderemet = self.ui.cidaade_remetente.setText("")
        pagtoremet = self.ui.pagto_prest_servico_remetente.setText("")
        ufpgto = self.ui.uf_pagamento.setCurrentText("")

    # adicionar produto a nota fiscal
    def addprodnf(self):
        cod = self.ui.codigo_ins.text()
        cod = int(cod)
        skuins = self.ui.sku_ins.text()
        descins = self.ui.descricao_ins.text()
        unidadeins = self.ui.un_ins.text()
        qtdeins = self.ui.qtde_ins.text()
        qtdeins = int(qtdeins)
        cfopins = self.ui.cfop_ins.text()
        cstins = self.ui.cst_ins.text()
        precounitins = self.ui.preco_ins.text()
        icmsins = self.ui.icms_ins.text()
        totalins = self.ui.total_ins.text()
        ncmins = self.ui.ncm_ins.text()
        numeroremet = self.ui.numero_remetente.text()

        Cursor = banco.cursor()
        try:
            lancamento = ("INSERT INTO produtos_nf(cod_produto, sku,desc_produto,unidade,quantidade,cfop,cst,preco_un,icms,total_prod,ncm, numeronota) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            formatos = (cod, skuins,descins,unidadeins,qtdeins,cfopins,cstins,precounitins,icmsins,totalins,ncmins, numeroremet)
            Cursor.execute(lancamento,formatos)
            self.vetorcodnf.append(cod)
            self.vetorqtdnf.append(qtdeins)
            banco.commit()
        except:
            return

        
    # fazer a consulta no botao de busca nessa tela
    def consultaprodnf(self):
        Cursor = banco.cursor()
        cod = self.ui.codigo_ins.text()
        try:
            selecionar = f"select * from produto where pcodigo = '{cod}'"
            Cursor.execute(selecionar)
            fetch = Cursor.fetchall()
            desc = self.ui.descricao_ins.setText(fetch[0][1])
            sku = self.ui.sku_ins.setText(str(fetch[0][9]))
            un = self.ui.un_ins.setText(fetch[0][6])
            precouni = self.ui.preco_ins.setText(str(fetch[0][8]))
        except:
            return
        

    def tabelanf(self):
        # mostrar tabela da nota fiscal
        Cursor =  banco.cursor()
        selecionar = "SELECT cod_produto, desc_produto, unidade, quantidade, preco_un, cfop, ncm from produtos_nf"
            
        Cursor.execute(selecionar)
            
            
        resultados = Cursor.fetchall()
        # mostrar itens na tabela
        self.ui.insercao_ins.setRowCount(len(resultados))
        self.ui.insercao_ins.setColumnCount(7)      

        for i in range(0,len(resultados)):
            for j in range(0,7):
                self.ui.insercao_ins.setItem(i,j,QtWidgets.QTableWidgetItem(str(resultados[i][j])))

        



    # remover itens que estavam sendo inseridos
    def removerinsercaonf(self):
        Cursor = banco.cursor()
        tabela = self.ui.insercao_ins.currentRow()            
        pegarid = self.ui.insercao_ins.item(tabela, 0).text()
        pegarqtd = self.ui.insercao_ins.item(tabela, 3).text()
        self.ui.insercao_ins.removeRow(tabela)
        excluir = f"DELETE FROM produtos_nf WHERE cod_produto = {pegarid}"
        pegarid  = int(pegarid)
        pegarqtd = int(pegarqtd)
        Cursor.execute(excluir)
        banco.commit()


    # lançar a nota fiscal
    def lancarnf (self):
        Cursor = banco.cursor()

        for i in range(len(self.vetorcodnf)):
            slct1 = f"select pcodigo, estoqueatual from produto where pcodigo = '{self.vetorcodnf[i]}'"
            Cursor.execute(slct1)
            resultados3 = Cursor.fetchall()
            qtd = (str(resultados3[0][1]))
            qtd = int(qtd)
            print(self.vetorqtdnf[i])
            resultados = Cursor.fetchall()
            altaestoque = (f"UPDATE produto SET estoqueatual = '{qtd+(self.vetorqtdnf[i])}' where pcodigo = '{self.vetorcodnf[i]}'")
            Cursor.execute(altaestoque)
            
        banco.commit()
        limpa = "truncate table produtos_nf"
        Cursor.execute(limpa)
        banco.commit()


    
    
        


    # busca no estoque na tela de estoque
    def buscar_estoque(self):
        codigo = self.ui.consulta_estoque.text()
        Cursor = banco.cursor()
        codigo = codigo.upper()
        # realizar parametros da busca
        if codigo == "":
            sql = f"SELECT * FROM produto"

            Cursor.execute(sql)
            select = Cursor.fetchall()

            self.ui.estoque_tab_2.setRowCount(len(select))
            self.ui.estoque_tab_2.setColumnCount(13)

            for i in range(0, len(select)):
                for j in range (0,13):
                    self.ui.estoque_tab_2.setItem(i, j,QTableWidgetItem(str(select[i][j])))


        else:
            sql = f"SELECT * FROM produto WHERE pcodigo = '{codigo}' or nome = '{codigo}'"

            Cursor.execute(sql)
            select = Cursor.fetchall()

            self.ui.estoque_tab_2.setRowCount(len(select))
            self.ui.estoque_tab_2.setColumnCount(13)
            
            for i in range(0, len(select)):
                for j in range (0,13):
                    self.ui.estoque_tab_2.setItem(i, j,QTableWidgetItem(str(select[i][j])))

            self.ui.consulta_estoque.setText('')

        Cursor.close()  


    def remover_estoque(self):
        #Idetifica a linha
        linha = self.ui.estoque_tab_2.currentRow()
        consulta = self.ui.consulta_estoque.setText('')

        if linha >= 0:
            self.ui.estoque_tab_2.removeRow(linha)

        else:
            errorMessage = QtWidgets.QErrorMessage()
            errorMessage.showMessage('Não há nada para remover.')
            errorMessage.exec_()


        def limpar_estoque(self):
            self.ui.consulta_estoque.setText('')
            self.ui.estoque_tab_2.setRowCount(0)




            #Função de lançamento dos dados da nota
    
    def dados_nota(self):
        sub_tributo = self.ui.tributo_dn.text()
        uf_lancamento = self.ui.lancamento_dn.currentText()
        dt_emicao = self.ui.emissao_dn.text()
        modelonf = self.ui.modelo_dn.text()
        dt_entrada = self.ui.entrada_dn.text()
        cod_serv = self.ui.servico_dn.text()
        dt_cadastro = self.ui.cadastro_dn.text()
        tipo_contribuinte = self.ui.contribuinte_dn.currentText()
        Cursor = banco.cursor()
        # inserir campos dos dados da nota
        try:
            busca = "INSERT INTO dados_nota (ie_sub_tributo, uf_lancamento, modelo_nf, cod_servico, data_emissao, dt_entrada, dt_cadastro, tipo_contribuinte) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            valores = (sub_tributo, uf_lancamento, dt_emicao, modelonf, dt_entrada, cod_serv, dt_cadastro, tipo_contribuinte)

            
            Cursor.execute(busca,valores)
            banco.commit()
            Cursor.close()

            sub_tributo = self.ui.tributo_dn.setText('')
            uf_lancamento = self.ui.lancamento_dn.setCurrentText(1)
            dt_emicao = self.ui.emissao_dn.setText('')
            modelonf = self.ui.modelo_dn.setText('')
            dt_entrada = self.ui.entrada_dn.setText('')
            cod_serv = self.ui.servico_dn.setText('')
            dt_cadastro = self.ui.cadastro_dn.setText('')
            tipo_contribuinte = self.ui.contribuinte_dn.setCurrentText(1)
        except:
            return
    # excluir dados da nota
    def excluir_dadosnota(self):
        sub_tributo = self.ui.tributo_dn.text()
        uf_lancamento = self.ui.lancamento_dn.currentText()
        dt_emicao = self.ui.emissao_dn.text()
        modelonf = self.ui.modelo_dn.text()
        dt_entrada = self.ui.entrada_dn.text()
        cod_serv = self.ui.servico_dn.text()
        dt_cadastro = self.ui.cadastro_dn.text()
        tipo_contribuinte = self.ui.contribuinte_dn.currentText()
        Cursor = banco.cursor()
        try:
            busca = f"DELETE FROM dados_nota WHERE = {sub_tributo}"
            valores = (sub_tributo, uf_lancamento, dt_emicao, modelonf, dt_entrada, cod_serv, dt_cadastro, tipo_contribuinte)

            Cursor.execute(busca,valores)
            banco.commit()
            Cursor.close()
        except:
            return

        sub_tributo = self.ui.tributo_dn.setText('')
        uf_lancamento = self.ui.lancamento_dn.setCurrentText(1)
        dt_emicao = self.ui.emissao_dn.setText('')
        modelonf = self.ui.modelo_dn.setText('')
        dt_entrada = self.ui.entrada_dn.setText('')
        cod_serv = self.ui.servico_dn.setText('')
        dt_cadastro = self.ui.cadastro_dn.setText('')
        tipo_contribuinte = self.ui.contribuinte_dn.setCurrentText(1)


    # limpar dados da nota
    def limpa_dadosnt(self):
        sub_tributo = self.ui.tributo_dn.setText('')
        uf_lancamento = self.ui.lancamento_dn.setCurrentText(1)
        dt_emicao = self.ui.emissao_dn.setText('')
        modelonf = self.ui.modelo_dn.setText('')
        dt_entrada = self.ui.entrada_dn.setText('')
        cod_serv = self.ui.servico_dn.setText('')
        cod_serv2 = self.ui.servico_dn_2.setText('')
        dt_cadastro = self.ui.cadastro_dn.setText('')
        tipo_contribuinte = self.ui.contribuinte_dn.setCurrentText(1)

    
    # adicionar na tela de vendas
    def addvendas(self):
        cod_campo = self.ui.cod_campo.text()
        Cursor = banco.cursor()
        try:
            selecionar = f"SELECT nome, precovenda from produto where pcodigo = '{cod_campo}'"
            Cursor.execute(selecionar)
            sql = Cursor.fetchall()

            nome = self.ui.nome_campo.setText(str(sql[0][0]))
            preco = self.ui.valoruni_campo.setText(str(sql[0][1]))

        except:
            return




    # subtotal nos valores
    def subtotal(self):
        quantidade = self.ui.quantidade_campo.text()
        valorunit = self.ui.valoruni_campo.text()
        try:
            subtotal = float(quantidade)*float(valorunit)
            subtotal1 = self.ui.subtotal_campo.setText(str(subtotal))
        except:
            return



    # função de desconto 
    def desconto(self):
        numero = self.ui.desconto_campo.text()
        numero = numero[0: -1]
        subtotal = self.ui.subtotal_campo.text()
        try:
            desconto = -float(subtotal)*(int(numero*1)/100)+float(subtotal)
            subtotal1 = self.ui.subtotal_campo.setText(str(desconto))
        except:
            return
    
    # função de zerar 
    def zerar(self):
        if self.ui.desconto_campo.text() == "":
            quantidade = self.ui.quantidade_campo.text()
            valorunit = self.ui.valoruni_campo.text()
            try:
                subtotal = float(quantidade)*float(valorunit)
                subtotal1 = self.ui.subtotal_campo.setText(str(subtotal))
            except:
                return
    # função de adicionar na tabela de carrinho
    def adicionarcarrinho(self):
        codigo = self.ui.cod_campo.text()
        codigo = int(codigo)
        nome = self.ui.nome_campo.text()
        quantidade = self.ui.quantidade_campo.text()
        quantidade = int(quantidade)
        valorunit = self.ui.valoruni_campo.text()
        subtotal = self.ui.subtotal_campo.text()
        Cursor = banco.cursor()
        inserir = "INSERT INTO carrinho VALUES(%s,%s,%s,%s,%s)"     
        self.vetor1.append(codigo)
        self.vetor2.append(quantidade) 
        valores = (codigo,nome,quantidade,valorunit,subtotal)        
        Cursor.execute(inserir,valores)
        banco.commit()       
        
        Cursor = banco.cursor()

        selecionar = "SELECT * from carrinho"

        Cursor.execute(selecionar)

        resultados = Cursor.fetchall()




        self.ui.cupom.setRowCount(len(resultados))
        self.ui.cupom.setColumnCount(5)      

        for i in range(0,len(resultados)):
            for j in range(0,5):
                self.ui.cupom.setItem(i,j,QtWidgets.QTableWidgetItem(str(resultados[i][j])))
        
    
    # remover da tabela de carrinho e pro usuario também
    def removercarrinho(self):
        Cursor = banco.cursor()
        tabela = self.ui.cupom.currentRow()            
        pegarid = self.ui.cupom.item(tabela, 0).text()
        pegarqtd = self.ui.cupom.item(tabela, 2).text()

        self.ui.cupom.removeRow(tabela)
        excluir = f"DELETE FROM carrinho WHERE cod = {pegarid}"
        pegarid  = int(pegarid)
        pegarqtd = int(pegarqtd)
        self.vetor1.remove(pegarid)
        self.vetor2.remove(pegarqtd)


        print(self.vetor2,self.vetor1)
        Cursor.execute(excluir)
        banco.commit()

    # somar o total de valores
    def somartotal(self):
        Cursor = banco.cursor()
        selecionar = "select round(sum(valor),2) as total from carrinho"
        Cursor.execute(selecionar)
        resultados = Cursor.fetchall()
        total = self.ui.total_campo.setText(str(resultados[0][0]))
        if self.ui.total_campo.text() == "None":
            total = self.ui.total_campo.setText("")

    # finalizar a compra 
    def finalizarcompra(self):

        Cursor = banco.cursor()
        slct = f"select * from carrinho"
        Cursor.execute(slct)
        resultados = Cursor.fetchall()

        for i in range(len(resultados)):
            slct1 = f"select pcodigo, estoqueatual from produto where pcodigo = '{self.vetor1[i]}'"
            Cursor.execute(slct1)
            resultados3 = Cursor.fetchall()
            qtd = (str(resultados3[0][1]))
            qtd = int(qtd)
            print(self.vetor2[i])
            resultados = Cursor.fetchall()
            baixaestoque = (f"UPDATE produto SET estoqueatual = '{qtd-(self.vetor2[i])}' where pcodigo = '{self.vetor1[i]}'")
            Cursor.execute(baixaestoque)
            banco.commit()
            limpa = "truncate table carrinho"
            Cursor.execute(limpa)
            banco.commit()
        msg = QMessageBox()
        msg.setText("COMPRA FINALIZADA COM SUCESSO!")
        msg.setWindowTitle("SENALAR")
        msg.setWindowIcon(QtGui.QIcon("Logo sem circulo.png"))
        msg.setStyleSheet("color: rgb(0, 0, 0);")
        msg.exec_() 

    
    # cancelar compra caso o usuario queira
    def cancelarcompra(self):
        Cursor = banco.cursor()
        codigo = self.ui.cod_campo.setText('')
        nome = self.ui.nome_campo.setText('')
        quantidade = self.ui.quantidade_campo.setText('')
        valorunit = self.ui.valoruni_campo.setText('')
        subtotal = self.ui.subtotal_campo.setText('')
        desconto = self.ui.desconto_campo.setText('')
        total = self.ui.total_campo.setText('')
        limpa = "truncate table carrinho"
        Cursor.execute(limpa)
        banco.commit()
        
        selecionar = "SELECT * from carrinho"
        self.vetor1.clear()
        self.vetor2.clear()
        Cursor.execute(selecionar)

        resultados = Cursor.fetchall()

        self.ui.cupom.setRowCount(len(resultados))
        self.ui.cupom.setColumnCount(5)      

        for i in range(0,len(resultados)):
            for j in range(0,5):
                self.ui.cupom.setItem(i,j,QtWidgets.QTableWidgetItem(str(resultados[i][j])))

    #criar o metodo da tela de login
class login(QMainWindow):
    def __init__(self,*args,**argvs):
        super(login,self).__init__(*args,**argvs)
        self.ui = Ui_login()
        self.ui.setupUi(self)
        self.ui.bt_vsenha.clicked.connect(self.mostrar_senha)
        self.ui.bt_login.clicked.connect(self.entrar)


    # função para o botao de mostrar tela
    def mostrar_senha(self):
        if self.ui.senha.echoMode()==QLineEdit.Normal:
            self.ui.senha.setEchoMode(QLineEdit.Password)
        else:
            self.ui.senha.setEchoMode(QLineEdit.Normal)

    # funcao de entrar na tela principal
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