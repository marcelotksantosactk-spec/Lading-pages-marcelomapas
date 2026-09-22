#!/usr/bin/env bash
# Sobe o public_html deste repositório para a Hostinger (marcelomapas.com).
#
# Uso:
#   ./deploy.sh                      # simulação: mostra o que mudaria, não envia nada
#   ./deploy.sh --pra-valer          # envia de verdade
#   ./deploy.sh --pra-valer penal    # envia só a pasta penal/
#
# NUNCA use --delete aqui. O servidor tem 1,17 GB de vídeo (quiz/video/VLS e
# lp/video/VLS) e o biologia.tar.gz que de propósito NÃO estão neste repositório;
# um rsync com --delete apagaria tudo isso do ar.

set -euo pipefail

CHAVE="$HOME/.ssh/marcelo-hostinger"
SERVIDOR="u759412808@82.180.153.114"
PORTA=65002
REMOTO="domains/marcelomapas.com/public_html"
LOCAL="$(cd "$(dirname "$0")" && pwd)/public_html"

PRA_VALER=""
ALVO=""
for arg in "$@"; do
  case "$arg" in
    --pra-valer) PRA_VALER="sim" ;;
    --*) echo "opção desconhecida: $arg" >&2; exit 1 ;;
    *) ALVO="$arg" ;;
  esac
done

if [ ! -f "$CHAVE" ]; then
  echo "Chave SSH não encontrada em $CHAVE." >&2
  echo "Ela é a chave da TAOS cadastrada no painel da Hostinger do Marcelo." >&2
  exit 1
fi

ORIGEM="$LOCAL/"
DESTINO="$SERVIDOR:$REMOTO/"
if [ -n "$ALVO" ]; then
  ORIGEM="$LOCAL/$ALVO/"
  DESTINO="$SERVIDOR:$REMOTO/$ALVO/"
  [ -d "$LOCAL/$ALVO" ] || { echo "pasta não existe: public_html/$ALVO" >&2; exit 1; }
fi

FLAGS=(-az --no-perms --no-owner --no-group)
[ -n "$PRA_VALER" ] || FLAGS+=(--dry-run)

echo "origem:  $ORIGEM"
echo "destino: $DESTINO"
[ -n "$PRA_VALER" ] && echo ">>> ENVIANDO DE VERDADE" || echo ">>> simulação (use --pra-valer para enviar)"
echo

rsync "${FLAGS[@]}" -v \
  -e "ssh -i $CHAVE -p $PORTA -o BatchMode=yes" \
  "$ORIGEM" "$DESTINO"

echo
if [ -n "$PRA_VALER" ]; then
  echo "Enviado. Confira no ar antes de avisar o cliente."
  [ -n "$ALVO" ] && echo "  https://marcelomapas.com/$ALVO/" || echo "  https://marcelomapas.com/"
else
  echo "Nada foi enviado. Rode de novo com --pra-valer quando estiver certo."
fi
