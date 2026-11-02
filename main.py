from funcoes import (
    ler_csv,
    padronizar_categoria,
    padronizar_canal,
    validar_numeros,
    converter_data,
    testar_hipotese_entrega,
    contar_por_canal,
    contar_por_ano_mes,
    gerar_relatorio,
)

ARQUIVO_CSV = "halloween_vendas.csv"


def main():
    registros = ler_csv(ARQUIVO_CSV)
    print(f"Total de linhas lidas: {len(registros)}")

    # --- Exemplos ANTES -> DEPOIS (um de cada valor diferente) ---
    print("\nCategoria (antes -> depois):")
    vistos = set()
    for reg in registros:
        if reg["categoria"] not in vistos:
            vistos.add(reg["categoria"])
            nova, _ = padronizar_categoria(reg["categoria"])
            print(f"  {reg['categoria']!r} -> {nova!r}")

    print("\nCanal (antes -> depois):")
    vistos = set()
    for reg in registros:
        if reg["canal_venda"] not in vistos:
            vistos.add(reg["canal_venda"])
            novo, _ = padronizar_canal(reg["canal_venda"])
            print(f"  {reg['canal_venda']!r} -> {novo!r}")

    # --- Contagens ---
    cat_preenchidas = 0
    cat_alteradas = 0
    canais_alterados = 0
    canais_desconhecidos = 0

    for reg in registros:
        _, mudanca_cat = padronizar_categoria(reg["categoria"])
        if mudanca_cat == "preenchida":
            cat_preenchidas += 1
        elif mudanca_cat == "alterada":
            cat_alteradas += 1

        _, mudanca_canal = padronizar_canal(reg["canal_venda"])
        if mudanca_canal == "alterada":
            canais_alterados += 1
        elif mudanca_canal == "nao_reconhecido":
            canais_desconhecidos += 1

    print("\nContagens:")
    print(f"  Categorias vazias preenchidas: {cat_preenchidas}")
    print(f"  Categorias não vazias alteradas: {cat_alteradas}")
    print(f"  Canais alterados: {canais_alterados}")
    print(f"  Canais não reconhecidos: {canais_desconhecidos}")

        # --- Sprint 3: validação numérica ---
    problemas_por_campo = {"quantidade": 0, "preco_unitario": 0}
    pedidos_com_problema = 0
    exemplos = []

    for reg in registros:
        problemas = validar_numeros(reg)
        if problemas:                       # lista não vazia = tem problema
            pedidos_com_problema += 1       # conta o PEDIDO uma única vez
            for campo in problemas:
                problemas_por_campo[campo] += 1
            if len(exemplos) < 3:
                exemplos.append((reg["pedido_id"], problemas))

    print("\nValidação numérica:")
    print(f"  Problemas em quantidade: {problemas_por_campo['quantidade']}")
    print(f"  Problemas em preco_unitario: {problemas_por_campo['preco_unitario']}")
    print(f"  Pedidos afetados (sem somar ocorrências): {pedidos_com_problema}")
    print(f"  Exemplos (pedido_id, campos): {exemplos}")

    # --- Sprint 4: datas ---
    datas_invalidas = []
    exemplos_datas = []
    for reg in registros:
        info = converter_data(reg["data_venda"])
        if info is None:
            datas_invalidas.append(reg["pedido_id"])
        elif len(exemplos_datas) < 3:
            exemplos_datas.append((reg["data_venda"], info))

    print("\nDatas:")
    for original, info in exemplos_datas:
        print(f"  {original!r} -> {info['data_br']} "
              f"(ano {info['ano']}, mês {info['mes']}, dia {info['dia']}, hora {info['hora']})")
    print(f"  Datas inválidas ou vazias: {len(datas_invalidas)}")

    # --- Sprint 4: regra de entrega ---
    cancelados, outros = testar_hipotese_entrega(registros)
    print("\nPedidos sem data de entrega:")
    print(f"  Sem entrega e Cancelado: {len(cancelados)}")
    print(f"  Sem entrega e outros status: {len(outros)}")
    if len(outros) == 0:
        print("  Hipótese VERDADEIRA nesta base.")
    else:
        print("  Hipótese FALSA (existem contraexemplos). Até 3 exemplos:")
        for reg in outros[:3]:
            print(f"    pedido {reg['pedido_id']} | status {reg['status_pedido']} "
                  f"| data_venda {reg['data_venda']}")

    # --- Sprint 4: contagens ---
    por_canal, canal_excluidos = contar_por_canal(registros)
    print("\nPedidos por canal:")
    for canal, qtd in por_canal.most_common():
        print(f"  {canal}: {qtd}")
    print(f"  Excluídos (canal não reconhecido): {canal_excluidos}")

    por_periodo, periodo_excluidos = contar_por_ano_mes(registros)
    print("\nPedidos por ano-mês:")
    for periodo in sorted(por_periodo):
        print(f"  {periodo}: {por_periodo[periodo]}")
    print(f"  Excluídos (data inválida): {periodo_excluidos}")

    # --- Relatório final ---
    cancelados_total = 0
    for reg in registros:
        if reg["status_pedido"].strip() == "Cancelado":
            cancelados_total += 1

    exemplos_outros = []
    for reg in outros[:3]:
        exemplos_outros.append(
            f"pedido {reg['pedido_id']} | status {reg['status_pedido']} "
            f"| data_venda {reg['data_venda']}"
        )

    resumo = {
        "total": len(registros),
        "cat_preenchidas": cat_preenchidas,
        "cat_alteradas": cat_alteradas,
        "canais_alterados": canais_alterados,
        "prob_quantidade": problemas_por_campo["quantidade"],
        "prob_preco": problemas_por_campo["preco_unitario"],
        "pedidos_problema": pedidos_com_problema,
        "datas_invalidas": len(datas_invalidas),
        "cancelados_total": cancelados_total,
        "sem_entrega_cancelado": len(cancelados),
        "sem_entrega_outros": len(outros),
        "exemplos_outros": exemplos_outros,
        "por_canal": por_canal,
        "canal_excluidos": canal_excluidos,
        "por_periodo": por_periodo,
        "periodo_excluidos": periodo_excluidos,
    }

    texto = gerar_relatorio(resumo)
    with open("report.md", "w", encoding="utf-8") as saida:
        saida.write(texto + "\n")
    print("\nRelatório salvo em report.md")

if __name__ == "__main__":
    main()

