---
name: brand-system
description: Aplica cores, fontes, estilo e regras visuais da marca a qualquer material ou página gerada.
---

# Objetivo

Garantir que todo material e página produzidos (didáticos ou comerciais) sigam o mesmo padrão visual e editorial, definido em `brand/`.

# Entradas

- tipo de material (mapa mental, resumo, apostila, questão, mockup, criativo, landing page)
- meio de saída (web, PDF, imagem, impresso)
- se é material didático ou comercial

# Processo

1. Ler `brand/brand-guide.md` para confirmar posicionamento e público.
2. Ler `brand/cores.md` e aplicar a paleta correta para a aplicação (didático vs. comercial, ver tabela "Paleta por aplicação").
3. Ler `brand/tipografia.md` e aplicar a hierarquia de tamanhos/pesos adequada ao meio de saída.
4. Ler `brand/linguagem.md` e ajustar o tom (didático ou comercial) do texto gerado.
5. Ler `brand/estilo-visual.md` e aplicar os padrões de composição (cards, boxes, ícones, espaçamento).
6. Se algum pedido do usuário conflitar com uma regra do Brand System, sinalizar o conflito antes de prosseguir, em vez de simplesmente ignorar a regra ou o pedido.
7. Se `brand/exemplos/` tiver materiais aprovados, usá-los como referência visual adicional.

# Regras

- Nunca usar cores fora da paleta definida em `cores.md` sem justificativa explícita.
- Nunca misturar o tom didático com o tom comercial dentro do mesmo bloco de texto (ex.: uma explicação de conceito não deve soar como anúncio).
- Marcar com `[VERIFICAR]` qualquer informação de marca que ainda não esteja definida (nome oficial, nicho exato, logo) em vez de presumir.

# Saída

- Confirmação de quais regras de marca foram aplicadas (cores, fonte, tom, composição).
- Lista de eventuais conflitos ou lacunas encontradas no Brand System durante a aplicação.
