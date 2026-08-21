---
name: tipografia
description: Fontes, pesos, hierarquia e tamanhos recomendados.
status: rascunho v1 — baseado no padrão visual do documento-base
---

# Tipografia

## ⚠️ Status

Baseado na stack tipográfica do documento-base. Ajuste se a marca já tiver uma fonte definida (ex.: fonte da logo).

## Família tipográfica

- **Principal**: `Inter` (com fallback `ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif`).
- **Código / valores técnicos**: monoespaçada (`SFMono-Regular, Consolas, "Liberation Mono", monospace`) — usar apenas em blocos técnicos (fórmulas, artigos de lei citados literalmente, código).

`[VERIFICAR]`: se a marca tiver identidade visual própria com outra fonte, substituir aqui e propagar para `estilo-visual.md`.

## Hierarquia e tamanhos (referência web/responsivo)

| Nível | Uso | Tamanho aprox. | Peso |
|---|---|---|---|
| H1 | Título de hero / capa | `clamp(36px, 6vw, 68px)` | 800 (extra bold) |
| H2 | Título de seção | 28–30px | 700 (bold) |
| H3 | Subtítulo / título de card | 20–21px | 700 (bold) |
| Corpo | Texto corrido | 15–16px | 400 (regular) |
| Lead / destaque | Parágrafo de abertura | 18–19px | 400–500 |
| Legenda / metadado | Datas, tags, notas de rodapé | 12–13px | 600–700 |

## Regras de uso

1. Nunca mais de 3 níveis de hierarquia visíveis na mesma tela (ex.: H2 + H3 + corpo).
2. Títulos sempre com peso alto (700+); nunca títulos em peso regular.
3. Line-height confortável para leitura densa: **1.5–1.7** no corpo de texto, especialmente em materiais didáticos longos (apostilas, resumos).
4. Em materiais impressos/PDF, manter proporção equivalente (ex.: H1 24–32pt, corpo 10–11pt), ajustando para a mídia.
5. Tags, badges e rótulos (`.tag`, `.badge`) usam caixa alta ou peso 700 com leve `letter-spacing` para diferenciar de texto corrido.
