# Festa em Cena – Análise de Pedidos de Halloween

Mini-Projeto Avaliativo – Machine Learning e Visão Computacional (Turma 04) – Módulo 1, Semana 07.

## 1. Descrição do Projeto

**O problema.** A Festa em Cena é uma rede fictícia que vende fantasias e acessórios de Halloween pelos canais
**Mercado** (caixas de supermercados parceiros), **Loja física** (lojas próprias) e **Web** (site). A empresa tem
registros bagunçados: categorias vazias ou com pontuação, quantidades inválidas, preços ausentes e datas inválidas.

**Objetivo do programa.** Ler, organizar e explorar o CSV usando **somente a biblioteca padrão do Python**
(`csv`, `re`, `datetime`, `collections`), gerando um relatório simples antes de comparar os períodos de venda.

**Significado de uma linha e das colunas principais.** Cada linha é **um pedido distinto** de **um produto**
(que pode ter várias unidades). Colunas usadas:
- `data_venda`: data/hora do pedido (fuso local de São Paulo, sem fuso explícito).
- `canal_venda`: Mercado, Loja física ou Web.
- `categoria`: Fantasia ou Acessorio (pode vir vazia ou "suja").
- `quantidade` e `preco_unitario`: validados (quantidade inteira > 0; preço preenchido e não negativo).
- `status_pedido` e `data_entrega`: usados na regra de negócio.

Custos e descontos (`custo_unitario`, `desconto_pct`) estão no CSV, mas **não foram usados** (uso opcional).

**Regras adotadas**
- **Textos:** `strip()` + `lower()` + `re.sub` para remover pontuação preservando letras e espaços. Categoria vazia
  (ou que fica vazia após a limpeza) vira `"sem categoria"`. `canal_venda` é padronizado para Mercado / Loja física / Web.
- **Valores:** `quantidade` precisa ser inteiro > 0; `preco_unitario` precisa estar preenchido e ser ≥ 0. Registros com
  problema são **marcados** (nada é inventado ou corrigido) e o processamento **continua**.
- **Datas:** `data_venda` é convertida com `datetime.strptime("%Y-%m-%d %H:%M:%S")`; o texto original é preservado, extraímos
  ano/mês/dia/hora e formatamos com `strftime("%d/%m/%Y")`. Datas inválidas/vazias são marcadas e excluídas só das
  contagens por período (nunca trocadas pela data de hoje).
- O CSV original **não é modificado**.

## 2. Guia de Execução

**Arquivos necessários (mesma pasta):** `main.py`, `funcoes.py` e `halloween_vendas.csv`.

```bash
python main.py
```

Requer Python 3 (sem instalar bibliotecas). O programa imprime o relatório no terminal e salva o arquivo `report.md`.

## 3. Resultados

| Item | Resultado |
|---|---|
| Linhas lidas | 1500 |
| Categorias vazias preenchidas com "sem categoria" | 18 |
| Categorias não vazias alteradas | 1482 (1351 só trocaram maiúscula/minúscula; 131 tinham espaços/pontuação) |
| Canais padronizados | 45 |
| Problemas numéricos | `quantidade` = 7; `preco_unitario` = 12 → **19 pedidos afetados** |
| Datas de venda inválidas | 4 |
| Pedidos cancelados | 109 |
| Sem `data_entrega` e Cancelado | 109 |
| Sem `data_entrega` e outro status | 34 (todos "Concluído") |

### Conclusão sobre entrega sem data
Hipótese: *"todo pedido com `data_entrega` vazia está Cancelado"*. **É FALSA nesta base.** Há 143 pedidos sem entrega:
109 cancelados e **34 "Concluído"** (contraexemplos). Exemplos: pedidos 1170, 990 e 740. Não alteramos o status nem inventamos datas.

### Descoberta 1 – Por canal (pedidos registrados, todos os status, canais reconhecidos; 0 excluídos)
Web 666 (44,4%), Loja física 551 (36,7%), Mercado 283 (18,9%).
- **Interpretação:** o site concentra quase metade dos pedidos; o Mercado é o menor canal.
- **Limitação:** conta pedidos, não unidades, receita nem vendas concluídas; inclui cancelados e devolvidos.

### Descoberta 2 – Por ano-mês (`data_venda` válida; 4 excluídas)
| Mês | 2024 | 2025 |
|---|---|---|
| Ago | 77 | 62 |
| Set | 104 | 94 |
| **Out** | **393** | **410** |
| Nov | 174 | 182 |

- **Interpretação:** outubro (mês do Halloween) concentra cerca de 40% dos pedidos em ambos os anos e é o pico, com
  queda forte em novembro. 2025 foi um pouco acima de 2024 em outubro/novembro (e abaixo em ago/set).
- **Limitação:** contagem de pedidos registrados (não receita); a base é fictícia e tem só 4 meses por ano;
  as 4 datas inválidas ficaram fora.

## 4. Reflexão: ML e qualidade de dados
Antes de usar dados em Machine Learning é preciso verificar ausentes, textos inconsistentes e datas inválidas, pois a
qualidade dos dados influencia as análises e os modelos (lixo entra, lixo sai). Limpeza não garante bons modelos:
também importam representatividade, escolha do modelo e avaliação, para evitar overfitting e underfitting.
Aqui, por exemplo, a hipótese "sem entrega = cancelado" parecia razoável, mas os dados a contradisseram.
