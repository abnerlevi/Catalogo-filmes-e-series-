from enum import Enum
from typing import List, Optional, Union
import uuid


class TipoMidia(Enum):

    FILME = "FILME"
    SERIE = "SERIE"


class StatusVisualizacao(Enum):

    PENDENTE = "Pendente"
    ASSISTINDO = "Assistindo"
    CONCLUIDO = "Concluído"
    ABANDONADO = "Abandonado"


class Midia:

    def __init__(
        self,
        titulo: str,
        genero: str,
        ano_lancamento: int,
        elenco: List[str],
        tipo: TipoMidia,
        id: Optional[int] = None,
        status_visualizacao: StatusVisualizacao = StatusVisualizacao.PENDENTE,
        avaliacao: float = 0.0
    ):

        self._id: Optional[int] = id

        self.uuid: str = str(uuid.uuid4())

        if not titulo or not genero or not ano_lancamento:
            raise ValueError(
                "Título, gênero e ano de lançamento são obrigatórios.")

        self.titulo: str = titulo
        self.genero: str = genero
        self.ano_lancamento: int = ano_lancamento
        self.elenco: List[str] = elenco
        self.tipo: TipoMidia = tipo
        self._status_visualizacao: StatusVisualizacao = status_visualizacao
        self._avaliacao: float = 0.0

        self.avaliacao = avaliacao

    @property
    def id(self) -> Optional[int]:

        return self._id

    @id.setter
    def id(self, value: int):

        if self._id is None and isinstance(value, int) and value > 0:
            self._id = value
        elif self._id is not None and self._id != value:

            self._id = value

        elif self._id is None and value is None:

            pass
        else:

            pass

    @property
    def status_visualizacao(self) -> StatusVisualizacao:

        return self._status_visualizacao

    @status_visualizacao.setter
    def status_visualizacao(self, value: StatusVisualizacao):

        if not isinstance(value, StatusVisualizacao):
            raise TypeError(
                "O status deve ser um membro do enum StatusVisualizacao.")
        self._status_visualizacao = value

    @property
    def avaliacao(self) -> float:

        return self._avaliacao

    @avaliacao.setter
    def avaliacao(self, value: Union[int, float]):

        try:
            val = float(value)
        except ValueError:
            raise ValueError("A avaliação deve ser um número.")

        val = max(0.0, min(val, 10.0))

        if self.status_visualizacao != StatusVisualizacao.CONCLUIDO and val > 0.0:
            print(
                "Aviso: Avaliação só é válida para mídias 'Concluído'. Avaliação redefinida para 0.0.")
            self._avaliacao = 0.0
        else:
            self._avaliacao = val

    def to_dict(self) -> dict:

        data = {
            'id': self.id,
            'titulo': self.titulo,
            'genero': self.genero,
            'ano_lancamento': self.ano_lancamento,
            'elenco': self.elenco,
            'tipo': self.tipo.name,
            'status_visualizacao': self.status_visualizacao.name,
            'avaliacao': self.avaliacao
        }
        return data

    def __str__(self) -> str:

        elenco_str = ", ".join(
            self.elenco[:3]) + ("..." if len(self.elenco) > 3 else "")
        return (
            f"  Título: {self.titulo} ({self.ano_lancamento}) | Tipo: {self.tipo.value}\n"
            f"  Gênero: {self.genero} | Status: {self.status_visualizacao.value}\n"
            f"  Avaliação: {self.avaliacao:.1f}/10.0 | Elenco: {elenco_str}"
        )


class Episodio:

    def __init__(self, numero: int, nome: str, duracao_minutos: int, id: Optional[int] = None):

        if numero <= 0 or duracao_minutos <= 0:
            raise ValueError(
                "Número e duração do episódio devem ser positivos.")

        self._id: Optional[int] = id
        self.numero: int = numero
        self.nome: str = nome
        self.duracao_minutos: int = duracao_minutos

    @property
    def id(self) -> Optional[int]:

        return self._id

    @id.setter
    def id(self, value: int):

        if self._id is None and isinstance(value, int) and value > 0:
            self._id = value
        elif self._id is not None and self._id != value:
            self._id = value

    def to_dict(self) -> dict:

        return {
            'id': self.id,
            'numero': self.numero,
            'nome': self.nome,
            'duracao_minutos': self.duracao_minutos
        }

    def __str__(self) -> str:
        return f"E{self.numero}: {self.nome} ({self.duracao_minutos} min)"


class Temporada:

    def __init__(self, numero: int, titulo: str, episodios: Optional[List[Episodio]] = None, id: Optional[int] = None):

        if numero <= 0:
            raise ValueError("O número da temporada deve ser positivo.")

        self._id: Optional[int] = id
        self.numero: int = numero
        self.titulo: str = titulo
        self.episodios: List[Episodio] = episodios if episodios is not None else [
        ]

    @property
    def id(self) -> Optional[int]:

        return self._id

    @id.setter
    def id(self, value: int):

        if self._id is None and isinstance(value, int) and value > 0:
            self._id = value
        elif self._id is not None and self._id != value:
            self._id = value

    def adicionar_episodio(self, episodio: Episodio):

        if not isinstance(episodio, Episodio):
            raise TypeError("O objeto deve ser uma instância de Episodio.")

        if any(e.numero == episodio.numero for e in self.episodios):
            raise ValueError(
                f"O episódio número {episodio.numero} já existe na T{self.numero}.")

        self.episodios.append(episodio)

    def to_dict(self) -> dict:

        return {
            'id': self.id,
            'numero': self.numero,
            'titulo': self.titulo,

            'episodios': [e.to_dict() for e in self.episodios]
        }

    def __str__(self) -> str:
        total_eps = len(self.episodios)
        return f"T{self.numero}: {self.titulo} ({total_eps} episódios)"
