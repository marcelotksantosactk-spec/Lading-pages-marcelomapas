#!/usr/bin/env bash
# Puxa o public_html da Hostinger para este repositório.
#
# Use antes de editar, sempre que houver chance de o Marcelo ter mexido direto
# no servidor — senão o deploy sobrescreve o que ele fez.
#
# Uso:
#   ./sincronizar.sh             # simulação
#   ./sincronizar.sh --pra-valer # puxa de verdade

set -euo pipefail

CHAVE="$HOME/.ssh/marcelo-hostinger"
SERVIDOR="u759412808@82.180.153.114"
PORTA=65002
REMOTO="domains/marcelomapas.com/public_html"
LOCAL="$(cd "$(dirname "$0")" && pwd)/public_html"

PRA_VALER=""
[ "${1:-}" = "--pra-valer" ] && PRA_VALER="sim"

FLAGS=(-az --no-perms --no-owner --no-group)
[ -n "$PRA_VALER" ] || FLAGS+=(--dry-run)

# os mesmos excluídos do repositório: vídeos e tarballs grandes demais para o git
rsync "${FLAGS[@]}" -v \
  -e "ssh -i $CHAVE -p $PORTA -o BatchMode=yes" \
  --exclude='video/VLS' --exclude='*.tar.gz' --exclude='biologia' \
  --exclude='.trash' --exclude='*.mov' \
  "$SERVIDOR:$REMOTO/" "$LOCAL/"

echo
[ -n "$PRA_VALER" ] && echo "Puxado. Veja o 'git status' para o que mudou no servidor." \
  || echo "Simulação. Rode com --pra-valer para puxar."
