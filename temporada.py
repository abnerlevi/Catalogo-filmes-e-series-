from episodio import Episodio


class Temporada:

    def __init__(self, numero: int):
        self._numero = None
        self.numero = numero
        self.episodios: list[Episodio] = []

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, novo_numero: int):
        if not isinstance(novo_numero, int) or novo_numero <= 0:
            raise ValueError("O número da temporada deve ser positivo.")
        self._numero = novo_numero

    def adicionar_episodio(self, episodio: Episodio):
        if not isinstance(episodio, Episodio):
            raise TypeError(
                "Só é possível adicionar objetos do tipo Episodio.")
        self.episodios.append(episodio)

    def total_episodios(self) -> int:

        return len(self.episodios)

    def __str__(self) -> str:
        return f"Temporada {self.numero} ({self.total_episodios()} episódios)"
