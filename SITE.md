# O site do Marcelo Mapas neste repositório

`public_html/` é o espelho do site que está no ar em `marcelomapas.com`, hospedado na Hostinger.
Puxado por SSH em 22/09/2026. 188 arquivos, 113 MB.

## Como funciona

Não tem build, não tem framework. Cada produto é uma pasta com um `index.html` de página única:

```
public_html/penal/index.html          -> https://marcelomapas.com/penal/
public_html/constitucional/index.html -> https://marcelomapas.com/constitucional/
public_html/carreiras-policiais/      -> ... também tem up.html, down.html, obrigado.html
public_html/lp/                       -> a landing com VSL (css, js, fonts, img separados)
public_html/quiz/                     -> o quiz (mesma estrutura da lp)
```

Editar = mexer no HTML e subir o arquivo. É isso.

## Os dois comandos

```bash
./sincronizar.sh --pra-valer   # servidor -> aqui (faça ANTES de editar)
./deploy.sh --pra-valer        # aqui -> servidor (sobe pro ar)
```

Sem `--pra-valer` os dois só simulam e mostram o que mudaria. Use isso sempre antes.

Para subir só uma pasta: `./deploy.sh --pra-valer penal`

## O que NÃO está aqui, de propósito

1,45 GB que não cabem no git e continuam vivos só no servidor:

| O quê | Tamanho |
|---|---|
| `quiz/video/VLS` | 586 MB |
| `lp/video/VLS` | 586 MB |
| `biologia` e `biologia.tar.gz` | 135 MB cada |

**Por isso nenhum rsync daqui pode usar `--delete`.** Os dois scripts acima não usam, e não é
para adicionar. Com `--delete`, o primeiro deploy apagaria as duas VSLs do ar.

## Sincronização: o cuidado que importa

O Marcelo mexe no site dele direto pelo painel da Hostinger. Se ele editar uma página lá e você
fizer deploy daqui sem sincronizar antes, o trabalho dele é sobrescrito sem aviso. **Rode
`./sincronizar.sh --pra-valer` antes de começar a editar**, todo dia que for mexer.

## Acesso

Chave SSH da TAOS cadastrada no painel da Hostinger do Marcelo em 22/09/2026, nome
"TAOS Midia - automacao deploy". A chave privada fica em `~/.ssh/marcelo-hostinger` na máquina
do André, fora deste repositório e fora de qualquer git. Servidor: porta 65002, usuário
`u759412808`. Para dar acesso a outra máquina (a do Vitor, por exemplo), gere outra chave
naquela máquina e cadastre a pública no mesmo lugar — não copie a chave privada.

## Deploy automático de verdade (ainda não existe)

Hoje o deploy é um comando. Para virar automático a cada `git push`, o caminho é GitHub Actions
com rsync por SSH, e falta uma coisa só: **acesso de admin neste repositório**, para cadastrar a
chave privada como secret (`gh secret set`). Hoje a TAOS tem `push`, não `admin`. Quando o
Marcelo conceder, o workflow é curto e entra em `.github/workflows/`.

Alternativa: mover a fonte de verdade para um repositório na conta da TAOS, onde já temos admin,
e convidar o Marcelo como colaborador. Decisão do André — a primeira opção mantém o site na mão
do dono, que é o certo a longo prazo.
