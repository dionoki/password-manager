#Início primeiro projeto ( Sistema de gerenciamento de senhas com hash )


#Dicionário 
senha_mestre = "1109"
senhasdousuario = { 
 
  
'gmail': { 
    'login': 'kelvin@gmail.com', # type: ignore
    'senha': '32'
   },

    
'netflix': { 
    'login': 'usuario.netflix',
    'senha': '123456789'
    }

}



#estrutura de interação com usuário 


print('Serviços Disponiveis: ')
for servico1 in senhasdousuario:
      print('- ' + servico1)
while True:    
          servico = input("Selecione um serviço:" ).strip().lower() 
                #.strip().lower() serve para o python ler a formatação igualmente mesmo se digitarmos em maiusculo ou minusculo
                
          if servico in senhasdousuario: 
                 senha = input('Digite a senha:').strip()
                 if senha == senha_mestre:
                                                            
                      print('Serviço encontrado!') 
                      print("login:", senhasdousuario[servico]['login'])
                      print("senha:", senhasdousuario[servico]['senha'])
                     
                      break              
                 else : 
                      print('Acesso negado')
                      
                     
          else : 
                  print('Serviço não encontrado!')



