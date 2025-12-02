class Episodio:

    def __init__(self, numero: int, nome: str, duracao_minutos: int):
        self._numero = None
        self._duracao_minutos = None

        self.numero = numero
        self.nome = nome
        self.duracao_minutos = duracao_minutos

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, novo_numero: int):
        if not isinstance(novo_numero, int) or novo_numero <= 0:
            raise ValueError("O número do episódio deve ser positivo.")
        self._numero = novo_numero

    @property
    def duracao_minutos(self):
        return self._duracao_minutos

    @duracao_minutos.setter
    def duracao_minutos(self, nova_duracao: int):
        if not isinstance(nova_duracao, int) or nova_duracao <= 0:
            raise ValueError("A duração do episódio deve ser positiva.")
        self._duracao_minutos = nova_duracao

    def __str__(self) -> str:
        return f"Ep. {self.numero} - {self.nome} ({self.duracao_minutos} min)"
