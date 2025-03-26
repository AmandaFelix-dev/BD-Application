from database import Database
from models import criar_banco

def mostrar_menu():
    print("\n--- SISTEMA DE CLIENTES E PEDIDOS ---")
    print("1. Inserir cliente")
    print("2. Atualizar cliente")
    print("3. Deletar cliente")
    print("4. Listar clientes")
    print("5. Inserir pedido")
    print("6. Listar pedidos")
    print("7. Ver logs de inserção (trigger)")
    print("0. Sair")

def main():
    criar_banco()
    db = Database()
    
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome do cliente: ")
            email = input("Email do cliente: ")
            if db.inserir_cliente(nome, email):
                print("Cliente inserido com sucesso!")
            else:
                print("Erro ao inserir cliente. Email pode já existir.")
        
        elif opcao == "2":
            id = input("ID do cliente a atualizar: ")
            nome = input("Novo nome (deixe em branco para não alterar): ")
            email = input("Novo email (deixe em branco para não alterar): ")
            if db.atualizar_cliente(id, nome if nome else None, email if email else None):
                print("Cliente atualizado com sucesso!")
            else:
                print("Erro ao atualizar cliente.")
        
        elif opcao == "3":
            id = input("ID do cliente a deletar: ")
            if db.deletar_cliente(id):
                print("Cliente deletado com sucesso!")
            else:
                print("Erro ao deletar cliente.")
        
        elif opcao == "4":
            clientes = db.listar_clientes()
            print("\n--- CLIENTES CADASTRADOS ---")
            for cliente in clientes:
                print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Email: {cliente[2]} | Cadastro: {cliente[3]}")
        
        elif opcao == "5":
            cliente_id = input("ID do cliente: ")
            produto = input("Nome do produto: ")
            valor = float(input("Valor do produto: "))
            if db.inserir_pedido(cliente_id, produto, valor):
                print("Pedido inserido com sucesso!")
            else:
                print("Erro ao inserir pedido.")
        
        elif opcao == "6":
            pedidos = db.listar_pedidos()
            print("\n--- PEDIDOS REGISTRADOS ---")
            for pedido in pedidos:
                print(f"ID: {pedido[0]} | Cliente: {pedido[1]} | Produto: {pedido[2]} | Valor: R${pedido[3]:.2f} | Data: {pedido[4]}")
        
        elif opcao == "7":
            logs = db.listar_logs_trigger()
            print("\n--- LOGS DE INSERÇÃO (TRIGGER) ---")
            for log in logs:
                print(f"ID: {log[0]} | Tabela: {log[1]} | Operação: {log[2]} | ID Registro: {log[3]} | Data: {log[4]}")
        
        elif opcao == "0":
            db.close()
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()