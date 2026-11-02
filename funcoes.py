import csv
import re
from datetime import datetime
from collections import Counter

SEM_CATEGORIA = "sem categoria"

# Canais aceitos
CANAIS_VALIDOS = {
    "mercado": "Mercado",
    "loja física": "Loja física",
    "web": "Web",
}

FORMATO_ENTRADA = "%Y-%m-%d %H:%M:%S"   # ex.: 2025-10-12 14:35:00
FORMATO_BR = "%d/%m/%Y"                 # ex.: 12/10/2025


def ler_csv(caminho):
    """Lê o CSV com csv.DictReader.

    Cada linha vira um dicionário {coluna: valor}.
    Todos os valores chegam como TEXTO (str), mesmo números e datas.
    """
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=",")
        return list(leitor)


def padronizar_texto(texto):
    texto = texto.strip().lower()             
    texto = re.sub(r"[^\w\s]|_", "", texto)   
    texto = re.sub(r"\s+", " ", texto)        
    return texto.strip()


def padronizar_categoria(original):
    limpa = padronizar_texto(original)

    if limpa == "":
        if original.strip() == "":
            return SEM_CATEGORIA, "preenchida"   
        return SEM_CATEGORIA, "alterada"        

    if limpa != original:
        return limpa, "alterada"
    return limpa, "igual"


def padronizar_canal(original):
    """Retorna (canal_padrao, tipo_de_mudanca). Canal desconhecido -> None."""
    chave = padronizar_texto(original)

    if chave not in CANAIS_VALIDOS:
        return None, "nao_reconhecido"

    canal = CANAIS_VALIDOS[chave]
    if canal != original:
        return canal, "alterada"
    return canal, "igual"

def validar_numeros(registro):
    """Valida quantidade e preco_unitario de UM registro.

    Regras:
    - quantidade: precisa ser inteiro maior que zero.
    - preco_unitario: precisa estar preenchido e não ser negativo.

    Retorna a lista de campos com problema, ex.: ["quantidade"].
    Lista vazia = registro válido.
    """
    problemas = []

    # quantidade: converte de texto para inteiro; se não der, é problema
    try:
        quantidade = int(registro["quantidade"].strip())
        if quantidade <= 0:
            problemas.append("quantidade")
    except ValueError:
        problemas.append("quantidade")

    # preco_unitario: vazio é problema; senão converte para número
    preco_texto = registro["preco_unitario"].strip()
    if preco_texto == "":
        problemas.append("preco_unitario")
    else:
        try:
            if float(preco_texto) < 0:
                problemas.append("preco_unitario")
        except ValueError:
            problemas.append("preco_unitario")

    return problemas

#sprint 4
def converter_data(texto):
    """Converte data_venda (texto) para datetime e extrai as partes.

    Retorna um dicionário com ano, mes, dia, hora, data_br e ano_mes.
    Se a data for vazia ou inválida, retorna None (NÃO inventa data).
    """
    try:
        data = datetime.strptime(texto.strip(), FORMATO_ENTRADA)
    except ValueError:
        return None

    return {
        "ano": data.year,
        "mes": data.month,
        "dia": data.day,
        "hora": data.hour,
        "data_br": data.strftime(FORMATO_BR),
        "ano_mes": data.strftime("%Y-%m"),
    }


def entrega_vazia(registro):
    """True se data_entrega estiver vazia (só espaços também conta)."""
    return registro["data_entrega"].strip() == ""


def testar_hipotese_entrega(registros):
    """Hipótese: TODO pedido com data_entrega vazia está 'Cancelado'.

    Retorna dois grupos de pedidos sem entrega:
    (cancelados, outros_status).
    Se 'outros_status' tiver algum pedido, a hipótese é FALSA.
    """
    cancelados = []
    outros_status = []
    for reg in registros:
        if entrega_vazia(reg):
            if reg["status_pedido"].strip() == "Cancelado":
                cancelados.append(reg)
            else:
                outros_status.append(reg)
    return cancelados, outros_status


def contar_por_canal(registros):
    """Conta pedidos por canal padronizado (todos os status).

    Retorna (contagem, excluidos). Excluídos = canal não reconhecido.
    """
    contagem = Counter()
    excluidos = 0
    for reg in registros:
        canal, _ = padronizar_canal(reg["canal_venda"])
        if canal is None:
            excluidos += 1
        else:
            contagem[canal] += 1
    return contagem, excluidos


def contar_por_ano_mes(registros):
    """Conta pedidos por 'AAAA-MM' usando data_venda válida (todos os status).

    Usa ano-mês (e não só mês) para NÃO misturar 2024 com 2025.
    Retorna (contagem, excluidos). Excluídos = data inválida ou vazia.
    """
    contagem = Counter()
    excluidos = 0
    for reg in registros:
        info = converter_data(reg["data_venda"])
        if info is None:
            excluidos += 1
        else:
            contagem[info["ano_mes"]] += 1
    return contagem, excluidos

#funcao de relatorio

def gerar_relatorio(resumo):
    """Monta o texto do relatório (Markdown) a partir de um dicionário de números."""
    linhas = []
    linhas.append("# Relatório - Festa em Cena (Halloween)")
    linhas.append("")
    linhas.append("## 1. Qualidade dos dados")
    linhas.append(f"- Total de linhas lidas: {resumo['total']}")
    linhas.append(f"- Categorias vazias preenchidas com \"{SEM_CATEGORIA}\": {resumo['cat_preenchidas']}")
    linhas.append(f"- Categorias não vazias padronizadas: {resumo['cat_alteradas']}")
    linhas.append(f"- Canais padronizados: {resumo['canais_alterados']}")
    linhas.append(f"- Problemas em quantidade: {resumo['prob_quantidade']}")
    linhas.append(f"- Problemas em preco_unitario: {resumo['prob_preco']}")
    linhas.append(f"- Pedidos afetados por problema numérico (sem somar ocorrências): {resumo['pedidos_problema']}")
    linhas.append(f"- Datas de venda inválidas ou vazias: {resumo['datas_invalidas']}")
    linhas.append(f"- Total de pedidos cancelados: {resumo['cancelados_total']}")
    linhas.append("")
    linhas.append("## 2. Pedidos sem data de entrega")
    linhas.append(f"- Sem entrega e Cancelado: {resumo['sem_entrega_cancelado']}")
    linhas.append(f"- Sem entrega e outros status: {resumo['sem_entrega_outros']}")
    if resumo["sem_entrega_outros"] == 0:
        linhas.append("- Hipótese \"sem entrega = Cancelado\": VERDADEIRA nesta base.")
    else:
        linhas.append("- Hipótese \"sem entrega = Cancelado\": FALSA (existem contraexemplos).")
        linhas.append("- Exemplos de pedidos sem entrega que não estão cancelados:")
        for texto in resumo["exemplos_outros"]:
            linhas.append(f"  - {texto}")
    linhas.append("")
    linhas.append("## 3. Contagens (pedidos registrados, todos os status)")
    linhas.append("### Por canal")
    for canal, qtd in resumo["por_canal"].most_common():
        linhas.append(f"- {canal}: {qtd}")
    linhas.append(f"- Excluídos (canal não reconhecido): {resumo['canal_excluidos']}")
    linhas.append("")
    linhas.append("### Por ano-mês")
    for periodo in sorted(resumo["por_periodo"]):
        linhas.append(f"- {periodo}: {resumo['por_periodo'][periodo]}")
    linhas.append(f"- Excluídos (data inválida): {resumo['periodo_excluidos']}")
    linhas.append("")
    linhas.append("> Estas contagens representam pedidos registrados, não receita nem vendas concluídas.")
    return "\n".join(linhas)