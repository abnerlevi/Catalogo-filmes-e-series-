from enum import Enum
from datetime import date


class TipoMidia(Enum):

    FILME = "FILME"
    SERIE = "SERIE"


class StatusVisualizacao(Enum):

    NAO_ASSISTIDO = "NÃO ASSISTIDO"
    ASSISTINDO = "ASSISTINDO"
    ASSISTIDO = "ASSISTIDO"


class Midia:

    def __init__(self, titulo: str, tipo: TipoMidia, genero: str, ano: int,
                 duracao: int, classificacao: str, elenco: list, status: StatusVisualizacao):

        self._titulo = None
        self._ano = None
        self._duracao = None
        self._nota_media = 0.0  # Inicializa

        self.titulo = titulo
        self.ano = ano
        self.duracao = duracao

        self._tipo = tipo
        self.genero = genero
        self.classificacao = classificacao
        self.elenco = elenco
        self._status = status

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, novo_titulo: str):
        if not novo_titulo or novo_titulo.strip() == "":
            raise ValueError("O título da mídia não pode ser vazio.")
        self._titulo = novo_titulo.strip()

    @property
    def ano(self):
        return self._ano

    @ano.setter
    def ano(self, novo_ano: int):
        # Validação básica
        if not isinstance(novo_ano, int) or novo_ano < 1900 or novo_ano > date.today().year + 5:
            raise ValueError(f"O ano de lançamento ({novo_ano}) é inválido.")
        self._ano = novo_ano

    @property
    def duracao(self):
        return self._duracao

    @duracao.setter
    def duracao(self, nova_duracao: int):
        if not isinstance(nova_duracao, int) or nova_duracao <= 0:
            raise ValueError(
                "A duração deve ser um valor inteiro positivo em minutos.")
        self._duracao = nova_duracao

    @property
    def nota_media(self):
        return self._nota_media

    @nota_media.setter
    def nota_media(self, nova_nota: float):
        if not (0 <= nova_nota <= 10):
            raise ValueError("A nota deve ser um número entre 0 e 10.")
        self._nota_media = nova_nota

    def __str__(self) -> str:

        return f"{self._tipo.value}: {self._titulo} ({self._ano}) - Status: {self._status.value}"

    def __eq__(self, outra_midia: object) -> bool:

        if not isinstance(outra_midia, Midia):
            return NotImplemented

        return (self._titulo == outra_midia.titulo and
                self._tipo == outra_midia._tipo and
                self._ano == outra_midia.ano)
