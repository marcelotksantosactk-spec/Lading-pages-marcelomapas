# Central de Produção Digital

Repositório-base da operação de produção digital com IA (ChatGPT, Codex, Claude, GitHub, Vercel e, futuramente, n8n).

Este repositório é a fonte central de verdade para:

- **Materiais didáticos**: mapas mentais, resumos ilustrados, apostilas, questões comentadas e mnemônicos.
- **Materiais comerciais**: mockups, criativos de anúncios, copy de vendas e landing pages.
- **Automação**: regras que Codex e Claude seguem para implementar, revisar e publicar cada produto.

## Como este repositório funciona

1. Todo padrão de marca (cores, fontes, linguagem, estilo visual) vive em [`brand/`](./brand).
2. Toda regra de produção reutilizável vive em [`skills/`](./skills), uma pasta por Skill, cada uma com seu `SKILL.md`.
3. Cada produto (curso, apostila, landing page) vive em sua própria pasta dentro de [`produtos/`](./produtos), isolado dos demais.
4. Componentes e layouts reaproveitáveis entre produtos vivem em [`templates/`](./templates).
5. Fluxos de automação (n8n, scripts, webhooks) vivem em [`automacoes/`](./automacoes), e só devem ser criados depois que os fluxos manuais estiverem validados.
6. [`AGENTS.md`](./AGENTS.md) define as regras globais que o Codex (e qualquer outro agente que edite este repositório) deve seguir.

## Estrutura de pastas

```
producao-digital/
│
├── AGENTS.md
├── README.md
│
├── brand/
│   ├── brand-guide.md
│   ├── cores.md
│   ├── tipografia.md
│   ├── linguagem.md
│   ├── estilo-visual.md
│   ├── logos/
│   └── exemplos/
│
├── skills/
│   ├── brand-system/
│   ├── pesquisa-conteudo/
│   ├── resumo-ilustrado/
│   ├── mapa-mental/
│   ├── apostila/
│   ├── questoes-comentadas/
│   ├── revisao/
│   ├── imagem-didatica/
│   ├── mockup-produto/
│   ├── copy-vendas/
│   ├── landing-page-builder/
│   ├── criativos-ads/
│   └── landing-page-review/
│
├── produtos/
│   └── produto-01/
│
├── templates/
└── automacoes/
```

## Fluxo geral

```
VOCÊ → CHATGPT → BIBLIOTECA DE SKILLS → CODEX → GITHUB → CLAUDE (revisão) → VERCEL → SITE ONLINE
```

## Estado atual do projeto

- [x] Repositório criado
- [x] Estrutura de pastas principal
- [x] Brand System (v1 — a validar com exemplos reais da marca)
- [x] Skill `resumo-ilustrado`
- [x] Skill `mapa-mental`
- [x] Skill `landing-page-builder`
- [ ] Skills restantes (`pesquisa-conteudo`, `apostila`, `questoes-comentadas`, `revisao`, `imagem-didatica`, `mockup-produto`, `copy-vendas`, `criativos-ads`, `landing-page-review`)
- [ ] Primeiro produto real em `produtos/`
- [ ] Conexão com Codex
- [ ] Conexão com Vercel
- [ ] Automação com n8n

## Documento de referência

A visão completa do projeto (arquitetura, skills, fluxos e prompts prontos) está em `projeto_producao_digital_skills.html`, o documento-base que originou este repositório.
