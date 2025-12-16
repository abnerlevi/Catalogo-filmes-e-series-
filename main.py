import sys
from typing import List, Union


from midia import StatusVisualizacao, TipoMidia, Temporada, Episodio, Midia
from midia_concreta import Filme, Serie
from catalogo import Catalogo
from pathlib import Path


DB_PATH = Path("dados.db")

try:

    catalogo = Catalogo(db_path=DB_PATH)
except Exception as e:
    print(f"Não foi possível inicializar o Catálogo: {e}")
    sys.exit(1)


def limpar_tela():

    print("\n" * 5)


def input_limpo(prompt: str) -> str:

    return input(prompt).strip()


def obter_dados_base():

    titulo = input_limpo("Título: ")
    genero = input_limpo("Gênero: ")
    while True:
        try:
            ano = int(input_limpo("Ano de Lançamento (YYYY): "))
            if 1888 <= ano <= 2100:
                break
            else:
                print("Ano inválido. Use um formato YYYY razoável.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    elenco_str = input_limpo(
        "Elenco Principal (separado por vírgulas, ex: Ator A, Ator B): ")
    elenco = [a.strip() for a in elenco_str.split(',') if a.strip()]

    return titulo, genero, ano, elenco


def menu_adicionar_midia():

    limpar_tela()
    print("--- ADICIONAR NOVA MÍDIA ---")
    print("1. Adicionar Filme")
    print("2. Adicionar Série")
    print("0. Voltar")
    escolha = input_limpo("Escolha uma opção: ")

    if escolha == '1':
        titulo, genero, ano, elenco = obter_dados_base()
        while True:
            try:
                duracao = int(input_limpo("Duração (minutos): "))
                if duracao > 0:
                    break
                else:
                    print("Duração deve ser um número positivo.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")

        filme = Filme(titulo, genero, ano, duracao, elenco)
        catalogo.adicionar_midia(filme)
        print(
            f"\n[SUCESSO] Filme '{filme.titulo}' adicionado ao catálogo com ID {filme.id}.\n")

    elif escolha == '2':
        titulo, genero, ano, elenco = obter_dados_base()

        serie = Serie(titulo, genero, ano, elenco)

        temp1 = Temporada(1, "Primeira Temporada")
        serie.adicionar_temporada(temp1)

        catalogo.adicionar_midia(serie)
        print(
            f"\n[SUCESSO] Série '{serie.titulo}' adicionada ao catálogo com ID {serie.id} (T1 criada).\n")

    elif escolha == '0':
        return
    else:
        print("Opção inválida.")


def exibir_midias(midias_list: List[Midia]):

    if not midias_list:
        print("\nO catálogo está vazio ou não foram encontrados resultados.\n")
        return

    print("\n--- CATÁLOGO DE MÍDIAS ---\n")
    for midia in midias_list:
        print(f"ID: {midia.id} | {midia.tipo.value}")
        print(midia)

        print(f"Elenco: {', '.join(midia.elenco) if midia.elenco else 'N/A'}")

        if midia.tipo == TipoMidia.SERIE:
            serie = midia
            print("\nTemporadas:")
            if not serie.temporadas:
                print("    Nenhuma temporada cadastrada.")

            for temporada in sorted(serie.temporadas, key=lambda t: t.numero):
                total_eps = len(temporada.episodios)
                print(
                    f"    - T{temporada.numero}: {temporada.titulo} (ID: {temporada.id}, {total_eps} episódios)")

                for episodio in sorted(temporada.episodios, key=lambda e: e.numero):
                    print(
                        f"        -> E{episodio.numero}: {episodio.nome} ({episodio.duracao_minutos} min)")
        print("-" * 60)
    print()


def menu_atualizar_status_avaliacao():

    limpar_tela()
    catalogo.carregar_midias()
    exibir_midias(catalogo.midias)

    if not catalogo.midias:
        input("\nPressione ENTER para voltar ao menu principal.")
        return

    while True:
        try:
            midia_id = int(input_limpo(
                "Digite o ID da Mídia para atualizar (ou 0 para voltar): "))
            if midia_id == 0:
                return

            midia = next(
                (m for m in catalogo.midias if m.id == midia_id), None)
            if not midia:
                print("ID não encontrado. Tente novamente.")
                continue
            break
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    print(f"\nAtualizando: {midia.titulo}")

    print("\n--- Status de Visualização ---")
    status_options = {str(i+1): status for i,
                      status in enumerate(StatusVisualizacao)}
    for key, status in status_options.items():
        print(f"{key}. {status.value}")

    while True:
        novo_status_key = input_limpo(
            f"Novo Status (Atual: {midia.status_visualizacao.value}) [1-{len(status_options)}] ou [ENTER] para manter: ")
        if not novo_status_key:
            break
        if novo_status_key in status_options:
            midia.status_visualizacao = status_options[novo_status_key]
            print(
                f"[STATUS] Atualizado para: {midia.status_visualizacao.value}")
            break
        else:
            print("Opção inválida.")

    if midia.status_visualizacao == StatusVisualizacao.CONCLUIDO:
        while True:
            avaliacao_str = input_limpo(
                f"Nova Avaliação (0.0 a 10.0) (Atual: {midia.avaliacao:.1f}) ou [ENTER] para manter: ")
            if not avaliacao_str:
                break
            try:
                nova_avaliacao = float(avaliacao_str)

                midia.avaliacao = nova_avaliacao
                print(f"[AVALIAÇÃO] Atualizada para: {midia.avaliacao:.1f}")
                break
            except ValueError:
                print("Avaliação inválida. Digite um número entre 0.0 e 10.0.")

    catalogo.atualizar_midia(midia)
    print(
        f"\n[SUCESSO] Mídia '{midia.titulo}' atualizada no banco de dados.\n")
    input("Pressione ENTER para voltar ao menu principal.")


def menu_adicionar_episodio():

    limpar_tela()
    series = [m for m in catalogo.midias if m.tipo == TipoMidia.SERIE]

    if not series:
        print("\nNão há Séries cadastradas para adicionar episódios.\n")
        input("Pressione ENTER para voltar ao menu principal.")
        return

    print("--- SÉRIES CADASTRADAS ---")
    for s in series:
        print(f"ID: {s.id} | {s.titulo}")

    while True:
        try:
            serie_id = int(input_limpo(
                "Digite o ID da Série para adicionar o episódio (ou 0 para voltar): "))
            if serie_id == 0:
                return

            serie = next((s for s in series if s.id == serie_id), None)
            if not serie:
                print("ID da Série não encontrado. Tente novamente.")
                continue
            break
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    while True:
        try:
            num_temporada = int(input_limpo(
                "Número da Temporada (se não existir, será criada): "))
            if num_temporada <= 0:
                print("Número da temporada deve ser positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida.")

    while True:
        try:
            num_episodio = int(input_limpo("Número do Episódio: "))
            if num_episodio <= 0:
                print("Número do episódio deve ser positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida.")

    nome_episodio = input_limpo("Nome do Episódio: ")

    while True:
        try:
            duracao = int(input_limpo("Duração do Episódio (minutos): "))
            if duracao > 0:
                break
            else:
                print("Duração deve ser um número positivo.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    try:
        novo_episodio = Episodio(num_episodio, nome_episodio, duracao)

        catalogo.adicionar_episodio_em_temporada(
            serie_id, num_temporada, novo_episodio)
        print(
            f"\n[SUCESSO] Episódio E{num_episodio} na T{num_temporada} de '{serie.titulo}' adicionado.\n")
    except Exception as e:
        print(f"\n[ERRO] Não foi possível adicionar o episódio: {e}")

    input("\nPressione ENTER para voltar ao menu principal.")


def menu_remover_midia():

    limpar_tela()
    catalogo.carregar_midias()
    exibir_midias(catalogo.midias)

    if not catalogo.midias:
        input("\nPressione ENTER para voltar ao menu principal.")
        return

    while True:
        try:
            midia_id = int(input_limpo(
                "Digite o ID da Mídia para REMOVER (ou 0 para voltar): "))
            if midia_id == 0:
                return

            midia_para_remover = next(
                (m for m in catalogo.midias if m.id == midia_id), None)
            if not midia_para_remover:
                print("ID não encontrado. Tente novamente.")
                continue
            break
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    titulo = midia_para_remover.titulo
    tipo = midia_para_remover.tipo

    try:
        # Pede confirmação
        confirmacao = input_limpo(
            f"Tem certeza que deseja remover '{titulo}' ({tipo.value})? Digite 'SIM' para confirmar: ")
        if confirmacao.upper() == 'SIM':
            catalogo.remover_midia(midia_id, tipo)
            print(
                f"\n[SUCESSO] Mídia '{titulo}' ({tipo.value}, ID: {midia_id}) removida permanentemente do catálogo.\n")
        else:
            print("\nOperação cancelada.")
    except Exception as e:
        print(f"\n[ERRO] Não foi possível remover a mídia: {e}")

    input("Pressione ENTER para voltar ao menu principal.")


def menu_relatorio():

    limpar_tela()
    catalogo.carregar_midias()
    stats = catalogo.obter_estatisticas_gerais()

    print("=" * 40)
    print("        RELATÓRIO DO CATÁLOGO")
    print("=" * 40)

    if stats['total'] == 0:
        print("\nO catálogo está vazio. Não há dados para gerar o relatório.")
    else:
        print("\n--- Estatísticas Gerais ---")
        print(f"Total de Mídias Cadastradas: {stats['total']}")
        print(f"  - Filmes: {stats['filmes']}")
        print(f"  - Séries: {stats['series']}")

        print("\n--- Métricas de Visualização ---")
        for status in StatusVisualizacao:

            count = stats['status'].get(status.value, 0)
            print(f"  - {status.value}: {count} itens")

        print("\n--- Avaliação ---")
        if stats['total_avaliacoes'] > 0:
            print(
                f"Avaliação Média Global: {stats['media_avaliacao']:.2f} / 10.0 (baseado em {stats['total_avaliacoes']} avaliações)")
        else:
            print("Nenhuma mídia avaliada ainda.")

        print(
            f"Total de Horas Assistidas: {stats['total_horas_assistidas']:.1f} horas (mídias concluídas)")

        print("\n" + "=" * 40)
        print("    LISTA DE ITENS PENDENTES")
        print("=" * 40)

        pendentes = catalogo.obter_midias_por_status(
            StatusVisualizacao.PENDENTE)
        if pendentes:
            for midia in sorted(pendentes, key=lambda m: m.titulo):
                print(
                    f"  > ID {midia.id} | {midia.tipo.value}: {midia.titulo} ({midia.ano_lancamento})")
        else:
            print("Nenhuma mídia no status 'Pendente'. Bom trabalho!")

        print("\n" + "=" * 40)
        print("    TOP 10 FILMES MAIS BEM AVALIADOS")
        print("=" * 40)

        if stats['top10_filmes']:
            for i, filme in enumerate(stats['top10_filmes'], 1):
                print(
                    f"{i:2d}. {filme.titulo} ({filme.ano_lancamento}) - Nota: {filme.avaliacao:.1f}/10.0")
        else:
            print("Nenhum filme avaliado ainda.")

        print("\n" + "=" * 40)
        print("    TOP 10 SÉRIES MAIS BEM AVALIADAS")
        print("=" * 40)

        if stats['top10_series']:
            for i, serie in enumerate(stats['top10_series'], 1):
                print(
                    f"{i:2d}. {serie.titulo} ({serie.ano_lancamento}) - Nota: {serie.avaliacao:.1f}/10.0")
        else:
            print("Nenhuma série avaliada ainda.")

        print("\n" + "=" * 40)
        print("    DISTRIBUIÇÃO POR GÊNERO")
        print("=" * 40)

        if stats['generos']:
            for genero, counts in sorted(stats['generos'].items()):
                filmes = counts['filmes']
                series = counts['series']
                total = filmes + series
                print(
                    f"  {genero}: {total} itens (Filmes: {filmes}, Séries: {series})")
        else:
            print("Nenhum gênero encontrado.")

    print("\n" + "=" * 40)
    input("Pressione ENTER para voltar ao menu principal.")


def menu_principal():

    while True:
        limpar_tela()
        print("=" * 40)
        print("   CATÁLOGO DE MÍDIAS PESSOAL V2")
        print("=" * 40)
        print("1. Visualizar Catálogo Completo")
        print("2. Adicionar Nova Mídia (Filme/Série)")
        print("3. Atualizar Status e Avaliação de Mídia")
        print("4. Adicionar Episódio a uma Série")
        print("5. Remover Mídia do Catálogo")
        print("6. Gerar Relatório de Estatísticas")
        print("0. Sair e Fechar")
        print("-" * 40)

        escolha = input_limpo("Escolha uma opção: ")

        if escolha == '1':
            limpar_tela()
            catalogo.carregar_midias()
            exibir_midias(catalogo.midias)
            input("Pressione ENTER para voltar ao menu principal.")
        elif escolha == '2':
            menu_adicionar_midia()
        elif escolha == '3':
            menu_atualizar_status_avaliacao()
        elif escolha == '4':
            menu_adicionar_episodio()
        elif escolha == '5':
            menu_remover_midia()
        elif escolha == '6':
            menu_relatorio()
        elif escolha == '0':
            print("\nSalvando alterações e fechando o catálogo. Até mais!")
            catalogo.fechar_conexao()
            break
        else:
            print("\nOpção inválida. Tente novamente.")
            input("Pressione ENTER para continuar.")


if __name__ == "__main__":
    menu_principal()
