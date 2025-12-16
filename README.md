# Catálogo Pessoal de Mídias

## Visão Geral

Este projeto implementa um sistema de linha de comando (CLI) para gerenciar um catálogo pessoal de filmes e séries. O sistema permite acompanhar o progresso de visualização, registrar avaliações, gerenciar temporadas e episódios, e gerar relatórios de consumo de mídia. A persistência é realizada em SQLite, e a modelagem orientada a objetos enfatiza herança, encapsulamento, validações e composição.

O projeto foi desenvolvido como parte de uma atividade acadêmica, seguindo os requisitos de POO e regras de negócio especificadas.

## Funcionalidades Principais

### 1. Cadastro de Mídias
- **Campos**: Título, tipo (Filme ou Série), gênero, ano de lançamento, duração (minutos), elenco (lista), status de visualização (Pendente, Assistindo, Concluído, Abandonado), avaliação (0.0 a 10.0).
- **Validações**: Impede duplicidade de títulos com mesmo tipo e ano. Validações automáticas via `@property`.

### 2. Gerenciamento de Séries e Episódios
- Para séries: Registro de temporadas e episódios com campos como número, nome, duração.
- Atualização automática do status da série para "Concluído" quando todos os episódios forem marcados como assistidos.
- Adição dinâmica de episódios e temporadas.

### 3. Avaliações e Histórico
- Avaliação de mídias de 0.0 a 10.0.
- Cálculo automático de médias por série, gênero e catálogo geral.
- Histórico de visualização com datas (embora simplificado na implementação atual).

### 4. Relatórios
- Estatísticas gerais: Total de mídias, contagem por status, média de avaliações.
- Listas filtradas por status (ex.: mídias pendentes).
- Relatórios de tempo total assistido (estimado via durações).

### 5. Interface CLI
- Menu interativo com opções para:
  - Visualizar catálogo completo.
  - Adicionar filmes ou séries.
  - Atualizar status e avaliações.
  - Adicionar episódios a séries.
  - Remover mídias.
  - Gerar relatórios de estatísticas.

## Requisitos Técnicos de POO

### Modelagem e Herança
- **Midia** (classe base abstrata) com subclasses **Filme** e **Serie**.
- **Serie** agrega **Temporada**, que contém **Episodio**.
- Relacionamentos de composição para representar a estrutura hierárquica.

### Encapsulamento e Validações
- Uso de `@property` para validar:
  - Duração (>0 minutos).
  - Avaliações (0.0 a 10.0).
  - Títulos não vazios.
  - Números de temporada/episódio positivos.
- Atualizações automáticas de status (ex.: série concluída ao finalizar episódios).

### Métodos Especiais
- `__str__`: Representação formatada de mídias, episódios e temporadas.
- `__len__`: Número de episódios em uma temporada ou série.
- `__eq__`: Comparação de mídias por título e tipo.
- `__lt__`: Ordenação por avaliação.

### Persistência
- Banco de dados SQLite (`dados.db`) com tabelas para Midia, Temporada e Episodio.
- Funções para salvar, carregar e atualizar dados automaticamente.

### Testes
- Cobertura de criação de mídias, cálculos de estatísticas, validações e relatórios.

## Estrutura do Projeto

```
entregavel1_FINALIZADO/
├── main.py                 # Script principal com interface CLI
├── catalogo.py             # Classe Catalogo para gerenciamento e persistência
├── midia.py                # Classes base: Midia, Episodio, Temporada, enums
├── midia_concreta.py       # Classes concretas: Filme, Serie
├── test_catalogo.py        # Testes com pytest
├── dados.db                # Banco de dados SQLite (gerado automaticamente)
├── README.md               # Esta documentação
└── .git/                   # Controle de versão
```

### Diagrama de Classes (Texto)

```
Midia (abstrata)
├── atributos: id, titulo, genero, ano_lancamento, elenco, tipo, status_visualizacao, avaliacao
├── métodos: __init__, __str__, __eq__, __lt__, to_dict, setters com validação
└── subclasses:
    ├── Filme
    │   ├── atributos adicionais: duracao_minutos
    │   └── métodos: __str__
    └── Serie
        ├── atributos adicionais: temporadas (lista de Temporada)
        └── métodos: adicionar_temporada, duracao_total, __str__

Temporada
├── atributos: id, numero, titulo, episodios (lista de Episodio)
└── métodos: __init__, adicionar_episodio, __str__, __len__

Episodio
├── atributos: id, numero, nome, duracao_minutos
└── métodos: __init__, __str__
```

## Instalação e Uso

### Pré-requisitos
- Python 3.8+
- SQLite (incluído no Python)

### Instalação
1. Clone ou baixe o projeto.
2. Navegue até o diretório do projeto.
3. Execute o script principal:

```bash
python main.py
```

### Uso Básico
- O programa inicia com um menu interativo.
- Selecione opções numeradas para navegar:
  - 1: Visualizar catálogo.
  - 2: Adicionar nova mídia.
  - 3: Atualizar status/avaliação.
  - 4: Adicionar episódio a série.
  - 5: Remover mídia.
  - 6: Gerar relatório.
  - 0: Sair.

### Exemplos de Uso
- **Adicionar Filme**: Escolha opção 2 > 1, insira título, gênero, ano, elenco, duração.
- **Adicionar Série**: Opção 2 > 2, insira dados básicos; temporadas/episódios são adicionados posteriormente.
- **Avaliar Mídia**: Opção 3, selecione ID, atualize status e avaliação.
- **Relatório**: Opção 6, visualize estatísticas gerais e listas pendentes.


Os testes cobrem:
- Criação e manipulação de mídias.
- Validações de atributos.
- Cálculos de estatísticas.
- Persistência no banco.

## Regras de Negócio

- **Avaliações**: Numéricas de 0.0 a 10.0, clamped automaticamente.
- **Status de Séries**: "Concluído" apenas se todos os episódios estiverem concluídos.
- **Duplicidade**: Impede títulos idênticos com mesmo tipo e ano.
- **Relatórios**: Consideram apenas mídias com status "Concluído".
- **Persistência**: Dados salvos automaticamente no SQLite.

## Critérios de Aceite Atendidos

- ✅ Modelagem OO com herança, encapsulamento e métodos especiais.
- ✅ Validações e regras de negócio implementadas.
- ✅ Relatórios de estatísticas e filtros.
- ✅ Documentação completa no README.

## Cronograma e Desenvolvimento

O projeto foi desenvolvido em 5 semanas, conforme o cronograma:
- **Semana 1**: Modelagem OO e planejamento.
- **Semana 2**: Implementação de classes base e validações.
- **Semana 3**: Relacionamentos e persistência.
- **Semana 4**: Regras de negócio e CLI.
- **Semana 5**: Refinamentos, testes e documentação final.





Desenvolvido por [ABNER LEVI DA SILVA ANDRADE] como atividade da disciplina de Programação Orientada a Objetos.