#Início primeiro projeto ( Sistema de gerenciamento de senhas com hash )
import json
import hashlib
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
except:
    print("===============Bem-Vindo ao Keynoki!===============")
    senhapadrao = input('Crie agora sua senha e faça bom proveito de nosso sistema: ')
    cripto256 = hashlib.sha256(senhapadrao.encode())
    senha_mestre = cripto256.hexdigest()
    dados = {}
    salvar_dados()

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
   print("login:", dados[servico]['login'])
   print("senha:", dados[servico]['senha'])
     
# Sistema principal ---------------------------------------------------------------------------------------------------------------------------------------------------------
while True:
 print ('1 - Adicione um novo login \n2 - Mostrar senhas salvas\n3 - Sair')
 comando = input('Selecione uma opção:')   
    
 if comando == ('1'):
    print ('Que tipo de conta você está adicionando?')
    conta = input ('- Google \n- Microsoft \n- Streaming\n- Outros \n ')

    login = input('Digite seu novo login:')
    senha = input('Digite sua nova senha:')
     
    dados[conta] = {"login": login, "senha": senha }
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
        
    


   




