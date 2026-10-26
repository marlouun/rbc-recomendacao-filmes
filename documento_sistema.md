# Sistema RBC para recomendação de filmes

## Execução

Requer Python 3.9 ou superior. Não precisa instalar bibliotecas, usar API ou acessar a internet. Baixe o repositório, extraia os arquivos e abra o terminal na pasta.

```bash
python main.py
python main.py --filme "Avatar"
python main.py --exemplos
```

No Windows, também é possível usar `py main.py`. A opção 1 busca um filme conhecido; a opção 2 recebe os cinco atributos de preferência. A saída apresenta os TOP 5 com similaridade global em porcentagem e as cinco similaridades locais de 0 a 1. Os títulos e gêneros estão em inglês, conforme a base original.

## 1. Análise da base

Fonte: arquivo `tmdb_5000_movies.csv` fornecido na atividade, disponível em https://drive.google.com/file/d/1LsarcYG26L7fq9Ls6LhFywqyTcCu1IQH/view . São 4.803 registros e 20 colunas.

| Coluna original | Conteúdo e decisão |
|---|---|
| budget | Orçamento; excluído por não representar diretamente preferência de conteúdo e apresentar zeros. |
| genres | Lista de gêneros; selecionada. |
| homepage | Site do filme; excluído, com muitos valores ausentes. |
| id | Identificador; mantido para distinguir os filmes, sem peso. |
| keywords | Palavras-chave; potencialmente úteis, mas excluídas para simplificar a primeira versão. |
| original_language | Idioma original; selecionado. |
| original_title | Título original; excluído do cálculo. |
| overview | Sinopse; excluída para evitar processamento de texto mais complexo. |
| popularity | Popularidade; excluída por refletir visibilidade, não necessariamente afinidade. |
| production_companies | Produtoras; excluídas por serem menos diretas para a escolha do usuário. |
| production_countries | Países de produção; excluídos para manter o modelo pequeno. |
| release_date | Data de lançamento; selecionada, utilizando somente o ano. |
| revenue | Receita; excluída por refletir desempenho comercial. |
| runtime | Duração; selecionada. |
| spoken_languages | Idiomas falados; excluídos, utilizando apenas o idioma original. |
| status | Situação de lançamento; excluída por ter pouca utilidade para afinidade. |
| tagline | Frase promocional; excluída do cálculo. |
| title | Título; mantido para busca e exibição, sem peso. |
| vote_average | Nota média; selecionada. |
| vote_count | Quantidade de votos; usada apenas na preparação, para identificar notas sem avaliação. |

O arquivo `filmes.csv` é uma projeção da base original: mantém os 4.803 filmes, seus IDs, títulos e os cinco atributos selecionados. Gêneros foram extraídos do JSON e separados por `|`; o ano foi extraído da data. Duração vazia ou igual a zero foi tratada como ausente; nota sem votos também foi tratada como ausente. Não foram inventados valores nem removidos filmes.

A base não informa em quais plataformas cada filme está disponível. O projeto demonstra o mecanismo de recomendação que uma plataforma poderia utilizar; não consulta catálogos atuais de streaming.

## 2. Atributos, tipos e pesos

| Entrada | Campo original | Tipo no sistema | Peso | Justificativa |
|---|---|---|---:|---|
| Gêneros | genres | Conjunto de categorias nominais | 0,40 | Principal aproximação do conteúdo preferido. |
| Idioma original | original_language | Categórico nominal | 0,10 | Considera preferência linguística. |
| Ano de lançamento | release_date | Numérico discreto | 0,20 | Aproxima filmes de épocas semelhantes. |
| Duração em minutos | runtime | Numérico | 0,15 | Considera o tempo desejado para assistir. |
| Nota média de 0 a 10 | vote_average | Numérico contínuo | 0,15 | Aproxima o nível de avaliação desejado. |

Os pesos e tolerâncias são escolhas de projeto, não valores aprendidos ou comprovadamente ótimos. Somam 1 e priorizam gênero. Precisariam ser validados com usuários para uma aplicação real. Na entrada manual, o ano deve estar no intervalo observado na base; a duração aceita 1 a 600 minutos; a nota aceita 0 a 10. Um filme de referência preenche automaticamente os mesmos cinco atributos.

## 3. Similaridades locais

Todas variam de 0 a 1. Zero representa ausência de semelhança pelo critério definido, e 1 representa igualdade nesse atributo.

- **Gêneros — Jaccard:** `s(A,B) = quantidade de gêneros em comum / quantidade de gêneros distintos na união`. Exemplo: {Action, Adventure} e {Action, Drama} possuem 1 gênero em comum e 3 na união: `s = 1/3 = 0,3333`. Se um conjunto estiver vazio, a similaridade é zero, inclusive quando os dois estão vazios.
- **Idioma — igualdade:** `s(a,b) = 1` se os códigos forem iguais; `s(a,b) = 0` se forem diferentes.
- **Ano — distância linear:** `s(a,b) = max(0, 1 - |a-b|/30)`. Filmes de 2000 e 2006: `s = 0,8`. Diferenças de 30 anos ou mais resultam em zero.
- **Duração — distância linear:** `s(a,b) = max(0, 1 - |a-b|/120)`. Durações de 100 e 130 minutos: `s = 0,75`. Diferenças de 120 minutos ou mais resultam em zero.
- **Nota — distância linear:** `s(a,b) = max(0, 1 - |a-b|/10)`. Notas 8 e 6: `s = 0,8`.

As tolerâncias representam diferenças que zeram a semelhança: 30 anos, 120 minutos e 10 pontos de nota. Não são os intervalos mínimo e máximo medidos na base. Nota próxima significa avaliação parecida, não necessariamente maior qualidade.

Se um valor estiver ausente em qualquer lado, a similaridade local desse atributo será zero. Mantém-se o peso no denominador: é uma decisão conservadora para não tratar falta de informação como correspondência. Isso pode reduzir a classificação de registros incompletos.

## 4. Similaridade global

A similaridade global é a média ponderada das similaridades locais:

`S(q,c) = soma(peso_i × similaridade_local_i) / soma(peso_i)`

Como os pesos somam 1:

`S = 0,40×gêneros + 0,10×idioma + 0,20×ano + 0,15×duração + 0,15×nota`

O programa compara a consulta com todos os casos, exclui o próprio filme pelo ID e ordena pela similaridade global decrescente. Empates são resolvidos por título e depois ID. A porcentagem representa semelhança segundo esses critérios; não é uma probabilidade de o usuário gostar do filme.

Exemplo real: Avatar e Superman Returns têm os mesmos quatro gêneros e idioma; anos 2009 e 2006; durações 162 e 154 minutos; notas 7,2 e 5,4.

`S = 0,40×1 + 0,10×1 + 0,20×0,9 + 0,15×0,933333 + 0,15×0,82 = 0,943 = 94,30%`

## 5. TOP 5 de três filmes

Resultados produzidos por `python main.py --exemplos`. As similaridades locais abaixo foram arredondadas apenas para exibição; o cálculo global utiliza a precisão original.

### Consulta: Avatar

Gêneros: Action, Adventure, Fantasy, Science Fiction. Idioma: en. Ano: 2009. Duração: 162 minutos. Nota: 7.2.

| Posição | Filme | Gêneros | Idioma | Ano | Duração | Nota | Global |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | Superman Returns | 1.0000 | 1.0000 | 0.9000 | 0.9333 | 0.8200 | 94.30% |
| 2 | Man of Steel | 1.0000 | 1.0000 | 0.8667 | 0.8417 | 0.9300 | 93.91% |
| 3 | X-Men: Days of Future Past | 1.0000 | 1.0000 | 0.8333 | 0.7417 | 0.9700 | 92.34% |
| 4 | The Wolverine | 1.0000 | 1.0000 | 0.8667 | 0.7000 | 0.9100 | 91.48% |
| 5 | Jupiter Ascending | 1.0000 | 1.0000 | 0.8000 | 0.6833 | 0.8000 | 88.25% |

### Consulta: The Dark Knight

Gêneros: Action, Crime, Drama, Thriller. Idioma: en. Ano: 2008. Duração: 152 minutos. Nota: 8.2.

| Posição | Filme | Gêneros | Idioma | Ano | Duração | Nota | Global |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | Man on Fire | 1.0000 | 1.0000 | 0.8667 | 0.9500 | 0.9100 | 95.23% |
| 2 | The Dark Knight Rises | 1.0000 | 1.0000 | 0.8667 | 0.8917 | 0.9400 | 94.81% |
| 3 | Running Scared | 1.0000 | 1.0000 | 0.9333 | 0.7500 | 0.8800 | 93.12% |
| 4 | Street Kings | 1.0000 | 1.0000 | 1.0000 | 0.6417 | 0.8100 | 91.78% |
| 5 | Harsh Times | 1.0000 | 1.0000 | 0.9000 | 0.7333 | 0.8100 | 91.15% |

### Consulta: Toy Story

Gêneros: Animation, Comedy, Family. Idioma: en. Ano: 1995. Duração: 81 minutos. Nota: 7.7.

| Posição | Filme | Gêneros | Idioma | Ano | Duração | Nota | Global |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | Toy Story 2 | 1.0000 | 1.0000 | 0.8667 | 0.9083 | 0.9600 | 95.36% |
| 2 | Chicken Run | 1.0000 | 1.0000 | 0.8333 | 0.9750 | 0.8800 | 94.49% |
| 3 | Monsters, Inc. | 1.0000 | 1.0000 | 0.8000 | 0.9083 | 0.9800 | 94.33% |
| 4 | Doug's 1st Movie | 1.0000 | 1.0000 | 0.8667 | 0.9667 | 0.7700 | 93.38% |
| 5 | The SpongeBob SquarePants Movie | 1.0000 | 1.0000 | 0.7000 | 0.9500 | 0.9000 | 91.75% |

## 6. Relação com RBC e limites

Cada filme é um caso armazenado. O perfil informado ou filme escolhido é a consulta. O sistema **recupera** casos similares e **reutiliza** esses casos como recomendações. A solução não precisa adaptar um filme: apresenta os casos recuperados.

Esta versão implementa recuperação e reutilização. Não implementa revisão por feedback nem retenção automática de novas experiências. Portanto, não representa o ciclo completo de aprendizado de RBC. A atividade exige cálculos e classificação de casos, que estão explícitos nas funções `similaridade_local`, `similaridade_global` e `recomendar`.

Não há treinamento de rede neural nem uso de IA generativa. Filmes com gêneros iguais podem ter temas diferentes, e isso explica recomendações que não parecem tão próximas pelo enredo. Acrescentar palavras-chave seria uma melhoria posterior, acompanhada de nova avaliação de pesos.
