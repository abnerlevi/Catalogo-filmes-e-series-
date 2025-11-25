# Entregável — Semana 1  
Catálogo de Filmes e Séries (POO)

- Modelo UML em Excel   
- README inicial


# Catálogo de Filmes e Séries (POO)

## Descrição
Sistema orientado a objetos para organizar um catálogo pessoal de filmes e séries,
com gerenciamento de episódios, avaliações, histórico, relatórios e listas personalizadas.
Persistência será feita inicialmente em JSON.

## Funcionalidades principais
- Cadastro de Filmes e Séries (com validações).
- Séries com temporadas e episódios.
- Avaliação (0–10) e cálculo de médias.
- Status de visualização: NAO_ASSISTIDO, ASSISTINDO, ASSISTIDO.
- Histórico de mídias vistas.
- Relatórios: mais assistidos, médias por gênero, tempo total.
- Listas personalizadas e favoritos.

## Estrutura inicial do projeto
catalogo/
  midia.py  
  filme.py  
  serie.py  
  temporada.py  
  episodio.py  
  usuario.py  
  lista_personalizada.py  
  dados.py  
   

## *UML TEXTUAL — Semana 1 (Modelo de Classes Inicial)*

## 1. Classe Midia (classe base)

*Atributos*

titulo: str

tipo: Enum {FILME, SERIE}

genero: str

ano: int

duracao: int

classificacao: str

elenco: list[str]

status: Enum {NÃO_ASSISTIDO, ASSISTINDO, ASSISTIDO}

nota_media: float (calculada no futuro)

*Métodos principais*

avaliar(nota: float)

atualizar_status(novo_status)

__str__()

__eq__(outra_midia)



## 2. Classe Filme (herda de Midia)

*Atributos*

(nenhum extra além dos de Midia)

*Métodos principais*

__repr__()

## 3. Classe Serie (herda de Midia)

*Atributos*

temporadas: list[Temporada]

*Métodos principais*

adicionar_temporada(temporada)

calcular_nota_media()

verificar_status_series()

__len__() (número total de episódios)

## 4. Classe Temporada

**Atributos*

numero: int

episodios: list[Episodio]

*Métodos principais*

adicionar_episodio(episodio)

total_episodios()

## 5. Classe Episodio

*Atributos*

numero: int

titulo: str

duracao: int

data_lancamento: date

status: Enum {NÃO_ASSISTIDO, ASSISTIDO}

nota: float | None

*Métodos principais*

avaliar(nota)

atualizar_status(novo_status)

## 6. Classe Usuario

*Atributos*

nome: str

listas: list[ListaPersonalizada]

historico: list[Midia]

*Métodos principais*

criar_lista(nome)

adicionar_ao_historico(midia)

tempo_total_assistido()

## 7. Classe ListaPersonalizada

*Atributos*

nome: str

itens: list[Midia]

*Métodos principais*

adicionar_midia(midia)

remover_midia(midia)

## 8. Relacionamentos 

*Midia*
->Classe base de Filme e Serie (Herança)

*Serie*
->possui várias → Temporada (Composição)

*Temporada*
->possui vários → Episodio (Composição)

*Usuario*
->possui várias → ListaPersonalizada (Agregação)
->possui um → Historico contendo → Midia (Associação)
