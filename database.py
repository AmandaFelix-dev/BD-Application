import sqlite3
from models import escrever_log

class HQDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('hq_catalog.db')
        self.cursor = self.conn.cursor()
    
    # --- EDITORAS ---
    def inserir_editora(self, nome, pais=None):
        try:
            self.cursor.execute("INSERT INTO editoras (nome, pais) VALUES (?, ?)", (nome, pais))
            self.conn.commit()
            escrever_log(f"Editora inserida: {nome}")
            return True
        except sqlite3.IntegrityError:
            escrever_log(f"Erro: Editora {nome} já existe")
            return False
    
    def atualizar_editora(self, id, nome, pais=None):
        try:
            self.cursor.execute("UPDATE editoras SET nome = ?, pais = ? WHERE id = ?", (nome, pais, id))
            self.conn.commit()
            escrever_log(f"Editora ID {id} atualizada")
            return True
        except Exception as e:
            escrever_log(f"Erro ao atualizar editora: {str(e)}")
            return False
    
    def excluir_editora(self, id):
        try:
            self.cursor.execute("DELETE FROM editoras WHERE id = ?", (id,))
            self.conn.commit()
            escrever_log(f"Editora ID {id} excluída")
            return True
        except sqlite3.IntegrityError:
            escrever_log(f"Erro: Editora ID {id} possui séries associadas")
            return False
    
    def buscar_editora(self, id):
        self.cursor.execute("SELECT id, nome, pais FROM editoras WHERE id = ?", (id,))
        return self.cursor.fetchone()
    
    def listar_editoras(self):
        self.cursor.execute("SELECT id, nome, pais FROM editoras ORDER BY nome")
        return self.cursor.fetchall()
    
    # --- SÉRIES ---
    def inserir_serie(self, titulo, editora_id, ano_lancamento=None, status='Ativa'):
        try:
            self.cursor.execute('''
            INSERT INTO series (titulo, editora_id, ano_lancamento, status)
            VALUES (?, ?, ?, ?)
            ''', (titulo, editora_id, ano_lancamento, status))
            self.conn.commit()
            escrever_log(f"Série inserida: {titulo}")
            return True
        except Exception as e:
            escrever_log(f"Erro ao inserir série: {str(e)}")
            return False
    
    def atualizar_serie(self, id, titulo=None, editora_id=None, ano_lancamento=None, status=None):
        try:
            serie_atual = self.buscar_serie(id)
            if not serie_atual:
                return False
                
            titulo = titulo or serie_atual[1]
            editora_id = editora_id or serie_atual[2]
            ano_lancamento = ano_lancamento or serie_atual[3]
            status = status or serie_atual[4]
            
            self.cursor.execute('''
            UPDATE series SET titulo = ?, editora_id = ?, ano_lancamento = ?, status = ?
            WHERE id = ?
            ''', (titulo, editora_id, ano_lancamento, status, id))
            self.conn.commit()
            escrever_log(f"Série ID {id} atualizada")
            return True
        except Exception as e:
            escrever_log(f"Erro ao atualizar série: {str(e)}")
            return False
    
    def excluir_serie(self, id):
        try:
            self.cursor.execute("DELETE FROM series WHERE id = ?", (id,))
            self.conn.commit()
            escrever_log(f"Série ID {id} excluída")
            return True
        except sqlite3.IntegrityError:
            escrever_log(f"Erro: Série ID {id} possui edições associadas")
            return False
    
    def buscar_serie(self, id):
        self.cursor.execute('''
        SELECT s.id, s.titulo, e.nome, s.ano_lancamento, s.status
        FROM series s JOIN editoras e ON s.editora_id = e.id
        WHERE s.id = ?
        ''', (id,))
        return self.cursor.fetchone()
    
    def listar_series(self, editora_id=None):
        if editora_id:
            self.cursor.execute('''
            SELECT s.id, s.titulo, e.nome, s.ano_lancamento, s.status
            FROM series s JOIN editoras e ON s.editora_id = e.id
            WHERE s.editora_id = ?
            ORDER BY s.titulo
            ''', (editora_id,))
        else:
            self.cursor.execute('''
            SELECT s.id, s.titulo, e.nome, s.ano_lancamento, s.status
            FROM series s JOIN editoras e ON s.editora_id = e.id
            ORDER BY s.titulo
            ''')
        return self.cursor.fetchall()
    
    # --- EDIÇÕES ---
    def inserir_edicao(self, serie_id, numero, titulo_edicao=None, data_publicacao=None, 
                      preco_original=None, preco_atual=None, quantidade=0):
        try:
            self.cursor.execute('''
            INSERT INTO edicoes 
            (serie_id, numero, titulo_edicao, data_publicacao, preco_original, preco_atual, quantidade_estoque)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (serie_id, numero, titulo_edicao, data_publicacao, preco_original, preco_atual, quantidade))
            self.conn.commit()
            escrever_log(f"Edição {numero} inserida para série ID {serie_id}")
            return True
        except Exception as e:
            escrever_log(f"Erro ao inserir edição: {str(e)}")
            return False
    
    def atualizar_edicao(self, id, **kwargs):
        try:
            campos = []
            valores = []
            for campo, valor in kwargs.items():
                campos.append(f"{campo} = ?")
                valores.append(valor)
            valores.append(id)
            
            query = f"UPDATE edicoes SET {', '.join(campos)} WHERE id = ?"
            self.cursor.execute(query, valores)
            self.conn.commit()
            escrever_log(f"Edição ID {id} atualizada")
            return True
        except Exception as e:
            escrever_log(f"Erro ao atualizar edição: {str(e)}")
            return False
    
    def excluir_edicao(self, id):
        try:
            self.cursor.execute("DELETE FROM edicoes WHERE id = ?", (id,))
            self.conn.commit()
            escrever_log(f"Edição ID {id} excluída")
            return True
        except Exception as e:
            escrever_log(f"Erro ao excluir edição: {str(e)}")
            return False
    
    def buscar_edicao(self, id):
        self.cursor.execute('''
        SELECT e.id, e.numero, e.titulo_edicao, e.data_publicacao, e.preco_original, 
               e.preco_atual, e.quantidade_estoque, s.titulo
        FROM edicoes e JOIN series s ON e.serie_id = s.id
        WHERE e.id = ?
        ''', (id,))
        return self.cursor.fetchone()
    
    def listar_edicoes(self, serie_id=None):
        if serie_id:
            self.cursor.execute('''
            SELECT e.id, e.numero, e.titulo_edicao, e.data_publicacao, e.preco_atual, e.quantidade_estoque
            FROM edicoes e
            WHERE e.serie_id = ?
            ORDER BY e.numero
            ''', (serie_id,))
        else:
            self.cursor.execute('''
            SELECT e.id, e.numero, s.titulo, e.titulo_edicao, e.preco_atual, e.quantidade_estoque
            FROM edicoes e JOIN series s ON e.serie_id = s.id
            ORDER BY s.titulo, e.numero
            ''')
        return self.cursor.fetchall()
    
    # --- RELATÓRIOS ---
    def estoque_baixo(self, limite=5):
        self.cursor.execute('''
        SELECT e.id, e.numero, s.titulo, e.quantidade_estoque
        FROM edicoes e JOIN series s ON e.serie_id = s.id
        WHERE e.quantidade_estoque < ?
        ORDER BY e.quantidade_estoque
        ''', (limite,))
        return self.cursor.fetchall()
    
    def series_por_status(self):
        self.cursor.execute('''
        SELECT status, COUNT(*) as total
        FROM series
        GROUP BY status
        ORDER BY total DESC
        ''')
        return self.cursor.fetchall()
    
    def historico_logs(self, limite=50):
        self.cursor.execute('''
        SELECT data_hora, tabela, operacao, id_registro, descricao
        FROM logs
        ORDER BY data_hora DESC
        LIMIT ?
        ''', (limite,))
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()