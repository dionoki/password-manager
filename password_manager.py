#Início primeiro projeto ( Sistema de gerenciamento de senhas com hash )
import json
import hashlib
from cryptography.fernet import Fernet
import customtkinter as ctk


# Função principal do codigo ------------------------------------------------------------------------------------------------------------------------------------------------
class GerenciadorSenhas:
    def __init__(self):
        self.senha_mestre = None
        self.dados = {}
        self.f = None
        self.init_sistema()

    def salvar_dados(self):
        geral = {
            "senha_mestre": self.senha_mestre,
            "dados": self.dados
        }
        with open('arquivo.json', 'w', encoding='utf-8') as arquivo:
            json.dump(geral, arquivo, indent=4)

    def mostrar_servicos(self):
        print('Serviços Disponíveis:')
        for servico in self.dados:
            print('- ' + servico)

    def pedir_servico(self):
        servico = input("Selecione um serviço: ").strip().lower()
        return servico

    def autenticar(self, senhasalva):
        hash_digitado = hashlib.sha256(senhasalva.encode()).hexdigest()
        if hash_digitado == self.senha_mestre:
            return True
        else:
            return False

    def mostrar_dados(self, servico):
        print('Serviço encontrado!')
        login_salvo = self.dados[servico]['login'].encode()
        login_real = self.f.decrypt(login_salvo).decode()
        # Ambas linhas de código servem pra descriptografar oq está dentro do json afim de mostrar a senha depois da autorização por senha estar correta
        senha_salva = self.dados[servico]['senha'].encode()
        senha_real = self.f.decrypt(senha_salva).decode()

        print("login:", login_real)
        print("senha:", senha_real)

    def init_sistema(self):
        try:
            self.senha_mestre, self.dados = self.carregar_dados()
            with open('Chave.key', 'rb') as arquivo_da_chave:
                chave_lida = arquivo_da_chave.read()
                self.f = Fernet(chave_lida)

        except:
            pass
            
    def carregar_dados(self):
        with open("arquivo.json", "r", encoding='utf-8') as arquivo:
            geral = json.load(arquivo)
            return geral["senha_mestre"], geral['dados']
   



# Sistema principal ---------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    gm = GerenciadorSenhas()

    while True:
        print('1 - Adicione um novo login \n2 - Mostrar senhas salvas\n3 - Sair')
        comando = input('Selecione uma opção: ')

        if comando == '1':
            print('Que tipo de conta você está adicionando?')
            conta = input('- Google \n- Microsoft \n- Streaming\n- Outros \n')

            login = input('Digite seu novo login:')
            login_trancado = login.encode('utf-8')

            log_trancado = gm.f.encrypt(login_trancado)
            senha = input('Digite sua nova senha:')
            cript = senha.encode('utf-8')  # Codifica pra bytes

            senha_trancada = gm.f.encrypt(cript)  # Criptografa a senha
            gm.dados[conta] = {"login": log_trancado.decode(), "senha": senha_trancada.decode()}
            gm.salvar_dados()
            print('Login salvo com sucesso!')

        elif comando == '2':
            gm.mostrar_servicos()
            servico = gm.pedir_servico()

            if servico in gm.dados:
                senha_inserida = input('Digite a senha: ')
                if gm.autenticar(senha_inserida):
                    gm.mostrar_dados(servico)
                else:
                    print('Acesso negado')

            else:
                print('Serviço não encontrado!')

        elif comando == '3':
            print('Até logo!')
            break          
        
    


   




