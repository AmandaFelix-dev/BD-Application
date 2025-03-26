from database import HQDatabase
from models import criar_banco, escrever_log

def mostrar_menu():
    print("\n--- CATÁLOGO DE HQs ---")
    print("1. 📋 Gerenciar Editoras")
    print("2. 🎬 Gerenciar Séries")
    print("3. 🗃️  Gerenciar Edições")
    print("4. 📊 Relatórios")
    print("0. 🚀 Sair")

def menu_editoras(db):
    while True:
        print("\n--- EDITORAS ---")
        print("1. 📌 Cadastrar nova editora")
        print("2. 📄 Listar todas as editoras")
        print("3. ✏️  Atualizar editora")
        print("4. ❌ Excluir editora")
        print("0. ↩️  Voltar")
        
        opcao = input("✍️ 🤓  Escolha: ")
        
        if opcao == "1":
            nome = input("Nome da editora: ")
            pais = input("País de origem (opcional): ")
            if db.inserir_editora(nome, pais if pais else None):
                print("✅ Editora cadastrada com sucesso!")
        
        elif opcao == "2":
            editoras = db.listar_editoras()
            print("\n--- EDITORAS CADASTRADAS ---")
            for ed in editoras:
                print(f"ID: {ed[0]} | Nome: {ed[1]} | País: {ed[2] or 'Não informado'}")
        
        elif opcao == "3":
            editoras = db.listar_editoras()
            if not editoras:
                print("Nenhuma editora cadastrada!")
                continue
                
            print("\nEditoras disponíveis:")
            for ed in editoras:
                print(f"{ed[0]} - {ed[1]}")
                
            id = input("ID da editora a atualizar: ")
            if not id.isdigit():
                print("ID inválido!")
                continue
                
            editora = db.buscar_editora(int(id))
            if not editora:
                print("Editora não encontrada!")
                continue
                
            print(f"\nEditando editora: {editora[1]}")
            novo_nome = input(f"Novo nome [{editora[1]}]: ") or editora[1]
            novo_pais = input(f"Novo país [{editora[2] or 'Não informado'}]: ") or editora[2]
            
            if db.atualizar_editora(id, novo_nome, novo_pais):
                print("✅ Editora atualizada com sucesso!")
        
        elif opcao == "4":
            editoras = db.listar_editoras()
            if not editoras:
                print("Nenhuma editora cadastrada!")
                continue
                
            print("\nEditoras disponíveis:")
            for ed in editoras:
                print(f"{ed[0]} - {ed[1]}")
                
            id = input("ID da editora a excluir: ")
            if not id.isdigit():
                print("ID inválido!")
                continue
                
            if db.excluir_editora(int(id)):
                print("✅ Editora excluída com sucesso!")
            else:
                print("❌ Não foi possível excluir (possui séries associadas)")
        
        elif opcao == "0":
            break
        
        else:
            print("❌ Opção inválida!")

def menu_series(db):
    while True:
        print("\n--- SÉRIES ---")
        print("1. 📌 Cadastrar nova série")
        print("2. 📄 Listar séries por editora")
        print("3. 📄 Listar todas as séries")
        print("4. ✏️  Atualizar série")
        print("5. ❌ Excluir série")
        print("0. ↩️  Voltar")
        
        opcao = input("✍️ 🤓 Escolha: ")
        
        if opcao == "1":
            titulo = input("Título da série: ")
            editoras = db.listar_editoras()
            if not editoras:
                print("Nenhuma editora cadastrada! Cadastre uma editora primeiro.")
                continue
                
            print("\nEditoras disponíveis:")
            for ed in editoras:
                print(f"{ed[0]} - {ed[1]}")
                
            editora_id = input("ID da editora: ")
            if not editora_id.isdigit():
                print("ID inválido!")
                continue
                
            ano = input("Ano de lançamento (opcional): ")
            status = input("Status (Ativa/Concluída/Cancelada) [Ativa]: ") or "Ativa"
            
            if db.inserir_serie(titulo, editora_id, ano if ano else None, status):
                print("✅ Série cadastrada com sucesso!")
        
        elif opcao == "2":
            editoras = db.listar_editoras()
            if not editoras:
                print("Nenhuma editora cadastrada!")
                continue
                
            print("\nEditoras disponíveis:")
            for ed in editoras:
                print(f"{ed[0]} - {ed[1]}")
                
            editora_id = input("ID da editora para filtrar: ")
            if not editora_id.isdigit():
                print("ID inválido!")
                continue
                
            series = db.listar_series(editora_id)
            print("\n--- SÉRIES ---")
            for serie in series:
                print(f"ID: {serie[0]} | Título: {serie[1]} | Editora: {serie[2]} | Ano: {serie[3] or 'N/I'} | Status: {serie[4]}")
        
        elif opcao == "3":
            series = db.listar_series()
            print("\n--- TODAS AS SÉRIES ---")
            for serie in series:
                print(f"ID: {serie[0]} | Título: {serie[1]} | Editora: {serie[2]} | Ano: {serie[3] or 'N/I'} | Status: {serie[4]}")
        
        elif opcao == "4":
            series = db.listar_series()
            if not series:
                print("Nenhuma série cadastrada!")
                continue
                
            print("\nSéries disponíveis:")
            for serie in series:
                print(f"{serie[0]} - {serie[1]}")
                
            id = input("ID da série a atualizar: ")
            if not id.isdigit():
                print("ID inválido!")
                continue
                
            serie = db.buscar_serie(id)
            if not serie:
                print("Série não encontrada!")
                continue
                
            print(f"\nEditando série: {serie[1]}")
            novo_titulo = input(f"Novo título [{serie[1]}]: ") or serie[1]
            
            editoras = db.listar_editoras()
            print("\nEditoras disponíveis:")
            for ed in editoras:
                print(f"{ed[0]} - {ed[1]}")
            nova_editora = input(f"Nova editora ID [{serie[2]}]: ") or serie[2]
            
            novo_ano = input(f"Novo ano [{serie[3] or 'N/I'}]: ") or serie[3]
            novo_status = input(f"Novo status [{serie[4]}]: ") or serie[4]
            
            if db.atualizar_serie(id, novo_titulo, nova_editora, novo_ano, novo_status):
                print("✅ Série atualizada com sucesso!")
        
        elif opcao == "5":
            series = db.listar_series()
            if not series:
                print("Nenhuma série cadastrada!")
                continue
                
            print("\nSéries disponíveis:")
            for serie in series:
                print(f"{serie[0]} - {serie[1]}")
                
            id = input("ID da série a excluir: ")
            if not id.isdigit():
                print("ID inválido!")
                continue
                
            if db.excluir_serie(int(id)):
                print("✅ Série excluída com sucesso!")
            else:
                print("❌ Não foi possível excluir (possui edições associadas)")
        
        elif opcao == "0":
            break
        
        else:
            print("❌ Opção inválida!")

def menu_edicoes(db):
    while True:
        print("\n--- EDIÇÕES ---")
        print("1. 📌 Cadastrar nova edição")
        print("2. 📄 Listar edições por série")
        print("3. 📄 Listar todas as edições")
        print("4. ✏️  Atualizar edição")
        print("5. 📦 Atualizar estoque")
        print("6. ❌ Excluir edição")
        print("0. ↩️  Voltar")
        
        opcao = input("✍️ 🤓 Escolha: ")
        
        if opcao == "1":
            series = db.listar_series()
            if not series:
                print("Nenhuma série cadastrada! Cadastre uma série primeiro.")
                continue
                
            print("\nSéries disponíveis:")
            for serie in series:
                print(f"{serie[0]} - {serie[1]}")
                
            serie_id = input("ID da série: ")
            if not serie_id.isdigit():
                print("ID inválido!")
                continue
                
            numero = input("Número da edição: ")
            if not numero.isdigit():
                print("Número inválido!")
                continue
                
            titulo_edicao = input("Título da edição (opcional): ")
            data_publicacao = input("Data de publicação (AAAA-MM-DD, opcional): ")
            preco_original = input("Preço original (opcional): ")
            preco_atual = input("Preço atual (opcional): ")
            quantidade = input("Quantidade em estoque [0]: ") or "0"
            
            try:
                preco_original = float(preco_original) if preco_original else None
                preco_atual = float(preco_atual) if preco_atual else None
                quantidade = int(quantidade)
            except ValueError:
                print("Valor inválido para preço ou quantidade!")
                continue
                
            if db.inserir_edicao(serie_id, numero, titulo_edicao or None, 
                                data_publicacao or None, preco_original, 
                                preco_atual, quantidade):
                print("✅ Edição cadastrada com sucesso!")
        
        elif opcao == "2":
            series = db.listar_series()
            if not series:
                print("Nenhuma série cadastrada!")
                continue
                
            print("\nSéries disponíveis:")
            for serie in series:
                print(f"{serie[0]} - {serie[1]}")
                
            serie_id = input("ID da série para filtrar: ")
            if not serie_id.isdigit():
                print("ID inválido!")
                continue
                
            edicoes = db.listar_edicoes(serie_id)
            print("\n--- EDIÇÕES ---")
            for ed in edicoes:
                print(f"ID: {ed[0]} | Nº: {ed[1]} | Título: {ed[2] or 'N/I'} | "
                      f"Publicação: {ed[3] or 'N/I'} | Preço: R${ed[4] or '0.00'} | "
                      f"Estoque: {ed[5]}")
        
        elif opcao == "3":
            edicoes = db.listar_edicoes()
            print("\n--- TODAS AS EDIÇÕES ---")
            for ed in edicoes:
                print(f"ID: {ed[0]} | Nº: {ed[1]} | Série: {ed[2]} | "
                      f"Título: {ed[3] or 'N/I'} | Preço: R${ed[4] or '0.00'} | "
                      f"Estoque: {ed[5]}")
        
        elif opcao == "4":
            edicoes = db.listar_edicoes()
            if not edicoes:
                print("Nenhuma edição cadastrada!")
                continue
                
            print("\nEdições disponíveis:")
            for ed in edicoes:
                print(f"{ed[0]} - {ed[2]} #{ed[1]}")
                
            id = input("ID da edição a atualizar: ")
            if not id.isdigit():
                print("ID inválido!")
                continue
                
            edicao = db.buscar_edicao(id)
            if not edicao:
                print("Edição não encontrada!")
                continue
                
            print(f"\nEditando edição #{edicao[1]} da série {edicao[7]}")
            novo_numero = input(f"Novo número [{edicao[1]}]: ") or edicao[1]
            novo_titulo = input(f"Novo título [{edicao[2] or 'N/I'}]: ") or edicao[2]
            nova_data = input(f"Nova data (AAAA-MM-DD) [{edicao[3] or 'N/I'}]: ") or edicao[3]
            novo_preco_original = input(f"Novo preço original [{edicao[4] or 'N/I'}]: ") or edicao[4]
            novo_preco_atual = input(f"Novo preço atual [{edicao[5] or 'N/I'}]: ") or edicao[5]
            
            try:
                novo_numero = int(novo_numero)
                novo_preco_original = float(novo_preco_original) if novo_preco_original else None
                novo_preco_atual = float(novo_preco_atual) if novo_preco_atual else None
            except ValueError:
                print("Valor inválido para número ou preço!")
                continue
                
            if db.atualizar_edicao(id, numero=novo_numero, titulo_edicao=novo_titulo,
                                  data_publicacao=nova_data, preco_original=novo_preco_original,
                                  preco_atual=novo_preco_atual):
                print("✅ Edição atualizada com sucesso!")
        
        elif opcao == "5":
            edicoes = db.listar_edicoes()
            if not edicoes:
                print("Nenhuma edição cadastrada!")
                continue
                
            print("\nEdições disponíveis:")
            for ed in edicoes:
                print(f"{ed[0]} - {ed[2]} #{ed[1]} (Estoque: {ed[5]})")
                
            id = input("ID da edição para atualizar estoque: ")
            if not id.isdigit():
                print("ID inválido!")
                continue
                
            edicao = db.buscar_edicao(id)
            if not edicao:
                print("Edição não encontrada!")
                continue
                
            print(f"\nEdição #{edicao[1]} - {edicao[7]}")
            print(f"Estoque atual: {edicao[6]}")
            nova_quantidade = input("Nova quantidade: ")
            
            try:
                nova_quantidade = int(nova_quantidade)
            except ValueError:
                print("Quantidade inválida!")
                continue
                
            if db.atualizar_edicao(id, quantidade_estoque=nova_quantidade):
                print("✅ Estoque atualizado com sucesso!")
        
        elif opcao == "6":
            edicoes = db.listar_edicoes()
            if not edicoes:
                print("Nenhuma edição cadastrada!")
                continue
                
            print("\nEdições disponíveis:")
            for ed in edicoes:
                print(f"{ed[0]} - {ed[2]} #{ed[1]}")
                
            id = input("ID da edição a excluir: ")
            if not id.isdigit():
                print("ID inválido!")
                continue
                
            if db.excluir_edicao(int(id)):
                print("✅ Edição excluída com sucesso!")
        
        elif opcao == "0":
            break
        
        else:
            print("❌ Opção inválida!")

def menu_relatorios(db):
    while True:
        print("\n--- RELATÓRIOS ---")
        print("1. 📉 Estoque baixo")
        print("2. 📊 Séries por status")
        print("3. 📜 Histórico de logs")
        print("0. ↩️  Voltar")
        
        opcao = input("✍️ 🤓 Escolha: ")
        
        if opcao == "1":
            limite = input("Limite para estoque baixo [5]: ") or "5"
            try:
                limite = int(limite)
            except ValueError:
                print("Valor inválido!")
                continue
                
            estoque_baixo = db.estoque_baixo(limite)
            print("\n--- EDIÇÕES COM ESTOQUE BAIXO ---")
            for ed in estoque_baixo:
                print(f"ID: {ed[0]} | Nº: {ed[1]} | Série: {ed[2]} | Estoque: {ed[3]}")
        
        elif opcao == "2":
            series_status = db.series_por_status()
            print("\n--- SÉRIES POR STATUS ---")
            for status in series_status:
                print(f"{status[0]}: {status[1]}")
        
        elif opcao == "3":
            logs = db.historico_logs()
            print("\n--- ÚLTIMOS REGISTROS DE LOG ---")
            for log in logs:
                print(f"{log[0]} | {log[1]}.{log[2]} ID {log[3]} | {log[4] or ''}")
        
        elif opcao == "0":
            break
        
        else:
            print("❌ Opção inválida!")

def main():
    criar_banco()
    db = HQDatabase()
    
    while True:
        mostrar_menu()
        opcao = input("😎 Escolha uma opção: ")
        
        if opcao == "1":
            menu_editoras(db)
        elif opcao == "2":
            menu_series(db)
        elif opcao == "3":
            menu_edicoes(db)
        elif opcao == "4":
            menu_relatorios(db)
        elif opcao == "0":
            db.close()
            print("🤖 Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()