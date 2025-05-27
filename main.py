import interface
import banco
from tkinter import messagebox

if __name__ == "__main__":
    try:
        # Tenta criar as tabelas antes de iniciar a interface
        banco.criar_tabelas()
        # Inicia a interface gráfica
        interface.iniciar_interface()
    except Exception as e:
        messagebox.showerror("Erro Crítico", f"Ocorreu um erro inesperado: {e}")
    finally:
        banco.fechar_conexao()
