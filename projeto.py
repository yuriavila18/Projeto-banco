from registros import Usuario
import datetime
import os
import re
import shutil

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if not cpf.isdigit() or len(cpf) != 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito_verificador_1 = 0 if resto == 10 else resto

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito_verificador_2 = 0 if resto == 10 else resto

    return cpf[-2:] == f"{digito_verificador_1}{digito_verificador_2}"

def validar_telefone(telefone):
    telefone = re.sub(r'\D', '', telefone)
    return telefone.isdigit() and (len(telefone) == 10 or len(telefone) == 11)

def criar_diretorio_usuario(username):
    diretorio_usuario = os.path.join("dados_usuarios", username)
    os.makedirs(diretorio_usuario, exist_ok=True)
    return diretorio_usuario

def cadastrar_usuario(username, password, nome, cpf, telefone):
    diretorio_usuario = os.path.join("dados_usuarios", username)

    if os.path.exists(diretorio_usuario):
        print("Usuário já existe. Por favor, escolha outro nome de usuário.")
        return

    if not validar_cpf(cpf):
        print("CPF inválido. Por favor, insira um CPF válido.")
        return

    if not validar_telefone(telefone):
        print("Número de telefone inválido. Por favor, insira um telefone válido.")
        return

    usuario = Usuario(username, password, nome, cpf, telefone)
    diretorio_usuario = criar_diretorio_usuario(username)

    informacao_usuario = os.path.join(diretorio_usuario, "info.txt")
    saldo = 0.00

    with open(informacao_usuario, "w") as arquivo:
        arquivo.write(f"{usuario.username}:{usuario.password}:{usuario.nome}:{usuario.cpf}:{usuario.telefone}:{saldo}\n")

    operacao_usuario = os.path.join(diretorio_usuario, f"operacoes_{username}.txt")
    with open(operacao_usuario, "w") as arquivo_operacoes:
        pass

    print("Usuário cadastrado com sucesso!")

def excluir_usuario(username):
    diretorio_usuario = os.path.join("dados_usuarios", username)
    info_usuario = os.path.join(diretorio_usuario, "info.txt")
    
    # Remover o diretório do usuário
    if os.path.exists(diretorio_usuario):
        shutil.rmtree(diretorio_usuario)
        print(f"Usuário {username} excluído com sucesso!")
    
    # Remover o registro do usuário
        if os.path.exists(info_usuario):
            with open(info_usuario, "r") as arquivo:
                linhas = arquivo.readlines()
        else:
            print(f"Arquivo {info_usuario} não encontrado.")
        
        return False, None, None, None, None, None, None, None
    

    for i, linha in enumerate(linhas):
        data = linha.strip().split(":")
        if len(data) >= 6 and data[0] == username:
            del linhas[i]
            break

    with open(info_usuario, "w") as arquivo:
        arquivo.writelines(linhas)
    
    shutil.rmtree(diretorio_usuario)

def alterar_senha(username, info_usuario):
    with open(info_usuario, "r") as arquivo:
        linhas = arquivo.readlines()

    for i, linha in enumerate(linhas):
        data = linha.strip().split(":")
        if len(data) >= 6 and data[0] == username:
            senha_atual = input("Digite a senha atual: ")
            if senha_atual == data[1]:
                nova_senha = input("Digite a nova senha: ")
                linhas[i] = f"{data[0]}:{nova_senha}:{data[2]}:{data[3]}:{data[4]}:{data[5]}\n"
                print("Senha alterada com sucesso!")
            else:
                print("Senha atual incorreta.")
            break
    else:
        print("Usuário não encontrado.")

    with open(info_usuario, "w") as arquivo:
        arquivo.writelines(linhas)
    

def fazer_login(username, password):
    diretorio_usuario = os.path.join ("dados_usuarios", username)
    info_usuario = os.path.join(diretorio_usuario, "info.txt")
    operacao_usuario = os.path.join(diretorio_usuario, f"operacoes_{username}.txt")
        
    if os.path.exists(info_usuario): 
        with open(info_usuario, "r") as arquivo:
            linhas = arquivo.readlines()

        extrato = []
        
        if os.path.exists(operacao_usuario):
            with open(operacao_usuario, "r") as arquivo_operacoes:
                extrato = arquivo_operacoes.readlines()
            
            # Verifica se o arquivo está vazio
            if not extrato:
                print("Não há extrato.")
        
        else:
            print("Não há histórico de movimentação.")

        
        for linha in linhas:
            data = linha.strip().split(":")
        
            if len(data) >= 6:
                user, pwd, nome, cpf, telefone, saldo = data[:6]
            
                if user == username and pwd == password:
                    print("Login bem-sucedido!")
                    return True, username, float(saldo), info_usuario, nome, cpf, telefone, extrato

    print("Nome de usuário ou senha incorretos.")
    return False, None, None, None, None, None, None, None

def operacoes(username, saldo, valor, extrato, info_usuario, tipo_operacao):
    diretorio_usuario = os.path.join("dados_usuarios", username)
    operacao_usuario = os.path.join(diretorio_usuario, f"operacoes_{username}.txt")

    # Registrar operação no extrato
    operacao = f"{datetime.datetime.now()} - {tipo_operacao} - Valor: R${valor:.2f}\n"
    extrato.append(operacao)

    with open(operacao_usuario, "a") as arquivo:
        arquivo.write(operacao)
    
    with open(info_usuario, "r") as arquivo:
        linhas = arquivo.readlines()

    for i, linha in enumerate(linhas):
        data = linha.strip().split(":")
        if len(data) >= 6 and data[0] == username:
            linhas[i] = f"{data[0]}:{data[1]}:{data[2]}:{data[3]}:{data[4]}:{saldo}\n"

    with open(info_usuario, "w") as arquivo:
        arquivo.writelines(linhas)

def alterar_dados_usuario(username, info_usuario):
    with open(info_usuario, "r") as arquivo:
        linhas = arquivo.readlines()

    for i, linha in enumerate(linhas):
        data = linha.strip().split(":")
        if len(data) >= 6 and data[0] == username:
            print("Dados atuais do usuário:")
            print(f"1. Nome Completo: {data[2]}")
            print(f"2. CPF: {data[3]}")
            print(f"3. Número de Telefone: {data[4]}")

            opcao = input("Escolha o número do dado que deseja alterar (ou 0 para sair): ")

            if opcao == '1':
                novo_nome = input("Novo Nome Completo: ")
                linhas[i] = f"{data[0]}:{data[1]}:{novo_nome}:{data[3]}:{data[4]}:{data[5]}\n"

            elif opcao == '2':
                novo_cpf = input("Novo CPF: ")
                linhas[i] = f"{data[0]}:{data[1]}:{data[2]}:{novo_cpf}:{data[4]}:{data[5]}\n"

            elif opcao == '3':
                novo_telefone = input("Novo Número de Telefone: ")
                linhas[i] = f"{data[0]}:{data[1]}:{data[2]}:{data[3]}:{novo_telefone}:{data[5]}\n"

            elif opcao == '0':
                return

            else:
                print("Opção inválida.")

    with open(info_usuario, "w") as arquivo:
        arquivo.writelines(linhas)

    print("Dados atualizados com sucesso!")

def exibir_extrato(diretorio_usuario, username):
    caminho_info = os.path.join(diretorio_usuario, username, f"operacoes_{username}.txt")
    if os.path.exists(caminho_info):
    # Abrir e ler o arquivo info.txt
        with open(caminho_info, "r") as arquivo:
            conteudo = arquivo.read()
            print(conteudo) 
    else:
        print(f"O arquivo {caminho_info} não foi encontrado.")

def menu():
    print("1. Cadastrar Usuário")
    print("2. Fazer Login")
    print("3. Sair")

def exibir_menu():
    print("1. Depósito")
    print("2. Saque")
    print("3. Consultar Saldo")
    print("4. Extrato")
    print("5. Dados usuário")
    print("6. Sair")

def exibir_dados_usuario(username, nome, cpf, telefone):
    print("Dados do Usuário:")
    print(f"Nome de Usuário: {username}")
    print(f"Nome Completo: {nome}")
    print(f"CPF: {cpf}")
    print(f"Número de Telefone: {telefone}")

def main():
    bem_vindo = False
    username = ""
    nome = ""
    cpf = ""
    telefone = ""
    saldo = 0.00
    extrato = []

    while True:
        print("Bem-vindo ao Sistema Bancário!")
        menu()
        escolha_registro = input("Escolha uma opção: ")

        if escolha_registro == '1':
            username = input("Digite o nome de usuário: ")
            password = input("Digite a senha: ")
            nome = input("Nome completo: ")
            cpf = input("Digite o CPF: ")
            telefone = input("Digite o número de telefone: ")
            info_usuario = cadastrar_usuario(username, password, nome, cpf, telefone)

        elif escolha_registro == '2':
            username = input("Digite o nome de usuário: ")
            password = input("Digite a senha: ")
            login_efetuado, username, saldo, info_usuario, nome, cpf, telefone, extra = fazer_login(username, password)

            while login_efetuado:
                if not bem_vindo:
                    print(f"Bem-vindo ao Sistema Bancário, {username}!")
                    bem_vindo = True

                exibir_menu()

                escolha = input('Escolha a opção:')

                # Depósito
                if escolha == '1':  
                    valor = float(input('Valor do depósito:'))
                    saldo += valor 
                    operacoes(username, saldo, valor, extrato, info_usuario, "Depósito")
                # Saque
                elif escolha == '2':  
                    valor = float(input("Valor do saque:"))
                    if saldo >= valor:
                        saldo -= valor 
                        operacoes(username, saldo, valor, extrato, info_usuario, "Saque")
                        print(f"Saque de R${valor:.2f} realizado com sucesso!")
                    else:
                        print('Saldo insuficiente.')
                # Saldo
                elif escolha == '3':  
                    print(f'Saldo atual: R$ {saldo:.2f}')
                # Extrato
                elif escolha == '4':  
                    exibir_extrato("dados_usuarios", username)

                # Dados
                elif escolha == '5': 
                    exibir_dados_usuario(username, nome, cpf, telefone)
                    opcao_dados = input("Escolha a opção:\n1. Alterar Dados\n2. Alterar senha\n3. Voltar\n4. Excluir usuário\nEscolha a opção:")
                    
                    # Alterar dados do usuário
                    if opcao_dados == '1': 
                        alterar_dados_usuario(username, info_usuario)
                    
                    # Alterar senha do usuário
                    elif opcao_dados == '2': 
                        alterar_senha(username, info_usuario)

                    # Voltar
                    elif opcao_dados == '3': 
                        continue

                    # Excluir usuário
                    elif opcao_dados == '4': 
                        confirmacao = input(f"Tem certeza que deseja excluir o usuário {username}? (S/N): ")
                        if confirmacao.lower() == 's': 
                            excluir_usuario(username)
                            break
                        elif confirmacao.lower() == 'n':
                            continue
                # Sair
                elif escolha == '6':  
                    print(f"Obrigado, {username}, por utilizar o sistema bancário. Até mais!")
                    break

                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")

        elif escolha_registro == '3':
            print('Obrigado por acessar o nosso banco!')
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
