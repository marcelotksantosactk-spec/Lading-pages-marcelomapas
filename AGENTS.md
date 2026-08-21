# AGENTS.md — Regras globais do projeto

Este arquivo define as regras que **qualquer agente** (Codex, Claude ou outro) deve seguir ao criar, editar ou revisar arquivos neste repositório.

## Princípios gerais

1. **Sempre consultar o Brand System** (`brand/`) antes de criar qualquer material ou página. Cores, fontes, tom de voz e estilo visual não são opcionais.
2. **Sempre consultar a Skill correspondente** (`skills/<nome>/SKILL.md`) antes de produzir aquele tipo de material. Não improvisar um processo que já tem Skill definida.
3. **Nunca inventar conteúdo factual** (legislação, jurisprudência, dados, estatísticas, citações). Quando a fonte não estiver clara, marcar com `[VERIFICAR FONTE]` em vez de inventar.
4. **Um produto por pasta.** Todo material, imagem, mockup, criativo e landing page de um produto específico fica dentro de `produtos/<nome-do-produto>/`, nunca solto na raiz.
5. **Não duplicar padrões.** Se um componente, template ou trecho de copy for reutilizável, ele vai para `templates/` (ou `skills/<skill>/templates/`), não é copiado e colado em cada produto.

## Estrutura de pastas — convenção de nomes

- Pastas em `kebab-case` (minúsculas, sem acentos, hífen entre palavras).
- Cada produto novo é `produtos/produto-NN/` ou um slug descritivo (ex.: `produtos/direito-administrativo-2026/`).
- Toda Skill nova segue o padrão `skills/<nome-da-skill>/SKILL.md`, com `templates/` e `exemplos/` quando fizer sentido.

## Padrões técnicos (para landing pages e materiais web)

- HTML, CSS e JavaScript organizados em arquivos separados por responsabilidade quando o projeto crescer; para uma página única simples, um único arquivo autocontido é aceitável.
- Sempre criar versão **desktop e mobile** (responsivo), nunca apenas uma.
- Sem dependências externas desnecessárias; preferir CSS puro e JS vanilla, a menos que o briefing peça o contrário.
- Sem placeholders visuais no material final (`lorem ipsum`, imagens quebradas, links `#`) — usar os assets reais do produto.

## Fluxo de revisão

1. Codex implementa a partir do briefing e das Skills.
2. O resultado é enviado ao GitHub.
3. Claude revisa conteúdo, estrutura, copy e UX, e devolve um relatório de correções.
4. Codex corrige.
5. Só então o material segue para publicação (Vercel) ou entrega final.

## Limites

- Não remover ou reescrever o Brand System sem indicação explícita do responsável do projeto.
- Não publicar (deploy) sem que a etapa de revisão (`landing-page-review` ou `revisao`) tenha sido concluída.
- Não criar automações em `automacoes/` antes de os fluxos manuais estarem validados (ver seção 16 do documento-base: "Não comece automatizando tudo").
