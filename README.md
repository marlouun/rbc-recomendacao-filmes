# Sistema RBC - Recomendação de Filmes

Projeto acadêmico desenvolvido em Python utilizando **Raciocínio Baseado em Casos (RBC)** para recomendar filmes por semelhança.

A proposta é simples: o usuário escolhe um filme da base ou informa suas preferências, e o sistema compara essas informações com os demais filmes para apresentar os **5 casos mais semelhantes**.

## Objetivo

Aplicar os conceitos de RBC em uma base de filmes, utilizando:

- seleção de atributos;
- definição de pesos;
- cálculo de similaridade local;
- cálculo de similaridade global;
- recuperação dos casos mais semelhantes.

## Base de dados

O projeto utiliza uma versão tratada da base **TMDB 5000 Movies**, com 4.803 filmes.

O arquivo `filmes.csv` mantém os dados necessários para a recomendação:

- ID;
- título;
- gêneros;
- idioma original;
- ano de lançamento;
- duração;
- nota média.

## Atributos utilizados

Foram escolhidos cinco atributos para calcular a semelhança entre os filmes.

| Atributo | Tipo | Peso |
| --- | --- | ---: |
| Gêneros | Conjunto de categorias nominais | 0,40 |
| Idioma original | Categórico nominal | 0,10 |
| Ano de lançamento | Numérico discreto | 0,20 |
| Duração | Numérico | 0,15 |
| Nota média | Numérico contínuo | 0,15 |

Os pesos somam 1. O gênero recebeu o maior peso por ter maior influência na aproximação entre filmes com propostas parecidas.

## Similaridade local

A similaridade local compara **um atributo por vez**. O resultado fica entre 0 e 1.

### Gêneros

Para gêneros foi usado o índice de **Jaccard**:

```text
similaridade = gêneros em comum / total de gêneros diferentes
```

Exemplo:

```text
Filme A: Action, Adventure
Filme B: Action, Drama

1 gênero em comum / 3 gêneros diferentes = 0,333
```

### Idioma

A comparação é direta:

```text
mesmo idioma     = 1
idioma diferente = 0
```

### Ano

A diferença entre os anos é comparada usando uma tolerância de 30 anos:

```text
similaridade = max(0, 1 - diferença / 30)
```

### Duração

Para duração foi usada uma tolerância de 120 minutos:

```text
similaridade = max(0, 1 - diferença / 120)
```

### Nota

Para a nota média foi usada uma tolerância de 10 pontos:

```text
similaridade = max(0, 1 - diferença / 10)
```

Quando algum dado está ausente, a similaridade daquele atributo recebe valor 0.

## Similaridade global

Depois das cinco comparações locais, o sistema calcula uma média ponderada:

```text
S = 0,40 * gênero
  + 0,10 * idioma
  + 0,20 * ano
  + 0,15 * duração
  + 0,15 * nota
```

O resultado final representa o nível de semelhança entre a consulta e cada filme da base.

Por exemplo, um resultado de **0,943** é apresentado como **94,30% de similaridade**.

## Como o código funciona

O arquivo principal é o `main.py`.

### `carregar_filmes()`

Abre o arquivo `filmes.csv` e prepara os dados para as comparações.

### `similaridade_local()`

Compara dois filmes em um atributo específico.

### `similaridade_global()`

Reúne as cinco similaridades locais e aplica os pesos definidos no projeto.

### `recomendar()`

Compara a consulta com todos os filmes da base, ordena os resultados e retorna os cinco mais semelhantes.

### `mostrar()`

Exibe os resultados e as similaridades calculadas.

### `escolher_filme()`

Permite buscar um filme da base pelo título.

### `criar_consulta()`

Permite informar manualmente gênero, idioma, ano, duração e nota para criar uma recomendação personalizada.

### `main()`

Controla o menu e o fluxo geral do programa.

## Fluxo do sistema

```text
Usuário escolhe um filme ou informa preferências
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
     Ordena os filmes por semelhança
                    |
                    v
             Apresenta TOP 5
```

## TOP 5 de três filmes

O programa possui três exemplos usados na entrega.

### Avatar

| Posição | Filme | Similaridade |
| ---: | --- | ---: |
| 1 | Superman Returns | 94,30% |
| 2 | Man of Steel | 93,91% |
| 3 | X-Men: Days of Future Past | 92,34% |
| 4 | The Wolverine | 91,48% |
| 5 | Jupiter Ascending | 88,25% |

### The Dark Knight

| Posição | Filme | Similaridade |
| ---: | --- | ---: |
| 1 | Man on Fire | 95,23% |
| 2 | The Dark Knight Rises | 94,81% |
| 3 | Running Scared | 93,12% |
| 4 | Street Kings | 91,78% |
| 5 | Harsh Times | 91,15% |

### Toy Story

| Posição | Filme | Similaridade |
| ---: | --- | ---: |
| 1 | Toy Story 2 | 95,36% |
| 2 | Chicken Run | 94,49% |
| 3 | Monsters, Inc. | 94,33% |
| 4 | Doug's 1st Movie | 93,38% |
| 5 | The SpongeBob SquarePants Movie | 91,75% |

## Como executar

É necessário ter **Python 3.9 ou superior** instalado. Não é necessário instalar bibliotecas adicionais.

Na pasta do projeto:

```bash
python main.py
```

Para pesquisar diretamente por um filme:

```bash
python main.py --filme "Avatar"
```

Para executar os três exemplos da entrega:

```bash
python main.py --exemplos
```

No Windows, também pode ser usado:

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

## Relação com o RBC

Cada filme da base representa um **caso**. O filme escolhido ou as preferências informadas representam a nova consulta.

O sistema recupera os casos mais semelhantes e usa esses casos como recomendação. Neste projeto são utilizadas principalmente as etapas de **recuperação** e **reutilização** do ciclo de RBC.

## Observações

A base não informa em qual plataforma de streaming cada filme está disponível. O objetivo do projeto é demonstrar o mecanismo de recomendação por similaridade.

Os pesos e as tolerâncias foram definidos para esta implementação e podem ser ajustados em versões futuras.
