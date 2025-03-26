import sqlite3
from datetime import datetime

def criar_banco():
    conn = sqlite3.connect('hq_catalog.db')
    cursor = conn.cursor()
    
    # Tabela Editoras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS editoras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        pais TEXT,
        data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela Séries
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        editora_id INTEGER,
        ano_lancamento INTEGER,
        status TEXT CHECK(status IN ('Ativa', 'Concluída', 'Cancelada')),
        FOREIGN KEY (editora_id) REFERENCES editoras (id)
    )
    ''')
    
    # Tabela Edições
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS edicoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        serie_id INTEGER,
        numero INTEGER NOT NULL,
        titulo_edicao TEXT,
        data_publicacao DATE,
        preco_original REAL,
        preco_atual REAL,
        quantidade_estoque INTEGER DEFAULT 0,
        FOREIGN KEY (serie_id) REFERENCES series (id)
    )
    ''')
    
    # Tabela de Logs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tabela TEXT NOT NULL,
        operacao TEXT NOT NULL,
        id_registro INTEGER NOT NULL,
        data_hora TEXT NOT NULL,
        descricao TEXT
    )
    ''')
    
    # Triggers
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS log_nova_edicao
    AFTER INSERT ON edicoes
    BEGIN
        INSERT INTO logs (tabela, operacao, id_registro, data_hora)
        VALUES ('edicoes', 'INSERT', NEW.id, datetime('now', 'localtime'));
    END;
    ''')
    
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS log_edicao_estoque
    AFTER UPDATE OF quantidade_estoque ON edicoes
    BEGIN
        INSERT INTO logs (tabela, operacao, id_registro, data_hora, descricao)
        VALUES ('edicoes', 'UPDATE', NEW.id, datetime('now', 'localtime'),
               'Estoque alterado de ' || OLD.quantidade_estoque || ' para ' || NEW.quantidade_estoque);
    END;
    ''')
    
    conn.commit()
    conn.close()

def escrever_log(mensagem):
    with open('hq_catalog.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensagem}\n")