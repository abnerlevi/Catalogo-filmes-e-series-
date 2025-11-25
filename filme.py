from midia import Midia, TipoMidia, StatusVisualizacao


class Filme(Midia):

    def __init__(self, titulo: str, genero: str, ano: int, duracao: int,
                 classificacao: str, elenco: list, status: StatusVisualizacao):

        super().__init__(titulo, TipoMidia.FILME, genero, ano, duracao,
                         classificacao, elenco, status)

    def __repr__(self) -> str:

        return f"Filme(titulo='{self.titulo}', ano={self.ano})"
