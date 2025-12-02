import sqlite3
from typing import List
from midia import Midia, TipoMidia, StatusVisualizacao
from filme import Filme
from serie import Serie
from temporada import Temporada
from episodio import Episodio
# NOVAS IMPORTAÇÕES NECESSÁRIAS
import os
from pathlib import Path


class Catalogo:
    def __init__(self):
        self._midias: List[Midia] = []

        # --- MUDANÇA CRÍTICA AQUI ---
        # Constrói o caminho absoluto para 'dados.db'
        # Isso garante que ele encontre o arquivo, não importa de onde você execute main.py
        base_dir = Path(__file__).parent.parent if 'code/midia_app' in str(
            Path(__file__)) else Path(__file__).parent
        db_path = base_dir / 'dados.db'
        db_path_str = str(db_path)
        # --- FIM DA MUDANÇA CRÍTICA ---

        print("DEBUG: 1. Tentando conectar ao banco de dados...")
        try:
            # Conecta usando o caminho absoluto
            self.conn = sqlite3.connect(db_path_str)
            self.cursor = self.conn.cursor()
            print("DEBUG: 2. Conexão estabelecida com sucesso.")
        except Exception as e:
            print(f"ERRO CRÍTICO NA CONEXÃO: {e}")
            return

        self.inicializar_db()
        print("DEBUG: 3. DB inicializado/verificado.")

        self.carregar_midias()
        print("DEBUG: 4. Mídias carregadas com sucesso.")

    @property
    def midias(self):
        return self._midias

    def fechar_conexao(self):
        self.conn.close()

    def inicializar_db(self):
        # Tabela Midia (para Filmes e Séries)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Midia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                genero TEXT,
                ano_lancamento INTEGER,
                elenco TEXT,
                duracao_minutos INTEGER,
                tipo_midia TEXT NOT NULL,
                status_visualizacao TEXT NOT NULL,
                avaliacao REAL DEFAULT 0.0
            );
        """)

        # Tabela Temporada (relacionada a Séries)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Temporada (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serie_id INTEGER,
                numero INTEGER NOT NULL,
                nome TEXT,
                FOREIGN KEY (serie_id) REFERENCES Midia (id)
            );
        """)

        # Tabela Episodio (relacionada a Temporadas)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Episodio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temporada_id INTEGER,
                numero INTEGER NOT NULL,
                nome TEXT,
                duracao_minutos INTEGER,
                FOREIGN KEY (temporada_id) REFERENCES Temporada (id)
            );
        """)
        self.conn.commit()

    def carregar_midias(self):
        self._midias = []

        filmes_db = self.cursor.execute(
            "SELECT * FROM Midia WHERE tipo_midia = 'FILME'").fetchall()
        for id_midia, titulo, genero, ano, elenco, duracao, tipo, status_nome, avaliacao in filmes_db:
            status = StatusVisualizacao[status_nome]
            midia = Filme(titulo, genero, ano, duracao, elenco.split(
                ','), status=status, avaliacao=avaliacao)
            midia._id = id_midia
            self._midias.append(midia)

        series_db = self.cursor.execute(
            "SELECT * FROM Midia WHERE tipo_midia = 'SERIE'").fetchall()
        for id_midia, titulo, genero, ano, elenco, duracao, tipo, status_nome, avaliacao in series_db:
            status = StatusVisualizacao[status_nome]
            serie = Serie(titulo, genero, ano, elenco.split(
                ','), status=status, avaliacao=avaliacao)
            serie._id = id_midia

            temporadas_db = self.cursor.execute(
                "SELECT id, numero, nome FROM Temporada WHERE serie_id = ?", (id_midia,)).fetchall()
            for id_temp, num_temp, nome_temp in temporadas_db:
                temp_obj = Temporada(num_temp, nome_temp)
                temp_obj._id = id_temp

                episodios_db = self.cursor.execute(
                    "SELECT numero, nome, duracao_minutos FROM Episodio WHERE temporada_id = ?", (id_temp,)).fetchall()
                for num_ep, nome_ep, duracao_ep in episodios_db:
                    ep_obj = Episodio(num_ep, nome_ep, duracao_ep)
                    temp_obj.adicionar_episodio(ep_obj)

                serie.temporadas.append(temp_obj)

            self._midias.append(serie)

    def adicionar_midia(self, midia: Midia):
        if midia.tipo == TipoMidia.FILME:
            self.cursor.execute("""
                INSERT INTO Midia (titulo, genero, ano_lancamento, elenco, duracao_minutos, tipo_midia, status_visualizacao, avaliacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (midia.titulo, midia.genero, midia.ano_lancamento, ",".join(midia.elenco), midia.duracao_minutos, midia.tipo.name, midia.status_visualizacao.name, midia.avaliacao))
            midia._id = self.cursor.lastrowid

        elif midia.tipo == TipoMidia.SERIE:
            self.cursor.execute("""
                INSERT INTO Midia (titulo, genero, ano_lancamento, elenco, tipo_midia, status_visualizacao, avaliacao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (midia.titulo, midia.genero, midia.ano_lancamento, ",".join(midia.elenco), midia.tipo.name, midia.status_visualizacao.name, midia.avaliacao))
            midia._id = self.cursor.lastrowid

            for temporada in midia.temporadas:
                self.cursor.execute("""
                    INSERT INTO Temporada (serie_id, numero, nome)
                    VALUES (?, ?, ?)
                """, (midia._id, temporada.numero, temporada.nome))
                temporada._id = self.cursor.lastrowid

                for episodio in temporada.episodios:
                    self.cursor.execute("""
                        INSERT INTO Episodio (temporada_id, numero, nome, duracao_minutos)
                        VALUES (?, ?, ?, ?)
                    """, (temporada._id, episodio.numero, episodio.nome, episodio.duracao_minutos))

        self.conn.commit()
