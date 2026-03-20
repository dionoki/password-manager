#Início primeiro projeto ( Sistema de gerenciamento de senhas com hash )
import json
import hashlib
from cryptography.fernet import Fernet

#Dados, arquivos ---------------------------------------------------------------------------------------------------------------------------------------------------------

def salvar_dados():
  geral = {
     "senha_mestre": senha_mestre,
     "dados": dados
    }
  with open('arquivo.json', 'w', encoding='utf-8') as arquivo:
   json.dump(geral, arquivo, indent=4)      

def carregar_dados():
    with open("arquivo.json", "r") as arquivo:
      geral = json.load(arquivo)
      return geral["senha_mestre"], geral['dados']
 

#Dicionário -----------------------------------------------------------------------------------------------------------------------------------------------------------------

try: 
  senha_mestre, dados = carregar_dados()
  
  with open('Chave.key', 'rb') as arquivo_da_chave:
     chave_lida = arquivo_da_chave.read()# < ----- SALVA OQ LEU AQUI

     f= Fernet(chave_lida)
except:
    print("===============Bem-Vindo ao KeyNoki!===============")
    senhapadrao = input('Crie agora sua senha e faça bom proveito de nosso sistema: ')
    cripto256 = hashlib.sha256(senhapadrao.encode())
    senha_mestre = cripto256.hexdigest()
    dados = {}
    salvar_dados()

    chave = Fernet.generate_key() 
    with open('Chave.key', "wb") as arquivo_da_chave:
     arquivo_da_chave.write(chave)
    f = Fernet(chave)

 # Função principal do codigo ------------------------------------------------------------------------------------------------------------------------------------------------

def mostrar_servicos(senhas):
    print('Serviços Disponíveis:')
    for servico in senhas:
     print('- ' + servico)

def pedir_servico():
   servico = input("Selecione um serviço: ").strip().lower()
   return servico

def autenticar():
   senha = input('Digite a senha: ').strip()
   criarsenha = hashlib.sha256(senha.encode())
   senhasalva = criarsenha.hexdigest()
   return senhasalva == senha_mestre
 
def mostrar_dados(servico, dados):
   print('Serviço encontrado!')
   login_salvo = dados[servico]['login'].encode()
   login_real = f.decrypt(login_salvo).decode()
                                                               #ambas linhas de código servem pra descriptografar oq está dentro do json afim de mostrar a senha depois da autorização por senha estar correta
   senha_salva = dados[servico]['senha'].encode()
   senha_real = f.decrypt(senha_salva).decode()

   print("login:", login_real)
   print("senha:", senha_real)


# Sistema principal ---------------------------------------------------------------------------------------------------------------------------------------------------------
while True:
 print ('1 - Adicione um novo login \n2 - Mostrar senhas salvas\n3 - Sair')
 comando = input('Selecione uma opção:')   
    
 if comando == ('1'):
    print ('Que tipo de conta você está adicionando?')
    conta = input ('- Google \n- Microsoft \n- Streaming\n- Outros \n ')

    login = input('Digite seu novo login:')
    login_trancado = login.encode('utf-8')
    log_trancado = f.encrypt(login_trancado)
    senha = input('Digite sua nova senha:')
    cript = senha.encode('utf-8') # Codifica pra bytes
    senha_trancada = f.encrypt(cript) #ele pega os bytes do encode, mastiga e cospe aquela sopa de letras inteira que está agora gravada no json
    dados[conta] = {"login": log_trancado.decode(), "senha": senha_trancada.decode() }  #o .decode serve pra decodificar a sopa de letras pro json nao surtar 
    salvar_dados()
    print ('Login salvo com sucesso!')
       
 elif comando == ('2'):
    mostrar_servicos(dados)
    servico = pedir_servico()
    
    if servico in dados:
       if autenticar():
         mostrar_dados(servico, dados)
       else:
         print('Acesso negado')

    else:
     print('Serviço não encontrado!')
 
 
 elif comando == ('3'):
        print ('Até logo!')
        break          
        
    


   




