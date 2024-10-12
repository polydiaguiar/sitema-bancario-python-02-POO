from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    #"""representa um cliente do banco"""
    def __init__(self, endereco):
        #"""
        # Construtor da classe Cliente
        #   Args: 
        #       endereco(str): endereco do cliente
        #   Atributos:
        #       endereco(str): endereco do cliente
        #       contas (lis): lista de contas associadas ao cliente
        # """
        self.endereco = endereco
        self.contas=[]
        
    def realizar_transacao(self, conta, transacao):
        #"""
        # Realiza uma transação e registra em uma das contas do #cliente
        # Args:
        #       conta(Conta): conta na qual a transação será realizada. 
        #       transação(Transacao): objeto que representa a transação
        # """
        transacao.registrar(conta)
    
    def adicionar_conta(self,conta):
      # """ 
      # Adiciona uma nova conta à lista de contas do cliente.
      # Args:
      #      conta (Conta): Conta a ser adicionada.
      # """
        self.contas.append(conta)

class PessoaFisica(Cliente):
    #"""
    # Representa uma pessoa física que é cliente do banco, herda da classe Cliente
    # """
    def __init__(self, nome, data_nascimento, cpf, endereco):
    #"""Construtor da classe PessoaFisica.
    # Args:
    #    nome (str): Nome completo da pessoa física.
    #    data_nascimento (str): Data de nascimento da pessoa física..
    #    cpf (str): Número de CPF da pessoa física.
    #    endereco (str): Endereço da pessoa física.

    #Herda de:
    #    Cliente: Classe base que representa um cliente genérico.

    #Atributos:
    #    nome (str): Nome completo da pessoa física.
    #    data_nascimento (str): Data de nascimento da pessoa física.
    #    cpf (str): Número de CPF da pessoa física.
    #    endereco (str): Endereço da pessoa física (herdado da classe base).
    #"""
        super().__init__(endereco)
        self.nome=nome
        self.data_nascimento=data_nascimento
        self.cpf=cpf

class Conta():
    #""""""
    def __init__(self, numero, cliente):
        self._saldo= 0
        self._numero= numero
        self._agencia= "0001"
        self._cliente= cliente
        self._historico= Historico()
    
    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self.cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
    #""" define função sacar (keyword only), """
        saldo = self.saldo
        excedeu_saldo = valor > saldo 
        
        if excedeu_saldo: 
            print("\nOperação não concluída!. Você não tem saldo suficiente.")
        
        elif valor>0:            
            self._saldo -= valor 
            print("Operação concluída com sucesso. Retire o dinheiro na boca do caixa eletrônico.")   
            return True
                
        else:
            print("Operação não concluída!. Valor solicitado inválido.")
    
        return False

    def depositar(self, valor):
        """Cria função depositar(position only) que valida valor de depósito""" 
        if valor >0:      
            self._saldo += valor 
            print("Operação concluída com sucesso!")
        else:
            print("Valor inválido. Operação não concluída")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, *args, limite=500, limite_saque=3):
        super().__init__(*args)
        self.limite = limite 
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.trasacoes if trasacao["tipo"]== Saque.__name__]
        )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n Operação não concluída! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\n Operação não concluída! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False
        
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
    
    """

class Historico:
 
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
            
    def adicionar_transacao(self, trasacao):
        self.transacoes.append(
            {
                "tipo": trasacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M%s")    
                
                
            }         
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):    
        pass

class Sacar(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu(): 
    """atribue variável menu como retorno da função"""
    menu = """
Escolha umas das opções do menu a seguir: 

========= Menu =========

[0] Depositar
[1] Sacar
[2] Extrato
[3] Cadastrar Novo Cliente
[4] Criar Conta Corrente 
[5] Sair 

=========================

=> """
    return input(menu)


def gramatica_real(valor):
    """retorna plural da palavra real"""
    if valor == 1:
        return (" real.")
    else:
        return(" reais.")

def verificar_existencia_cliente( cpf, clientes): 
    verificar_existencia_cliente = [cliente for cliente in clientes if cliente["cpf"]==cpf]
    
    return verificar_existencia_cliente[0] if verificar_existencia_cliente else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Depositar(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = verificar_existencia_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado! ")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Sacar(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = verificar_existencia_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def cadastar_novo_cliente(clientes):
    
    cpf = input("Digite o cpf (apenas número): ")
    cliente_verificado = verificar_existencia_cliente(cpf, clientes)
    
    if cliente_verificado:
        print("Cliente já cadastrado!")
        
        return
    
    
    nome = input("Informe nome completo: ")
    data_nascimento = input("Informe data de nascimento(dd/mm/aaaa): ")
    endereco = input("Informe endereço ('logradouro, n. - bairro - cidade/sigla estado'): ")

    cliente = PessoaFisica(cpf= cpf,data_nascimento=data_nascimento, nome=nome,endereco=endereco)

    clientes.append(cliente)
    
    print("\nCadastro realizado com sucesso!")


def criar_conta_corrente(contas, clientes, numero_conta):
    cpf = input("Digite o cpf (apenas número): ")
    cliente = verificar_existencia_cliente(cpf, clientes)

    if not cliente:
        print("Usuário não encontrado, não foi possível concluir abertura de conta")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print(f"""Conta corrente criada com sucesso!
        \n
    === Dados da conta ===
        ID Cliente: {cpf}  
        Agência: {AGENCIA}
        cc: {numero_conta}
                    """)
    return {"gencia":AGENCIA, "numero_conta":numero_conta, "usuario":cpf}


def main():
    clientes =[]
    contas = []

    while True:
        opcao = int(menu())  

        if opcao == 0: 
            Depositar(clientes)     

        elif opcao == 1:  
            Sacar(clientes)

        elif opcao == 2:
            exibir_extrato(clientes)

        elif opcao == 3:
            cadastar_novo_usuario(clientes)
            
        elif opcao == 4:
            numero_conta= len(contas)+1
            criar_conta_corrente(numero_conta, clientes, contas)

            if novo_cadastro_cc:
                contas.append(novo_cadastro_cc)            

        elif opcao == 5 :
            break

        else:
            print("\nOperação inválida, por favor selecionar novamente a operação desejada.\n=> ")

main()

