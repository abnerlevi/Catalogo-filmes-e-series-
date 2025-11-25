# episodio.py
from midia import StatusVisualizacao


class Episodio:

    def __init__(self, numero: int, titulo: str, duracao: int, data_lancamento: str, status: StatusVisualizacao):
        self._numero = None
        self._duracao = None
        self._nota = 0.0

        self.numero = numero
        self.duracao = duracao

        self.titulo = titulo
        self.data_lancamento = data_lancamento
        self._status = status

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, novo_numero: int):
        if not isinstance(novo_numero, int) or novo_numero <= 0:
            raise ValueError("O número do episódio deve ser positivo.")
        self._numero = novo_numero

    @property
    def duracao(self):
        return self._duracao

    @duracao.setter
    def duracao(self, nova_duracao: int):
        if not isinstance(nova_duracao, int) or nova_duracao <= 0:
            raise ValueError("A duração do episódio deve ser positiva.")
        self._duracao = nova_duracao

    def __str__(self) -> str:
        return f"Ep. {self.numero} - {self.titulo} ({self.duracao} min)"
