from episodio import Episodio

from midia import Midia, TipoMidia, StatusVisualizacao
from temporada import Temporada


class Serie(Midia):

    def __init__(self, titulo: str, genero: str, ano: int, duracao_media_episodio: int,
                 classificacao: str, elenco: list, status: StatusVisualizacao):

        super().__init__(titulo, TipoMidia.SERIE, genero, ano, duracao_media_episodio,
                         classificacao, elenco, status)

        self.temporadas: list[Temporada] = []

    def adicionar_temporada(self, temporada: Temporada):
        if not isinstance(temporada, Temporada):
            raise TypeError(
                "Só é possível adicionar objetos do tipo Temporada.")
        self.temporadas.append(temporada)

    def __len__(self) -> int:

        total = 0
        for temporada in self.temporadas:
            total += temporada.total_episodios()
        return total

    def __repr__(self) -> str:
        return f"Serie(titulo='{self.titulo}', temporadas={len(self.temporadas)})"
