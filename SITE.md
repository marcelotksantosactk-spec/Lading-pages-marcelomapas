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

## Deploy automático

O workflow já está escrito em `.github/workflows/deploy.yml`: a cada push na `main` que mexa em
`public_html/`, ele faz o mesmo rsync do `deploy.sh` e depois confere se o site respondeu 200.

**Falta uma coisa só para ligar:** o secret `SSH_PRIVATE_KEY` com a chave privada da TAOS. Criar
secret exige acesso **admin** neste repositório, que a TAOS ainda não tem (só `push`). Sem o
secret o workflow sai sem fazer nada, de propósito, em vez de falhar a cada push. Quando o
Marcelo conceder admin:

```bash
gh secret set SSH_PRIVATE_KEY < ~/.ssh/marcelo-hostinger
```

Até lá, `./deploy.sh --pra-valer` faz exatamente a mesma coisa, em um comando.

## Por que NÃO usamos o deploy nativo da Hostinger (Avançado > GIT)

A Hostinger tem deploy a partir do GitHub no painel, e à primeira vista era o caminho óbvio. A
documentação dela diz duas coisas que matam a ideia para este site:

1. **"O diretório de destino precisa estar vazio para o primeiro deploy."** Conectar no
   `public_html` exigiria **esvaziar a pasta inteira antes** — o site sai do ar e os 1,45 GB de
   vídeo e tarball somem junto.
2. **"Substitui os arquivos existentes naquele diretório a cada deploy."** A pasta passa a ser
   controlada pelo repositório, e o que o Marcelo subir pelo painel dele vira passageiro.

O rsync dos scripts daqui faz o mesmo trabalho sem nenhuma das duas coisas: não exige pasta
vazia, não apaga o que não está no repositório, e convive com o Marcelo editando pelo painel.

Documentação consultada em 22/09/2026: https://docs.hostinger.com/websites/git

## Backup dos arquivos pesados

Feito em 22/09/2026, dentro do próprio servidor, em `~/backup-taos-20260922` (1,5 GB): as duas
VSLs e os dois `biologia.tar.gz`. Se algum dia algo apagar esses arquivos do `public_html`,
restaurar é uma cópia local no servidor, questão de segundos — não precisa reenviar 1,2 GB pela
internet.
