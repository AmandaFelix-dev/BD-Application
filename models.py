import sqlite3
from datetime import datetime

def criar_banco():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # Tabela Clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela Pedidos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        produto TEXT NOT NULL,
        valor REAL NOT NULL,
        data_pedido TEXT DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
    ''')
    
    # Tabela de logs
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
    
    # Trigger para log de inserção de clientes
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS log_insert_cliente
    AFTER INSERT ON clientes
    BEGIN
        INSERT INTO logs (tabela, operacao, id_registro, data_hora)
        VALUES ('clientes', 'INSERT', NEW.id, datetime('now', 'localtime'));
    END;
    ''')
    
    conn.commit()
    conn.close()

def escrever_log(mensagem):
    with open('logs.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensagem}\n")