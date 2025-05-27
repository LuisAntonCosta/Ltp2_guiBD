import sqlite3
from tkinter import messagebox

# --- Conexão e Cursor ---
try:
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    print("Banco de dados conectado com sucesso!")
except sqlite3.Error as e:
    messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao banco: {e}")
    exit()

# --- Funções de Criação ---
def criar_tabelas():
    """Cria as tabelas 'autores' e 'livros' se não existirem."""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS autores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor_id INTEGER NOT NULL,
                FOREIGN KEY (autor_id) REFERENCES autores (id)
                    ON DELETE RESTRICT -- Impede excluir autor com livros
            )
        """)
        conexao.commit()
        print("Tabelas verificadas/criadas.")
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Criar Tabelas", f"Erro: {e}")

# --- Funções CRUD para Autores ---
def inserir_autor(nome):
    """Insere um novo autor no banco."""
    if not nome:
        messagebox.showwarning("Atenção", "O nome do autor não pode ser vazio.")
        return False
    try:
        cursor.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        messagebox.showwarning("Erro de Integridade", f"O autor '{nome}' já existe.")
        return False
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Inserir Autor", f"Erro: {e}")
        return False

def listar_autores():
    """Retorna uma lista de todos os autores (id, nome)."""
    try:
        cursor.execute("SELECT * FROM autores ORDER BY nome")
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Listar Autores", f"Erro: {e}")
        return []

def excluir_autor(id_autor):
    """Exclui um autor pelo ID."""
    try:
        cursor.execute("DELETE FROM autores WHERE id = ?", (id_autor,))
        conexao.commit()
        return cursor.rowcount > 0 # Retorna True se excluiu, False se não
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro de Integridade", "Não é possível excluir um autor que possui livros cadastrados.")
        return False
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Excluir Autor", f"Erro: {e}")
        return False

# --- Funções CRUD para Livros ---
def inserir_livro(titulo, autor_id):
    """Insere um novo livro no banco."""
    if not titulo or not autor_id:
        messagebox.showwarning("Atenção", "Preencha o título e selecione um autor.")
        return False
    try:
        cursor.execute("INSERT INTO livros (titulo, autor_id) VALUES (?, ?)", (titulo, autor_id))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Inserir Livro", f"Erro: {e}")
        return False

def listar_livros():
    """Retorna uma lista de todos os livros (id_livro, titulo, nome_autor)."""
    try:
        cursor.execute("""
            SELECT l.id, l.titulo, a.nome
            FROM livros l
            JOIN autores a ON l.autor_id = a.id
            ORDER BY l.titulo
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Listar Livros", f"Erro: {e}")
        return []

def listar_livros_por_autor(autor_id):
    """Retorna uma lista de livros de um autor específico."""
    try:
        cursor.execute("""
            SELECT l.id, l.titulo, a.nome
            FROM livros l
            JOIN autores a ON l.autor_id = a.id
            WHERE a.id = ?
            ORDER BY l.titulo
        """, (autor_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Listar Livros", f"Erro: {e}")
        return []


def atualizar_livro(id_livro, novo_titulo, novo_autor_id):
    """Atualiza o título e/ou autor de um livro."""
    if not novo_titulo or not novo_autor_id:
        messagebox.showwarning("Atenção", "Preencha o título e selecione um autor para atualizar.")
        return False
    try:
        cursor.execute("UPDATE livros SET titulo = ?, autor_id = ? WHERE id = ?",
                       (novo_titulo, novo_autor_id, id_livro))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Atualizar Livro", f"Erro: {e}")
        return False

def excluir_livro(id_livro):
    """Exclui um livro pelo ID."""
    try:
        cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Excluir Livro", f"Erro: {e}")
        return False

# --- Fechamento ---
def fechar_conexao():
    """Fecha a conexão com o banco de dados."""
    if conexao:
        conexao.close()
        print("Conexão com o banco fechada.")
