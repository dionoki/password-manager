import json
import hashlib
import customtkinter as ctk
from gerenciador_de_senhas import GerenciadorSenhas

#Funções de autenticação e login -------------------------------------------------------------------------------------------------------------------------------

gm = GerenciadorSenhas()


def validar_login(entrada_senha, label_mensagem):

    gm.init_sistema() 

    senha = entrada_senha.get().strip()
 
    if not senha:
        label_mensagem.configure(text='Por favor, insira uma senha.')
        label_mensagem.pack(pady=(0, 10))
        return 
   
    if gm.senha_mestre is None:
        cripto256 = hashlib.sha256(senha.encode())
        gm.senha_mestre = cripto256.hexdigest()
        gm.dados = {}
        
        label_mensagem.configure(text='Senha criada com sucesso! Agora você pode logar')    
        label_mensagem.pack(pady=(0, 10))    
        gm.salvar_dados()
        
        ctk.CTkLabel(janela, text='Senha criada com sucesso! Agora você pode logar', font=('helvetica', 12, 'bold'), text_color='White').pack(pady=(0, 10))
    
    elif gm.autenticar(senha):
        entrada_senha.configure(border_color="Green")
        label_mensagem.configure(text='Login bem-sucedido!', text_color='white')
        label_mensagem.pack(pady=(0, 10))
        janela.destroy()
        menu = menu_inicial()
        menu.mainloop()
        ''
    else:
        entrada_senha.configure(border_color="red")
        label_mensagem.configure(text='Senha incorreta, tente novamente!', text_color='white')
        label_mensagem.pack(pady=(0, 10))
        entrada_senha.delete(0, ctk.END)

#JANELA ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class tela_login(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title('KeyNoki')
        self.geometry('800x600')

        ctk.set_appearance_mode('black')
        ctk.set_default_color_theme('blue')  
        
        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill='both')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight='1')
        
        self.frames = {}        
        
        for F in (FrameLogin, FrameCadastro):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.mostrar_frame(FrameLogin)

    def mostrar_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class FrameLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)        
        self.controller = controller
        
        #titulo e login
        titulo_app = ctk.CTkLabel(self, text='\nKeyNoki', font=('helvetica', 26, 'bold'))
        titulo_app.pack(pady=15)

        login_usuario = ctk.CTkLabel(self, text='Login', font=('helvetica', 20, 'bold'))
        login_usuario.pack(pady=(75, 10))

        #caixa de texto senha
        self.entrada_senha = ctk.CTkEntry(self, width=220, height= 40, placeholder_text='Digite sua senha')
        self.entrada_senha.pack(pady=(15, 15))

        #botão
        self.botao_logar = ctk.CTkButton(self, text='Iniciar sessão', command=self.validar_login)
        self.botao_logar.pack(pady=20)
        
        self.label_mensagem = ctk.CTkLabel(self, text='', font=('helvetica', 12, 'bold'), text_color='red')
        self.label_mensagem.pack(pady=(0, 10))
    
    def validar_login(self):
        validar_login(self.entrada_senha, self.label_mensagem) 
        
class FrameCadastro(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)        
        titulo_app = ctk.CTkLabel(self, text='\nKeyNoki', font=('helvetica', 26, 'bold'))
        titulo_app.pack(pady=15)
        
        botao_cadastrar = ctk.CTkButton(self, text='Cadastre sua senha', width=200, height=40)
        botao_cadastrar.pack(pady=20)
        
        self.controller = controller

janela = tela_login()


class menu_inicial(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('KeyNoki - Menu')
        self.geometry('800x600')

        ctk.set_appearance_mode('black')
        ctk.set_default_color_theme('blue')
        
#titulo do menu ---------------------------------------------------------------------------------------------------------------------------------
        titulo_menu = ctk.CTkLabel(self, text='\nMenu Principal', font=('helvetica', 26, 'bold'))
        titulo_menu.pack(pady=30)

        botao_adicionar = ctk.CTkButton(self, text='Adicionar nova senha', width=200, height=40)
        botao_adicionar.pack(pady=10)

        
janela.mainloop()
