import argparse
import csv
from pathlib import Path


# Os pesos somam 1. Gênero tem maior influência na recomendação.
PESOS = {"generos": 0.40, "idioma": 0.10, "ano": 0.20,
         "duracao": 0.15, "nota": 0.15}
TOLERANCIAS = {"ano": 30, "duracao": 120, "nota": 10}


def carregar_filmes():
    caminho = Path(__file__).with_name("filmes.csv")
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        filmes = list(csv.DictReader(arquivo))
    for filme in filmes:
        filme["generos"] = set(filter(None, filme["generos"].split("|")))
        for atributo in TOLERANCIAS:
            filme[atributo] = float(filme[atributo]) if filme[atributo] else None
    return filmes


def similaridade_local(atributo, a, b):
    # Dado ausente não significa que os filmes sejam semelhantes.
    if a is None or b is None or a == "" or b == "":
        return 0.0
    if atributo == "generos":
        uniao = a | b
        return len(a & b) / len(uniao) if uniao else 0.0
    if atributo == "idioma":
        return 1.0 if a == b else 0.0
    return max(0.0, 1 - abs(a - b) / TOLERANCIAS[atributo])


def similaridade_global(consulta, filme):
    locais = {atributo: similaridade_local(atributo, consulta[atributo],
                                          filme[atributo])
              for atributo in PESOS}
    global_ = sum(PESOS[a] * locais[a] for a in PESOS) / sum(PESOS.values())
    return global_, locais


def recomendar(consulta, filmes):
    resultados = []
    for filme in filmes:
        # O filme consultado não pode recomendar a si mesmo.
        if consulta.get("id") == filme["id"]:
            continue
        global_, locais = similaridade_global(consulta, filme)
        resultados.append((filme, global_, locais))
    resultados.sort(key=lambda item: (-item[1], item[0]["titulo"],
                                       int(item[0]["id"])))
    return resultados[:5]


def mostrar(consulta, filmes):
    print("\nConsulta:", consulta["titulo"])
    print("Gêneros:", ", ".join(sorted(consulta["generos"])))
    print("Idioma:", consulta["idioma"], "| Ano:", consulta["ano"],
          "| Duração:", consulta["duracao"], "| Nota:", consulta["nota"])
    for posicao, (filme, global_, locais) in enumerate(recomendar(consulta, filmes), 1):
        print(f"\n{posicao}. {filme['titulo']} — {global_:.2%}")
        print("   " + " | ".join(f"{a}: {v:.3f}" for a, v in locais.items()))


def escolher_filme(filmes, texto):
    encontrados = [f for f in filmes if texto.casefold() in f["titulo"].casefold()]
    if not encontrados:
        print("Nenhum filme encontrado. Busque pelo título em inglês da base.")
        return None
    exatos = [f for f in encontrados if f["titulo"].casefold() == texto.casefold()]
    if len(exatos) == 1:
        return exatos[0]
    for filme in encontrados:
        print(f"ID {filme['id']}: {filme['titulo']} ({filme['ano']})")
    identificador = input("Digite o ID do filme desejado: ").strip()
    return next((f for f in encontrados if f["id"] == identificador), None)


def ler_numero(mensagem, minimo, maximo):
    while True:
        try:
            valor = float(input(mensagem).strip().replace(",", "."))
            if minimo <= valor <= maximo:
                return valor
        except ValueError:
            pass
        print(f"Informe um número entre {minimo} e {maximo}.")


def criar_consulta(filmes):
    generos_validos = set().union(*(f["generos"] for f in filmes))
    print("Gêneros disponíveis:", ", ".join(sorted(generos_validos)))
    mapa = {g.casefold(): g for g in generos_validos}
    while True:
        entrada = [g.strip().casefold() for g in input("Gêneros separados por vírgula: ").split(",")]
        if entrada and all(g in mapa for g in entrada):
            generos = {mapa[g] for g in entrada}
            break
        print("Escolha ao menos um dos gêneros disponíveis.")
    idiomas = sorted({f["idioma"] for f in filmes if f["idioma"]})
    print("Idiomas disponíveis:", ", ".join(idiomas))
    while True:
        idioma = input("Idioma original (ex.: en, pt): ").strip().lower()
        if idioma in idiomas:
            break
        print("Escolha um dos códigos disponíveis.")
    anos = [f["ano"] for f in filmes if f["ano"] is not None]
    return {"titulo": "Preferências informadas", "generos": generos,
            "idioma": idioma,
            "ano": ler_numero("Ano desejado: ", min(anos), max(anos)),
            "duracao": ler_numero("Duração desejada (minutos): ", 1, 600),
            "nota": ler_numero("Nota desejada (0 a 10): ", 0, 10)}


def main():
    parser = argparse.ArgumentParser(description="Recomendação de filmes por RBC")
    parser.add_argument("--filme", help="Título de um filme da base")
    parser.add_argument("--exemplos", action="store_true", help="Executa os três exemplos da entrega")
    args = parser.parse_args()
    filmes = carregar_filmes()
    if args.exemplos:
        for titulo in ("Avatar", "The Dark Knight", "Toy Story"):
            consulta = next(f for f in filmes if f["titulo"] == titulo)
            mostrar(consulta, filmes)
        return
    if args.filme:
        consulta = escolher_filme(filmes, args.filme)
        if consulta:
            mostrar(consulta, filmes)
        return
    while True:
        print("\nRBC — FILMES\n1. Buscar por filme\n2. Informar os cinco atributos\n0. Sair")
        opcao = input("Opção: ").strip()
        if opcao == "0":
            break
        if opcao == "1":
            titulo = input("Título do filme: ").strip()
            consulta = escolher_filme(filmes, titulo) if titulo else None
        elif opcao == "2":
            consulta = criar_consulta(filmes)
        else:
            print("Opção inválida.")
            continue
        if consulta:
            mostrar(consulta, filmes)


if __name__ == "__main__":
    main()
