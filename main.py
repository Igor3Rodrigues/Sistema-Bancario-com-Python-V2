import textwrap

class ContaBancaria:
    def deposito(self, saldo, valor, extrato):
        if valor > 0:
            saldo += valor
            extrato += f"Depósito de R${valor:.2f} realizado com sucesso. Saldo atual: R${saldo:.2f}\n"
            return saldo, extrato
        else:
            return saldo, "Valor do depósito deve ser positivo."

    def saque(self, *, saldo, valor, extrato, limite=500, numero_saques=0, limite_saques=3):
        if valor > saldo:
            return "Saldo insuficiente.", saldo, extrato
        elif valor > limite:
            return "Valor do saque excede o limite permitido.", saldo, extrato
        elif numero_saques >= limite_saques:
            return "Limite diário de saques atingido.", saldo, extrato
        else:
            saldo -= valor
            extrato += f"Saque de R${valor:.2f} realizado com sucesso. Saldo atual: R${saldo:.2f}\n"
            numero_saques += 1
            return "Saque realizado com sucesso.", saldo, extrato
        

    def extrato(self, cliente, saldo):
        print("\n================ EXTRATO ================")
        extrato = f"Extrato bancário de {cliente}:\n"
        extrato += f"\nSaldo:\t\tR$ {saldo:.2f}\n"
        return extrato
        


def menu():
    menu_text = """
    Bem-vindo ao Sistema Bancário!
    
    1. Depositar
    2. Sacar
    3. Extrato
    4. Novo usuário
    5. Nova conta
    6. Listar contas
    7. Sair
    
    Selecione uma opção: 
    """

    return input(textwrap.dedent(menu_text))


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            conta_bancaria = ContaBancaria()  # Criar uma instância da classe ContaBancaria
            saldo, extrato = conta_bancaria.deposito(saldo, valor, extrato)  # Realizar o depósito
            print(f"Depósito de R${valor:.2f} realizado com sucesso. Saldo atual: R${saldo:.2f}")

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            conta_bancaria = ContaBancaria()  # Criar uma instância da classe ContaBancaria
            mensagem, saldo, extrato = conta_bancaria.saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

            print(mensagem)  # Exibir mensagem de sucesso ou erro

        elif opcao == "3":
            cliente = input("Digite o nome do cliente para exibir o extrato: ")
            extrato = conta_bancaria.extrato(cliente, saldo)
            print(extrato)
            
        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
