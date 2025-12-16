import sqlite3
from typing import List, Optional, Dict, Any, Union
from midia import Midia, TipoMidia, StatusVisualizacao, Temporada, Episodio
from midia_concreta import Filme, Serie
from pathlib import Path


class Catalogo:
    def __init__(self, db_path: Path = Path("dados.db")):
        self.db_path = db_path
        self._midias: List[Midia] = []

        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"ERRO CRÍTICO NA CONEXÃO: {e}")
            self.conn = None
            self.cursor = None
            return

        self.inicializar_db()
        self.carregar_midias()

    @property
    def midias(self):
        return self._midias

    def fechar_conexao(self):

        if getattr(self, "conn", None):
            self.conn.close()

    def inicializar_db(self):

        if not self.conn:
            return

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Midia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                genero TEXT,
                ano_lancamento INTEGER,
                elenco TEXT,
                duracao_minutos INTEGER DEFAULT 0,
                tipo_midia TEXT NOT NULL,
                status_visualizacao TEXT NOT NULL,
                avaliacao REAL DEFAULT 0.0
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Temporada (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serie_id INTEGER,
                numero INTEGER NOT NULL,
                nome TEXT,
                FOREIGN KEY (serie_id) REFERENCES Midia (id)
            );
        """)

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

        if not self.conn:
            self._midias = []
            return

        self._midias = []

        filmes_db = self.cursor.execute(
            "SELECT id, titulo, genero, ano_lancamento, elenco, duracao_minutos, status_visualizacao, avaliacao FROM Midia WHERE tipo_midia = 'FILME'"
        ).fetchall()

        for id_midia, titulo, genero, ano, elenco_str, duracao, status_nome, avaliacao in filmes_db:
            elenco = [ator.strip()
                      for ator in (elenco_str or "").split(',') if ator.strip()]
            status = StatusVisualizacao[status_nome]
            midia = Filme(titulo, genero, ano, duracao, elenco,
                          status=status, avaliacao=avaliacao)
            midia._id = id_midia
            self._midias.append(midia)

        series_db = self.cursor.execute(
            "SELECT id, titulo, genero, ano_lancamento, elenco, status_visualizacao, avaliacao FROM Midia WHERE tipo_midia = 'SERIE'"
        ).fetchall()

        for id_midia, titulo, genero, ano, elenco_str, status_nome, avaliacao in series_db:
            elenco = [ator.strip()
                      for ator in (elenco_str or "").split(',') if ator.strip()]
            status = StatusVisualizacao[status_nome]
            serie = Serie(titulo, genero, ano, elenco,
                          status=status, avaliacao=avaliacao)
            serie._id = id_midia

            temporadas_db = self.cursor.execute(
                "SELECT id, numero, nome FROM Temporada WHERE serie_id = ?", (
                    id_midia,)
            ).fetchall()

            for id_temp, num_temp, nome_temp in temporadas_db:
                temp_obj = Temporada(num_temp, nome_temp)
                temp_obj._id = id_temp

                episodios_db = self.cursor.execute(
                    "SELECT numero, nome, duracao_minutos FROM Episodio WHERE temporada_id = ?", (
                        id_temp,)
                ).fetchall()

                for num_ep, nome_ep, duracao_ep in episodios_db:
                    ep_obj = Episodio(num_ep, nome_ep, duracao_ep)
                    temp_obj.adicionar_episodio(ep_obj)

                serie.temporadas.append(temp_obj)

            self._midias.append(serie)

        self._midias.sort(key=lambda m: m.titulo)

    def adicionar_midia(self, midia: Midia):

        if not self.conn:
            raise RuntimeError("Conexão com DB indisponível.")

        elenco_db = ",".join(midia.elenco) if midia.elenco else ""

        if midia.tipo == TipoMidia.FILME:
            self.cursor.execute("""
                INSERT INTO Midia (titulo, genero, ano_lancamento, elenco, duracao_minutos, tipo_midia, status_visualizacao, avaliacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (midia.titulo, midia.genero, midia.ano_lancamento, elenco_db, midia.duracao_minutos, midia.tipo.name, midia.status_visualizacao.name, midia.avaliacao))
            midia._id = self.cursor.lastrowid

        elif midia.tipo == TipoMidia.SERIE:
            self.cursor.execute("""
                INSERT INTO Midia (titulo, genero, ano_lancamento, elenco, tipo_midia, status_visualizacao, avaliacao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (midia.titulo, midia.genero, midia.ano_lancamento, elenco_db, midia.tipo.name, midia.status_visualizacao.name, midia.avaliacao))
            midia._id = self.cursor.lastrowid

            for temporada in midia.temporadas:
                self.cursor.execute("""
                    INSERT INTO Temporada (serie_id, numero, nome)
                    VALUES (?, ?, ?)
                """, (midia._id, temporada.numero, temporada.titulo))
                temporada._id = self.cursor.lastrowid

                for episodio in temporada.episodios:
                    self.cursor.execute("""
                        INSERT INTO Episodio (temporada_id, numero, nome, duracao_minutos)
                        VALUES (?, ?, ?, ?)
                    """, (temporada._id, episodio.numero, episodio.nome, episodio.duracao_minutos))

        self.conn.commit()
        self._midias.append(midia)

    def atualizar_midia(self, midia: Midia):

        if not self.conn:
            raise RuntimeError("Conexão com DB indisponível.")

        self.cursor.execute("""
            UPDATE Midia 
            SET status_visualizacao = ?, avaliacao = ?
            WHERE id = ?
        """, (midia.status_visualizacao.name, midia.avaliacao, midia._id))
        self.conn.commit()

    def buscar_serie_por_id(self, serie_id: int) -> Optional[Serie]:

        for midia in self._midias:
            if midia._id == serie_id and midia.tipo == TipoMidia.SERIE:
                return midia
        return None

    def adicionar_episodio_em_temporada(self, serie_id: int, num_temporada: int, episodio: Episodio):

        if not self.conn:
            raise RuntimeError("Conexão com DB indisponível.")

        serie = self.buscar_serie_por_id(serie_id)
        if not serie:
            raise ValueError("Série não encontrada no catálogo.")

        temporada_encontrada = next(
            (t for t in serie.temporadas if t.numero == num_temporada), None)
        if not temporada_encontrada:
            raise ValueError(
                f"Temporada {num_temporada} não encontrada na série {serie.titulo}.")

        temporada_encontrada.adicionar_episodio(episodio)

        self.cursor.execute("""
            INSERT INTO Episodio (temporada_id, numero, nome, duracao_minutos)
            VALUES (?, ?, ?, ?)
        """, (temporada_encontrada._id, episodio.numero, episodio.nome, episodio.duracao_minutos))

        self.conn.commit()
        self._midias.sort(key=lambda m: m.titulo)
        print(
            f"Episódio {episodio.numero} adicionado à Temporada {num_temporada} de {serie.titulo}.")

    def remover_midia(self, midia_id: int, tipo_midia: TipoMidia):

        if not self.conn:
            raise RuntimeError("Conexão com DB indisponível.")

        if tipo_midia == TipoMidia.SERIE:
            temporada_ids = self.cursor.execute(
                "SELECT id FROM Temporada WHERE serie_id = ?", (midia_id,)
            ).fetchall()
            if temporada_ids:
                for temp_id in [t[0] for t in temporada_ids]:
                    self.cursor.execute(
                        "DELETE FROM Episodio WHERE temporada_id = ?", (temp_id,))

            self.cursor.execute(
                "DELETE FROM Temporada WHERE serie_id = ?", (midia_id,))

        self.cursor.execute("DELETE FROM Midia WHERE id = ?", (midia_id,))
        self.conn.commit()

        self._midias = [m for m in self._midias if m._id != midia_id]

    def obter_estatisticas_gerais(self) -> Dict[str, Union[int, float, Dict[str, int]]]:

        total = len(self._midias)

        stats: Dict[str, Any] = {
            'total': total,
            'filmes': 0,
            'series': 0,
            'status': {s.value: 0 for s in StatusVisualizacao},
            'media_avaliacao': 0.0,
            'total_avaliacoes': 0,
            'total_horas_assistidas': 0.0,
            'top10_filmes': [],
            'top10_series': [],
            'generos': {}
        }

        avaliacoes = []
        total_minutos_assistidos = 0
        for midia in self._midias:
            if midia.tipo == TipoMidia.FILME:
                stats['filmes'] += 1
            elif midia.tipo == TipoMidia.SERIE:
                stats['series'] += 1

            # Contagem por gênero
            genero = midia.genero
            if genero not in stats['generos']:
                stats['generos'][genero] = {'filmes': 0, 'series': 0}
            if midia.tipo == TipoMidia.FILME:
                stats['generos'][genero]['filmes'] += 1
            else:
                stats['generos'][genero]['series'] += 1

            stats['status'][midia.status_visualizacao.value] += 1

            if midia.status_visualizacao == StatusVisualizacao.CONCLUIDO:
                if midia.tipo == TipoMidia.FILME:
                    total_minutos_assistidos += midia.duracao_minutos
                elif midia.tipo == TipoMidia.SERIE:
                    total_minutos_assistidos += midia.duracao_total

            if midia.avaliacao is not None:
                avaliacoes.append(midia.avaliacao)
                stats['total_avaliacoes'] += 1

        if avaliacoes:
            stats['media_avaliacao'] = round(
                sum(avaliacoes) / len(avaliacoes), 2)

        stats['total_horas_assistidas'] = round(
            total_minutos_assistidos / 60, 1)

        filmes_avaliados = [m for m in self._midias if m.tipo ==
                            TipoMidia.FILME and m.avaliacao > 0]
        series_avaliadas = [m for m in self._midias if m.tipo ==
                            TipoMidia.SERIE and m.avaliacao > 0]

        stats['top10_filmes'] = sorted(
            filmes_avaliados, key=lambda m: m.avaliacao, reverse=True)[:10]
        stats['top10_series'] = sorted(
            series_avaliadas, key=lambda m: m.avaliacao, reverse=True)[:10]

        return stats

    def obter_midias_por_status(self, status: StatusVisualizacao) -> List[Midia]:

        return [midia for midia in self._midias if midia.status_visualizacao == status]
