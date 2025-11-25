import pytest
from midia import Midia, TipoMidia, StatusVisualizacao
from filme import Filme
from serie import Serie
from episodio import Episodio
from temporada import Temporada


@pytest.fixture
def midia_base_filme():
    return Midia("O Poderoso Chefão", TipoMidia.FILME, "Drama", 1972, 175, "16", ["Marlon Brando"], StatusVisualizacao.NAO_ASSISTIDO)


@pytest.fixture
def filme_valido():
    return Filme("Pulp Fiction", "Crime", 1994, 154, "18", ["John Travolta"], StatusVisualizacao.ASSISTIDO)


@pytest.fixture
def serie_valida():
    return Serie("Breaking Bad", "Drama", 2008, 45, "16", ["Bryan Cranston"], StatusVisualizacao.ASSISTINDO)


@pytest.fixture
def episodio_valido():
    return Episodio(1, "Pilot", 58, "2008-01-20", StatusVisualizacao.NAO_ASSISTIDO)


@pytest.fixture
def temporada_valida(episodio_valido):
    temp = Temporada(1)
    temp.adicionar_episodio(episodio_valido)
    return temp


def test_midia_duracao_nao_positiva_levanta_erro(midia_base_filme):
    with pytest.raises(ValueError):
        midia_base_filme.duracao = -10


def test_midia_titulo_vazio_levanta_erro(midia_base_filme):
    with pytest.raises(ValueError):
        midia_base_filme.titulo = "  "


def test_midia_titulo_alterado_com_sucesso(midia_base_filme):
    midia_base_filme.titulo = "O Poderoso Chefão II"
    assert midia_base_filme.titulo == "O Poderoso Chefão II"


def test_episodio_numero_negativo_levanta_erro(episodio_valido):
    with pytest.raises(ValueError):
        episodio_valido.numero = 0


def test_midia_eq_identica_retorna_true(midia_base_filme):
    outra_midia = Midia("O Poderoso Chefão", TipoMidia.FILME, "Drama", 1972, 175, "16", [
                        "Marlon Brando"], StatusVisualizacao.NAO_ASSISTIDO)
    assert midia_base_filme == outra_midia


def test_midia_eq_ano_diferente_retorna_false(midia_base_filme):
    outra_midia = Midia("O Poderoso Chefão", TipoMidia.FILME, "Drama", 1973, 175, "16", [
                        "Marlon Brando"], StatusVisualizacao.NAO_ASSISTIDO)
    assert midia_base_filme != outra_midia


def test_serie_len_total_episodios(serie_valida, episodio_valido):

    temp1 = Temporada(1)
    temp1.adicionar_episodio(episodio_valido)

    temp2 = Temporada(2)
    temp2.adicionar_episodio(episodio_valido)
    temp2.adicionar_episodio(episodio_valido)

    serie_valida.adicionar_temporada(temp1)
    serie_valida.adicionar_temporada(temp2)

    assert len(serie_valida) == 3


def test_temporada_adicionar_episodio(temporada_valida):
    assert temporada_valida.total_episodios() == 1


def test_filme_herda_titulo_e_validacao(filme_valido):
    assert filme_valido.titulo == "Pulp Fiction"
    with pytest.raises(ValueError):
        filme_valido.ano = 1800
