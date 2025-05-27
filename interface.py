import tkinter as tk
from tkinter import messagebox
import banco

# --- Funções de Ajuda ---
def extrair_id(texto_listbox):
    """Extrai o ID do texto formatado da Listbox (ex: 'ID: 1 | ...')."""
    try:
        if texto_listbox and '|' in texto_listbox and ':' in texto_listbox:
            parte_id = texto_listbox.split('|')[0] # Pega "ID: 1 "
            id_str = parte_id.split(':')[1]     # Pega " 1 "
            return int(id_str.strip())              # Pega 1 (como inteiro)
        return None # Retorna None se o formato for inválido
    except (IndexError, ValueError, AttributeError):
        # Retorna None se houver erro na divisão ou conversão
        return None

# --- Funções de Atualização da Interface ---
def atualizar_lista_autores(listbox):
    """Limpa e preenche a Listbox de autores."""
    listbox.delete(0, tk.END) # Limpa a lista
    autores = banco.listar_autores() # Busca os dados
    if autores: # Se houver autores
        for autor in autores:
            # Insere no formato "ID: X | Nome"
            listbox.insert(tk.END, f"ID: {autor[0]} | {autor[1]}")

def atualizar_lista_livros(listbox):
    """Limpa e preenche a Listbox de livros."""
    listbox.delete(0, tk.END) # Limpa a lista
    livros = banco.listar_livros() # Busca os dados
    if livros: # Se houver livros
        for livro in livros:
            # Insere no formato "ID: X | Título | Autor: Nome"
            listbox.insert(tk.END, f"ID: {livro[0]} | {livro[1]} | Autor: {livro[2]}")

def atualizar_tudo(lb_autores, lb_livros):
    """Atualiza ambas as Listboxes."""
    atualizar_lista_autores(lb_autores)
    atualizar_lista_livros(lb_livros)

# --- Funções de Callback (Ações dos Botões) ---
def adicionar_autor_click(entry, lb_autores, lb_livros):
    """Adiciona um novo autor."""
    nome = entry.get()
    if not nome:
        messagebox.showwarning("Atenção", "Digite o nome do autor.")
        return

    if banco.inserir_autor(nome):
        messagebox.showinfo("Sucesso", f"Autor '{nome}' adicionado!")
        entry.delete(0, tk.END)
        atualizar_tudo(lb_autores, lb_livros)
    else:
        entry.focus_set()

def excluir_autor_click(lb_autores, lb_livros):
    """Exclui o autor selecionado na Listbox."""
    try:
        # Pega a tupla de índices selecionados
        indices_selecionados = lb_autores.curselection()
        # Verifica se algo foi selecionado
        if not indices_selecionados:
            messagebox.showwarning("Atenção", "Selecione um autor na lista para excluir.")
            return

        # Pega o primeiro índice (Listbox está em modo single select)
        selecionado_idx = indices_selecionados[0]
        texto_selecionado = lb_autores.get(selecionado_idx)
        id_autor = extrair_id(texto_selecionado)

        if id_autor is None:
            messagebox.showerror("Erro", "Não foi possível identificar o ID do autor.")
            return

        nome_autor = texto_selecionado.split('|')[1].strip()

        if messagebox.askyesno("Confirmar", f"Deseja excluir o autor '{nome_autor}'?"):
            if banco.excluir_autor(id_autor):
                messagebox.showinfo("Sucesso", "Autor excluído!")
                atualizar_tudo(lb_autores, lb_livros)
            # else: banco.py já mostra o erro (ex: autor com livros)

    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao excluir autor: {e}")


def adicionar_livro_click(entry, lb_autores, lb_livros):
    """Adiciona um novo livro."""
    titulo = entry.get()
    if not titulo:
        messagebox.showwarning("Atenção", "Digite o título do livro.")
        return

    try:
        # Pega a seleção da lista de autores
        indices_selecionados = lb_autores.curselection()
        if not indices_selecionados:
            messagebox.showwarning("Atenção", "Selecione um autor na lista antes de adicionar um livro.")
            return

        selecionado_idx = indices_selecionados[0]
        texto_autor = lb_autores.get(selecionado_idx)
        id_autor = extrair_id(texto_autor)

        if id_autor is None:
            messagebox.showerror("Erro", "Selecione um autor válido na lista de autores.")
            return

        if banco.inserir_livro(titulo, id_autor):
            messagebox.showinfo("Sucesso", f"Livro '{titulo}' adicionado!")
            entry.delete(0, tk.END)
            atualizar_lista_livros(lb_livros)
        # else: banco.py mostra o erro

    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao adicionar livro: {e}")


def excluir_livro_click(lb_livros):
    """Exclui o livro selecionado na Listbox."""
    try:
        # 1. Pega a tupla de índices selecionados
        indices_selecionados = lb_livros.curselection()
        # 2. Verifica se algo foi selecionado
        if not indices_selecionados:
            messagebox.showwarning("Atenção", "Selecione um livro na lista para excluir.")
            return

        # 3. Pega o primeiro índice e o texto
        selecionado_idx = indices_selecionados[0]
        texto_selecionado = lb_livros.get(selecionado_idx)
        # 4. Extrai o ID
        id_livro = extrair_id(texto_selecionado)

        # DEBUG: Imprime no console para verificação
        print(f"--- TENTANDO EXCLUIR LIVRO ---")
        print(f"Texto selecionado: '{texto_selecionado}'")
        print(f"ID extraído: {id_livro}")
        print(f"-----------------------------")

        # 5. Verifica se o ID foi extraído
        if id_livro is None:
            messagebox.showerror("Erro", "Não foi possível identificar o ID do livro. O formato na lista está correto?")
            return

        # 6. Pega o título para a confirmação
        titulo_livro = texto_selecionado.split('|')[1].strip()

        # 7. Pede confirmação
        if messagebox.askyesno("Confirmar", f"Deseja excluir o livro '{titulo_livro}'?"):
            # 8. Tenta excluir e dá feedback
            if banco.excluir_livro(id_livro):
                messagebox.showinfo("Sucesso", "Livro excluído!")
                atualizar_lista_livros(lb_livros) # Atualiza a lista
            else:
                messagebox.showerror("Falha", "Não foi possível excluir o livro (ID não encontrado ou erro no banco).")

    except Exception as e:
        # Pega qualquer outro erro inesperado
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao excluir livro: {e}")


# --- Função Principal da Interface ---
def iniciar_interface():
    """Cria e configura a janela principal e seus widgets."""
    root = tk.Tk()
    root.title("Sistema de Biblioteca (Simples v2)")
    root.geometry("550x700") # Aumentei um pouco a altura

    # --- Frame Autores ---
    frame_autores = tk.Frame(root, bd=2, relief=tk.GROOVE, padx=10, pady=10)
    frame_autores.pack(pady=10, padx=10, fill=tk.X)

    tk.Label(frame_autores, text="--- Gestão de Autores ---", font=("Arial", 11, "bold")).pack()
    tk.Label(frame_autores, text="Nome do Autor:").pack()
    entry_autor = tk.Entry(frame_autores, width=50)
    entry_autor.pack(pady=2)
    btn_add_autor = tk.Button(frame_autores, text="Adicionar Autor")
    btn_add_autor.pack(pady=5)

    tk.Label(frame_autores, text="Autores Cadastrados:").pack(pady=(10, 2))
    # Frame para Listbox e Scrollbar de Autores
    frame_lb_autores = tk.Frame(frame_autores)
    scrollbar_autores = tk.Scrollbar(frame_lb_autores, orient=tk.VERTICAL)
    listbox_autores = tk.Listbox(frame_lb_autores, width=60, height=6, yscrollcommand=scrollbar_autores.set)
    scrollbar_autores.config(command=listbox_autores.yview)
    scrollbar_autores.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_autores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame_lb_autores.pack(pady=5)

    btn_del_autor = tk.Button(frame_autores, text="Excluir Autor Selecionado")
    btn_del_autor.pack(pady=5)

    # --- Frame Livros ---
    frame_livros = tk.Frame(root, bd=2, relief=tk.GROOVE, padx=10, pady=10)
    frame_livros.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    tk.Label(frame_livros, text="--- Gestão de Livros ---", font=("Arial", 11, "bold")).pack()
    tk.Label(frame_livros, text="Título do Livro:").pack()
    entry_livro = tk.Entry(frame_livros, width=50)
    entry_livro.pack(pady=2)
    tk.Label(frame_livros, text="(Selecione o autor na lista acima antes de adicionar)").pack()
    btn_add_livro = tk.Button(frame_livros, text="Adicionar Livro")
    btn_add_livro.pack(pady=5)

    tk.Label(frame_livros, text="Livros Cadastrados:").pack(pady=(10, 2))
    # Frame para Listbox e Scrollbar de Livros
    frame_lb_livros = tk.Frame(frame_livros)
    scrollbar_livros = tk.Scrollbar(frame_lb_livros, orient=tk.VERTICAL)
    listbox_livros = tk.Listbox(frame_lb_livros, width=60, height=10, yscrollcommand=scrollbar_livros.set)
    scrollbar_livros.config(command=listbox_livros.yview)
    scrollbar_livros.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_livros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame_lb_livros.pack(pady=5, expand=True, fill=tk.BOTH)

    btn_del_livro = tk.Button(frame_livros, text="Excluir Livro Selecionado")
    btn_del_livro.pack(pady=5)

    # --- Configuração dos Comandos dos Botões ---
    btn_add_autor.config(command=lambda: adicionar_autor_click(entry_autor, listbox_autores, listbox_livros))
    btn_del_autor.config(command=lambda: excluir_autor_click(listbox_autores, listbox_livros))
    btn_add_livro.config(command=lambda: adicionar_livro_click(entry_livro, listbox_autores, listbox_livros))
    # AQUI: Garante que o botão de excluir livro chama a função correta
    btn_del_livro.config(command=lambda: excluir_livro_click(listbox_livros))

    # --- Carregamento Inicial ---
    atualizar_tudo(listbox_autores, listbox_livros)

    # --- Loop Principal ---
    root.mainloop()
