# Sistema RBC - Recomendacao de Filmes

Trabalho academico desenvolvido em Python utilizando **Raciocinio Baseado em Casos (RBC)** para recomendacao de filmes.

A ideia do sistema e simples: a partir de um filme escolhido ou de preferencias informadas pelo usuario, o programa compara essas caracteristicas com os filmes da base e apresenta os **5 casos mais semelhantes**.

## Objetivo

Aplicar os conceitos de RBC em uma base de filmes, trabalhando principalmente com:

- selecao de atributos;
- definicao de pesos;
- calculo de similaridade local;
- calculo de similaridade global;
- recuperacao dos casos mais semelhantes.

O sistema nao utiliza inteligencia artificial generativa nem treinamento de modelos. As recomendacoes sao feitas diretamente pela comparacao entre os casos existentes na base.

## Base de dados

O projeto utiliza uma versao tratada da base **TMDB 5000 Movies**, com aproximadamente 4.800 filmes.

O arquivo `filmes.csv` contem somente os campos necessarios para o sistema:

- ID;
- titulo;
- generos;
- idioma original;
- ano de lancamento;
- duracao;
- nota media.

## Atributos utilizados

Foram escolhidos cinco atributos para calcular a semelhanca entre os filmes.

| Atributo | Tipo | Peso |
| --- | --- | ---: |
| Generos | Categorico / conjunto | 0,40 |
| Idioma original | Categorico nominal | 0,10 |
| Ano de lancamento | Numerico discreto | 0,20 |
| Duracao | Numerico | 0,15 |
| Nota media | Numerico continuo | 0,15 |

Os pesos somam 1. O genero recebeu o maior peso por ser considerado a caracteristica mais importante para aproximar filmes com propostas semelhantes.

## Similaridade local

A similaridade local compara **um atributo por vez**. Todos os resultados ficam entre 0 e 1.

### Generos

Para generos foi utilizado o indice de **Jaccard**:

```text
similaridade = generos em comum / total de generos diferentes
```

Exemplo:

```text
Filme A: Action, Adventure
Filme B: Action, Drama

1 genero em comum / 3 generos diferentes = 0,333
```

### Idioma

A comparacao e direta:

```text
mesmo idioma     = 1
idioma diferente = 0
```

### Ano

A diferenca entre os anos e comparada usando uma tolerancia de 30 anos:

```text
similaridade = max(0, 1 - diferenca / 30)
```

### Duracao

Para duracao foi utilizada uma tolerancia de 120 minutos:

```text
similaridade = max(0, 1 - diferenca / 120)
```

### Nota

Para a nota media foi utilizada uma tolerancia de 10 pontos:

```text
similaridade = max(0, 1 - diferenca / 10)
```

Quando algum dado esta ausente, a similaridade daquele atributo recebe valor 0.

## Similaridade global

Depois das cinco comparacoes locais, o sistema calcula uma media ponderada.

```text
S = 0,40 * genero
  + 0,10 * idioma
  + 0,20 * ano
  + 0,15 * duracao
  + 0,15 * nota
```

O resultado final representa o nivel de semelhanca entre a consulta e cada filme da base.

Por exemplo, um resultado de **0,943** e apresentado como **94,30% de similaridade**.

## Como o codigo funciona

O arquivo principal e o `main.py`.

As principais funcoes sao:

### `carregar_filmes()`

Abre o arquivo `filmes.csv` e prepara os dados para as comparacoes.

### `similaridade_local()`

Compara dois filmes em um atributo especifico.

### `similaridade_global()`

Reune as cinco similaridades locais e aplica os pesos definidos no projeto.

### `recomendar()`

Compara a consulta com todos os filmes da base, ordena os resultados e retorna os cinco mais semelhantes.

### `mostrar()`

Exibe os resultados e as similaridades calculadas.

### `escolher_filme()`

Permite buscar um filme da base pelo titulo.

### `criar_consulta()`

Permite informar manualmente genero, idioma, ano, duracao e nota para criar uma recomendacao personalizada.

### `main()`

Controla o menu e o fluxo geral do programa.

## Fluxo do sistema

```text
Usuario escolhe um filme ou informa preferencias
                    |
                    v
          Sistema carrega a base
                    |
                    v
       Calcula similaridades locais
                    |
                    v
       Calcula similaridade global
                    |
                    v
     Ordena os filmes por semelhanca
                    |
                    v
             Apresenta TOP 5
```

## TOP 5 de tres filmes

O programa possui tres exemplos utilizados na entrega.

### Avatar

| Posicao | Filme | Similaridade |
| ---: | --- | ---: |
| 1 | Superman Returns | 94,30% |
| 2 | Man of Steel | 93,91% |
| 3 | X-Men: Days of Future Past | 92,34% |
| 4 | The Wolverine | 91,48% |
| 5 | Jupiter Ascending | 88,25% |

### The Dark Knight

| Posicao | Filme | Similaridade |
| ---: | --- | ---: |
| 1 | Man on Fire | 95,23% |
| 2 | The Dark Knight Rises | 94,81% |
| 3 | Running Scared | 93,12% |
| 4 | Street Kings | 91,78% |
| 5 | Harsh Times | 91,15% |

### Toy Story

| Posicao | Filme | Similaridade |
| ---: | --- | ---: |
| 1 | Toy Story 2 | 95,36% |
| 2 | Chicken Run | 94,49% |
| 3 | Monsters, Inc. | 94,33% |
| 4 | Doug's 1st Movie | 93,38% |
| 5 | The SpongeBob SquarePants Movie | 91,75% |

## Como executar

E necessario ter **Python 3.9 ou superior** instalado.

Nao e necessario instalar bibliotecas adicionais.

Na pasta do projeto:

```bash
python main.py
```

Tambem e possivel pesquisar diretamente por um filme:

```bash
python main.py --filme "Avatar"
```

Para executar os tres exemplos utilizados na entrega:

```bash
python main.py --exemplos
```

No Windows, caso o comando `python` nao funcione, pode ser utilizado `py`:

```bash
py main.py
```

## Estrutura do projeto

```text
rbc-recomendacao-filmes/
|-- main.py
|-- filmes.csv
|-- README.md
|-- documento_sistema.md
```

## Relacao com RBC

Cada filme da base representa um **caso**.

O filme escolhido ou as preferencias do usuario representam o **novo problema**. O sistema recupera os casos mais semelhantes e utiliza esses casos como recomendacao.

Neste projeto sao utilizadas principalmente as etapas de **recuperacao** e **reutilizacao** do ciclo de RBC.

## Observacoes

A base nao possui informacoes sobre em qual plataforma de streaming cada filme esta disponivel. O objetivo do projeto e demonstrar o mecanismo de recomendacao por similaridade.

Os pesos e as tolerancias foram definidos para esta implementacao e podem ser ajustados em trabalhos futuros.
