import sqlite3
from models import escrever_log

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('app.db')
        self.cursor = self.conn.cursor()
        
    def inserir_cliente(self, nome, email):
        try:
            self.cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))
            self.conn.commit()
            escrever_log(f"Cliente inserido: {nome}, {email}")
            return True
        except sqlite3.IntegrityError as e:
            escrever_log(f"Erro ao inserir cliente: {str(e)}")
            return False
    
    def atualizar_cliente(self, id, nome=None, email=None):
        try:
            if nome and email:
                self.cursor.execute("UPDATE clientes SET nome = ?, email = ? WHERE id = ?", (nome, email, id))
            elif nome:
                self.cursor.execute("UPDATE clientes SET nome = ? WHERE id = ?", (nome, id))
            elif email:
                self.cursor.execute("UPDATE clientes SET email = ? WHERE id = ?", (email, id))
            
            self.conn.commit()
            escrever_log(f"Cliente ID {id} atualizado")
            return True
        except Exception as e:
            escrever_log(f"Erro ao atualizar cliente ID {id}: {str(e)}")
            return False
    
    def deletar_cliente(self, id):
        try:
            self.cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
            self.conn.commit()
            escrever_log(f"Cliente ID {id} deletado")
            return True
        except Exception as e:
            escrever_log(f"Erro ao deletar cliente ID {id}: {str(e)}")
            return False
    
    def listar_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()
    
    def inserir_pedido(self, cliente_id, produto, valor):
        try:
            self.cursor.execute("INSERT INTO pedidos (cliente_id, produto, valor) VALUES (?, ?, ?)", 
                              (cliente_id, produto, valor))
            self.conn.commit()
            escrever_log(f"Pedido inserido para cliente ID {cliente_id}: {produto}, R${valor:.2f}")
            return True
        except Exception as e:
            escrever_log(f"Erro ao inserir pedido: {str(e)}")
            return False
    
    def listar_pedidos(self):
        self.cursor.execute('''
        SELECT p.id, c.nome, p.produto, p.valor, p.data_pedido 
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        ''')
        return self.cursor.fetchall()
    
    def listar_logs_trigger(self):
        self.cursor.execute("SELECT * FROM logs ORDER BY data_hora DESC")
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()