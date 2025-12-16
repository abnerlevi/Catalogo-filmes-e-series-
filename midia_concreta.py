from typing import List, Optional
from midia import Midia, TipoMidia, StatusVisualizacao, Temporada


class Filme(Midia):
    """Representa um Filme, estendendo a classe base Midia."""

    def __init__(self,
                 titulo: str,
                 genero: str,
                 ano_lancamento: int,
                 duracao_minutos: int,
                 elenco: List[str],
                 status: StatusVisualizacao = StatusVisualizacao.PENDENTE,
                 avaliacao: float = 0.0,
                 id: Optional[int] = None):
        super().__init__(titulo, genero, ano_lancamento,
                         elenco, TipoMidia.FILME, id, status, avaliacao)
        self._duracao_minutos = None
        self.duracao_minutos = duracao_minutos

    @property
    def duracao_minutos(self) -> int:
        """Retorna a duração do filme em minutos."""
        return self._duracao_minutos

    @duracao_minutos.setter
    def duracao_minutos(self, nova_duracao: int):
        """Define a duração do filme com validação."""
        if not isinstance(nova_duracao, (int, float)) or nova_duracao <= 0:
            raise ValueError("A duração deve ser um número positivo.")
        self._duracao_minutos = int(nova_duracao)

    def __str__(self):
        """Representação em string do Filme."""
        base_str = super().__str__()
        return f"{base_str}\n  Duração: {self.duracao_minutos} min"


class Serie(Midia):
    """Representa uma Série, estendendo a classe base Midia e gerenciando Temporadas."""

    def __init__(self,
                 titulo: str,
                 genero: str,
                 ano_lancamento: int,
                 elenco: List[str],
                 status: StatusVisualizacao = StatusVisualizacao.PENDENTE,
                 avaliacao: float = 0.0,
                 id: Optional[int] = None):
        super().__init__(titulo, genero, ano_lancamento,
                         elenco, TipoMidia.SERIE, id, status, avaliacao)
        self.temporadas: List[Temporada] = []

    def adicionar_temporada(self, temporada: Temporada):
        """Adiciona uma temporada à lista da série."""
        if not isinstance(temporada, Temporada):
            raise TypeError(
                "Apenas objetos da classe Temporada podem ser adicionados.")
        self.temporadas.append(temporada)
        self.temporadas.sort(key=lambda t: t.numero)

    @property
    def duracao_total(self) -> int:
        """Retorna a duração total de todos os episódios."""
        total = 0
        for temporada in self.temporadas:
            for episodio in temporada.episodios:
                total += episodio.duracao_minutos
        return total

    def __str__(self):
        """Representação em string da Série, incluindo contagem de temporadas/episódios."""
        base_str = super().__str__()
        total_episodios = sum(len(t.episodios) for t in self.temporadas)

        info_str = (f"  Temporadas: {len(self.temporadas)} | "
                    f"Episódios Totais: {total_episodios} | "
                    f"Duração Total: {self.duracao_total} min")

        return f"{base_str.strip()}\n{info_str}"
