import customtkinter as ctk
from gerenciador_de_senhas import GerenciadorSenhas
import hashlib

#CONFIGURAÇÕES INICIAIS ------------------------------------------------------------------------------------------------------------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

gm = GerenciadorSenhas()

#CLASS PRINCPAL ------------------------------------------------------------------------------------------------------------------------------------------------------
class AppSenhas(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🔐 KeyNoki - Gerenciador de Senhas")
        self.geometry("600x700")
        self.resizable(False, False)
        
#Centralizar na tela------------------------------------------------------------------------------------------------------------------------------------------------------
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f'600x700+{x}+{y}')
        
#Container principal ------------------------------------------------------------------------------------------------------------------------------------------------------
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
#Criar todos os frames------------------------------------------------------------------------------------------------------------------------------------------------------
        for F in (TelaCadastro, TelaLogin, TelaMenu, TelaAdicionarSenha, TelaMostrarSenhas):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
#Determinar qual tela mostrar------------------------------------------------------------------------------------------------------------------------------------------------------
        if gm.senha_mestre is None:
            self.mostrar_frame(TelaCadastro)
        else:
            self.mostrar_frame(TelaLogin)
    
    def mostrar_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
#Se for a tela de mostrar senhas, atualizar os dados------------------------------------------------------------------------------------------------------------------------------------------------------
        if cont == TelaMostrarSenhas:
            frame.atualizar_senhas()


#tela de cadastro ------------------------------------------------------------------------------------------------------------------------------------------------------
class TelaCadastro(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
#Logo/Título------------------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ctk.CTkLabel(self, text="🔐 KeyNoki", font=("Helvetica", 40, "bold"))
        titulo.pack(pady=30)
        
        subtitulo = ctk.CTkLabel(self, text="Crie sua Senha Mestre", font=("Helvetica", 16))
        subtitulo.pack(pady=(0, 30))
        
#Frame para inputs------------------------------------------------------------------------------------------------------------------------------------------------------
        frame_inputs = ctk.CTkFrame(self)
        frame_inputs.pack(pady=20, padx=40, fill="both", expand=False)
        
#Label + Input Senha------------------------------------------------------------------------------------------------------------------------------------------------------
        label_senha = ctk.CTkLabel(frame_inputs, text="Nova Senha:", font=("Helvetica", 12))
        label_senha.pack(pady=(0, 5))
        
        self.entrada_senha = ctk.CTkEntry(frame_inputs, placeholder_text="Digite uma senha forte", show="*", height=40)
        self.entrada_senha.pack(fill="x", pady=(0, 15))
        
#Label + Input Confirmar------------------------------------------------------------------------------------------------------------------------------------------------------
        label_confirmar = ctk.CTkLabel(frame_inputs, text="Confirmar Senha:", font=("Helvetica", 12))
        label_confirmar.pack(pady=(0, 5))
        
        self.entrada_confirmar = ctk.CTkEntry(frame_inputs, placeholder_text="Confirme sua senha", show="*", height=40)
        self.entrada_confirmar.pack(fill="x", pady=(0, 20))
        
#Label de mensagem------------------------------------------------------------------------------------------------------------------------------------------------------
        self.label_mensagem = ctk.CTkLabel(frame_inputs, text="", font=("Helvetica", 12, "bold"), text_color="red")
        self.label_mensagem.pack(pady=(0, 10))
        
#Botão Registrar------------------------------------------------------------------------------------------------------------------------------------------------------
        botao_registro = ctk.CTkButton(
            frame_inputs,
            text="Criar Conta",
            height=40,
            font=("Helvetica", 14, "bold"),
            command=self.validar_cadastro
        )
        botao_registro.pack(fill="x", pady=10)
        
#Info------------------------------------------------------------------------------------------------------------------------------------------------------
        info = ctk.CTkLabel(self, text="Sua senha será criptografada e segura", font=("Helvetica", 10), text_color="gray")
        info.pack(pady=20)
    
    def validar_cadastro(self):
        senha = self.entrada_senha.get().strip()
        confirmar = self.entrada_confirmar.get().strip()
        
#Validações------------------------------------------------------------------------------------------------------------------------------------------------------
        if not senha or not confirmar:
            self.label_mensagem.configure(text="Preencha todos os campos!", text_color="red")
            return
        
        if len(senha) < 6:
            self.label_mensagem.configure(text="Senha deve ter mínimo 6 caracteres!", text_color="red")
            return
        
        if senha != confirmar:
            self.label_mensagem.configure(text="As senhas não conferem!", text_color="red")
            self.entrada_senha.delete(0, ctk.END)
            self.entrada_confirmar.delete(0, ctk.END)
            return
        
#Salvar senha------------------------------------------------------------------------------------------------------------------------------------------------------
        cripto256 = hashlib.sha256(senha.encode())
        gm.senha_mestre = cripto256.hexdigest()
        gm.dados = {}
        
#Criar chave e salvar dados------------------------------------------------------------------------------------------------------------------------------------------------------
        from cryptography.fernet import Fernet
        import os
        
        chave_nova = Fernet.generate_key()
        with open('Chave.key', 'wb') as f:
            f.write(chave_nova)
        gm.f = Fernet(chave_nova)
        gm.salvar_dados()
        
        self.label_mensagem.configure(text="Conta criada com sucesso!", text_color="green")
        self.entrada_senha.delete(0, ctk.END)
        self.entrada_confirmar.delete(0, ctk.END)
        
        self.after(1500, lambda: self.controller.mostrar_frame(TelaLogin))


#tela login ------------------------------------------------------------------------------------------------------------------------------------------------------
class TelaLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
#Logo------------------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ctk.CTkLabel(self, text="🔐 KeyNoki", font=("Helvetica", 40, "bold"))
        titulo.pack(pady=30)
        
        subtitulo = ctk.CTkLabel(self, text="Bem-vindo de volta!", font=("Helvetica", 16))
        subtitulo.pack(pady=(0, 40))
        
#Frame para input ------------------------------------------------------------------------------------------------------------------------------------------------------
        frame_input = ctk.CTkFrame(self)
        frame_input.pack(pady=20, padx=40, fill="both", expand=False)
        
        label_senha = ctk.CTkLabel(frame_input, text="Senha Mestre:", font=("Helvetica", 12))
        label_senha.pack(pady=(0, 5))
        
        self.entrada_senha = ctk.CTkEntry(frame_input, placeholder_text="Digite sua senha", show="*", height=40)
        self.entrada_senha.pack(fill="x", pady=(0, 15))
        self.entrada_senha.bind("<Return>", lambda e: self.fazer_login())
        
#Label de mensagem ------------------------------------------------------------------------------------------------------------------------------------------------------
        self.label_mensagem = ctk.CTkLabel(frame_input, text="", font=("Helvetica", 12, "bold"), text_color="red")
        self.label_mensagem.pack(pady=(0, 10))
        
#Botão Login ------------------------------------------------------------------------------------------------------------------------------------------------------
        botao_login = ctk.CTkButton(
            frame_input,
            text="Entrar",
            height=40,
            font=("Helvetica", 14, "bold"),
            command=self.fazer_login
        )
        botao_login.pack(fill="x", pady=10)
    
    def fazer_login(self):
        senha = self.entrada_senha.get().strip()
        
        if not senha:
            self.label_mensagem.configure(text="Digite sua senha!", text_color="red")
            return
        
        if gm.autenticar(senha):
            self.entrada_senha.delete(0, ctk.END)
            self.label_mensagem.configure(text="", text_color="white")
            self.controller.mostrar_frame(TelaMenu)
        else:
            self.label_mensagem.configure(text="Senha incorreta!", text_color="red")
            self.entrada_senha.delete(0, ctk.END)


#TELA MENU ------------------------------------------------------------------------------------------------------------------------------------------------------
class TelaMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
#Header------------------------------------------------------------------------------------------------------------------------------------------------------
        header = ctk.CTkFrame(self, fg_color="#1f1f1f")
        header.pack(fill="x", pady=(0, 20))
        
        titulo = ctk.CTkLabel(header, text="🔐 Suas Senhas", font=("Helvetica", 28, "bold"))
        titulo.pack(pady=15)
        
#Botões principais------------------------------------------------------------------------------------------------------------------------------------------------------
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(pady=20, padx=30, fill="both")
        
#Botão Adicionar------------------------------------------------------------------------------------------------------------------------------------------------------
        botao_adicionar = ctk.CTkButton(
            frame_botoes,
            text="Adicionar Nova Senha",
            height=50,
            font=("Helvetica", 14, "bold"),
            fg_color="#0d47a1",
            hover_color="#0a3a80",
            command=lambda: self.controller.mostrar_frame(TelaAdicionarSenha)
        )
        botao_adicionar.pack(fill="x", pady=10)
        
#Botão Mostrar ------------------------------------------------------------------------------------------------------------------------------------------------------
        botao_mostrar = ctk.CTkButton(
            frame_botoes,
            text="Ver Todas as Senhas",
            height=50,
            font=("Helvetica", 14, "bold"),
            fg_color="#1565c0",
            hover_color="#0d47a1",
            command=lambda: self.controller.mostrar_frame(TelaMostrarSenhas)
        )
        botao_mostrar.pack(fill="x", pady=10)
        
#Botão Sair------------------------------------------------------------------------------------------------------------------------------------------------------
        botao_sair = ctk.CTkButton(
            frame_botoes,
            text="Sair",
            height=50,
            font=("Helvetica", 14, "bold"),
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=lambda: self.sair()
        )
        botao_sair.pack(fill="x", pady=10)
 
 #Info------------------------------------------------------------------------------------------------------------------------------------------------------
        info = ctk.CTkLabel(self, text="Suas senhas estão seguras e criptografadas", font=("Helvetica", 10), text_color="gray")
        info.pack(pady=20)
    
    def sair(self):
        self.controller.mostrar_frame(TelaLogin)


#tela add senha ---------------------------------------------------------------------------------------------------------------------------------------------------------
class TelaAdicionarSenha(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
#Header------------------------------------------------------------------------------------------------------------------------------------------------------
        frame_header = ctk.CTkFrame(self)
        frame_header.pack(fill="x", pady=(0, 20))
        
        titulo = ctk.CTkLabel(frame_header, text="➕ Adicionar Nova Senha", font=("Helvetica", 24, "bold"))
        titulo.pack(pady=15, padx=20, anchor="w")
        
#Frame inputs------------------------------------------------------------------------------------------------------------------------------------------------------
        frame_inputs = ctk.CTkFrame(self)
        frame_inputs.pack(pady=20, padx=30, fill="both", expand=True)
        
#Serviço------------------------------------------------------------------------------------------------------------------------------------------------------
        label_servico = ctk.CTkLabel(frame_inputs, text="Nome do Serviço:", font=("Helvetica", 12))
        label_servico.pack(pady=(0, 5), anchor="w")
        
        self.entrada_servico = ctk.CTkEntry(frame_inputs, placeholder_text="Ex: Gmail, Netflix, etc", height=40)
        self.entrada_servico.pack(fill="x", pady=(0, 15))
        
#Login------------------------------------------------------------------------------------------------------------------------------------------------------
        label_login = ctk.CTkLabel(frame_inputs, text="Login/Email:", font=("Helvetica", 12))
        label_login.pack(pady=(0, 5), anchor="w")
        
        self.entrada_login = ctk.CTkEntry(frame_inputs, placeholder_text="Seu email ou usuário", height=40)
        self.entrada_login.pack(fill="x", pady=(0, 15))
        
#Senha------------------------------------------------------------------------------------------------------------------------------------------------------
        label_senha = ctk.CTkLabel(frame_inputs, text="Senha:", font=("Helvetica", 12))
        label_senha.pack(pady=(0, 5), anchor="w")
        
        self.entrada_senha = ctk.CTkEntry(frame_inputs, placeholder_text="Sua senha", show="*", height=40)
        self.entrada_senha.pack(fill="x", pady=(0, 20))
        
#Mensagem------------------------------------------------------------------------------------------------------------------------------------------------------
        self.label_mensagem = ctk.CTkLabel(frame_inputs, text="", font=("Helvetica", 11, "bold"), text_color="green")
        self.label_mensagem.pack(pady=(0, 15))
        
#Botões------------------------------------------------------------------------------------------------------------------------------------------------------
        frame_botoes = ctk.CTkFrame(frame_inputs)
        frame_botoes.pack(fill="x")
        
        botao_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            height=40,
            font=("Helvetica", 12, "bold"),
            command=self.salvar_senha
        )
        botao_salvar.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        botao_voltar = ctk.CTkButton(
            frame_botoes,
            text="Voltar",
            height=40,
            font=("Helvetica", 12, "bold"),
            fg_color="#555555",
            hover_color="#444444",
            command=lambda: self.controller.mostrar_frame(TelaMenu)
        )
        botao_voltar.pack(side="left", fill="x", expand=True, padx=(5, 0))
    
    def salvar_senha(self):
        servico = self.entrada_servico.get().strip()
        login = self.entrada_login.get().strip()
        senha = self.entrada_senha.get().strip()
        
        if not servico or not login or not senha:
            self.label_mensagem.configure(text="Preencha todos os campos!", text_color="red")
            return
        
        try:
            gm.adicionar_senha(servico, login, senha)
            
            self.entrada_servico.delete(0, ctk.END)
            self.entrada_login.delete(0, ctk.END)
            self.entrada_senha.delete(0, ctk.END)
            
            self.label_mensagem.configure(text="Senha salva com sucesso!", text_color="green")
            self.after(1500, lambda: self.controller.mostrar_frame(TelaMenu))
            
        except Exception as e:
            self.label_mensagem.configure(text=f"Erro ao salvar: {str(e)}", text_color="red")


#TELA MOSTRAR SENHAS ---------------------------------------------------------------------------------------------------------------------------------------------------------
class TelaMostrarSenhas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
#Header------------------------------------------------------------------------------------------------------------------------------------------------------
        frame_header = ctk.CTkFrame(self)
        frame_header.pack(fill="x", pady=(0, 10))
        
        titulo = ctk.CTkLabel(frame_header, text="Suas Senhas", font=("Helvetica", 24, "bold"))
        titulo.pack(pady=15, padx=20, anchor="w")
        
#Frame scrollável------------------------------------------------------------------------------------------------------------------------------------------------------
        self.frame_scrollavel = ctk.CTkScrollableFrame(self)
        self.frame_scrollavel.pack(fill="both", expand=True, padx=20, pady=10)
        
#Botões inferiores------------------------------------------------------------------------------------------------------------------------------------------------------
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(fill="x", padx=20, pady=10)
        
        botao_recarregar = ctk.CTkButton(
         frame_botoes,
         text="Recarregar",
         height=40,
         font=("Helvetica", 12, "bold"),
         width=100,
         command=self.atualizar_senhas
        )
        botao_recarregar.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        botao_voltar = ctk.CTkButton(
         frame_botoes,
         text="Voltar",
         height=40,
         font=("Helvetica", 12, "bold"),
         fg_color="#555555",
         hover_color="#444444",
         width=100,
         command=lambda: self.controller.mostrar_frame(TelaMenu)
        )
        botao_voltar.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        self.atualizar_senhas()
    
    def atualizar_senhas(self):
#Remover widgets antigos------------------------------------------------------------------------------------------------------------------------------------------------------
        for widget in self.frame_scrollavel.winfo_children():
            widget.destroy()
        
        senhas_por_servico = gm.obter_senhas_por_servico()
        
        if not senhas_por_servico:
            label_vazio = ctk.CTkLabel(
                self.frame_scrollavel,
                text="Nenhuma senha salva ainda",
                font=("Helvetica", 14),
                text_color="gray"
            )
            label_vazio.pack(pady=40)
            return
        
#Mostrar cada serviço com múltiplas senhas------------------------------------------------------------------------------------------------------------------------------------------------------
        for servico, senhas_lista in senhas_por_servico.items():
            label_servico = ctk.CTkLabel(
                self.frame_scrollavel,
                text=f"{servico.upper()}",
                font=("Helvetica", 14, "bold")
            )
            label_servico.pack(fill="x", pady=(15, 10), padx=10)
            
            for senha_info in senhas_lista:
                frame_senha = ctk.CTkFrame(self.frame_scrollavel, corner_radius=10, fg_color="#2b2b2b")
                frame_senha.pack(fill="x", pady=8, padx=10)
                
#Login------------------------------------------------------------------------------------------------------------------------------------------------------ 
                frame_login = ctk.CTkFrame(frame_senha, fg_color="transparent")
                frame_login.pack(fill="x", padx=15, pady=(10, 5))
                
                label_login_texto = ctk.CTkLabel(frame_login, text="Login/Email:", font=("Helvetica", 10, "bold"))
                label_login_texto.pack(side="left", padx=(0, 10))
                
                label_login_valor = ctk.CTkLabel(frame_login, text=senha_info['login'], font=("Helvetica", 10), text_color="#64b5f6")
                label_login_valor.pack(side="left")
                
#Senha com toggle------------------------------------------------------------------------------------------------------------------------------------------------------
                frame_senha_display = ctk.CTkFrame(frame_senha, fg_color="transparent")
                frame_senha_display.pack(fill="x", padx=15, pady=5)
                
                label_senha_texto = ctk.CTkLabel(frame_senha_display, text="Senha:", font=("Helvetica", 10, "bold"))
                label_senha_texto.pack(side="left", padx=(0, 10))
                
                senha_label = ctk.CTkLabel(frame_senha_display, text="••••••••", font=("Helvetica", 10), text_color="#64b5f6")
                senha_label.pack(side="left", padx=(0, 10))
                
                def criar_funcao_toggle(label, senha_criptografada):
                    def toggle():
                        if label.cget("text") == "••••••••":
                            try:
                                senha_real = gm.f.decrypt(senha_criptografada.encode()).decode()
                                label.configure(text=senha_real)
                            except:
                                label.configure(text="[Erro]", text_color="red")
                        else:
                            label.configure(text="••••••••", text_color="#64b5f6")
                    return toggle
                
                botao_toggle = ctk.CTkButton(
                    frame_senha_display,
                    text="👁️",
                    width=35,
                    height=25,
                    font=("Helvetica", 11),
                    command=criar_funcao_toggle(senha_label, senha_info['senha'])
                )
                botao_toggle.pack(side="left", padx=(0, 5))
                
                def criar_funcao_deletar(id_senha):
                    def deletar():
                        gm.deletar_senha(id_senha)
                        self.atualizar_senhas()
                    return deletar
                
                botao_deletar = ctk.CTkButton(
                    frame_senha_display,
                    text="Deletar Senha",
                    width=35,
                    height=25,
                    font=("Helvetica", 11),
                    fg_color="#d32f2f",
                    hover_color="#b71c1c",
                    command=criar_funcao_deletar(senha_info['id'])
                )
                botao_deletar.pack(side="left")


#EXECUTAR O APP ------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = AppSenhas()
    app.mainloop()
