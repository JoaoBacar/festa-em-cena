# Relatório - Festa em Cena (Halloween)

## 1. Qualidade dos dados
- Total de linhas lidas: 1500
- Categorias vazias preenchidas com "sem categoria": 18
- Categorias não vazias padronizadas: 1482
- Canais padronizados: 45
- Problemas em quantidade: 7
- Problemas em preco_unitario: 12
- Pedidos afetados por problema numérico (sem somar ocorrências): 19
- Datas de venda inválidas ou vazias: 4
- Total de pedidos cancelados: 109

## 2. Pedidos sem data de entrega
- Sem entrega e Cancelado: 109
- Sem entrega e outros status: 34
- Hipótese "sem entrega = Cancelado": FALSA (existem contraexemplos).
- Exemplos de pedidos sem entrega que não estão cancelados:
  - pedido 1170 | status Concluído | data_venda 2025-08-19 22:20:19
  - pedido 990 | status Concluído | data_venda 2025-10-13 20:00:16
  - pedido 740 | status Concluído | data_venda data_invalida

## 3. Contagens (pedidos registrados, todos os status)
### Por canal
- Web: 666
- Loja física: 551
- Mercado: 283
- Excluídos (canal não reconhecido): 0

### Por ano-mês
- 2024-08: 77
- 2024-09: 104
- 2024-10: 393
- 2024-11: 174
- 2025-08: 62
- 2025-09: 94
- 2025-10: 410
- 2025-11: 182
- Excluídos (data inválida): 4

