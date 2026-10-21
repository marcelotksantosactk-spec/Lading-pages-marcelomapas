"""Scripts de rastreamento que toda página de venda da TAOS no marcelomapas.com leva.

Usado pelos geradores (tjsp-build.py, oab-v2-build.py, portugues-build.py) para os scripts não sumirem
quando uma página é gerada de novo. `instalar(html)` é idempotente: só põe o que ainda não está lá.

- RASTREAMENTO: rastreamento próprio da TAOS (código em ~/dashtaos/tracking, modo direto, sem Worker).
  Grava page_view, checkout, contact e page_exit no banco do dash e põe a identidade do visitante no `sck`
  do link da Kiwify (`tv1.<vid>.<utm>`) e o utm_id no `s1`. Não carrega pixel (as páginas têm o próprio)
  e não manda compra. A chave é pública; a URL e a chave anon do Supabase também (vão no HTML).
  Trocou o t.js? Mude o `?v=` (a Cloudflare guarda arquivo estático).
- REPASSE: reserva da UTMify no clique (commit 98d9dd0). Acrescenta ao link da Kiwify os parâmetros da
  página que o link não tem, sem sobrescrever nada. Vai logo depois da tag da UTMify.
"""

CHAVE = '067ac0999349691af43ab4b2'
VERSAO_T_JS = 'eb01b922'

RASTREAMENTO = (
    '<!-- Rastreamento próprio da TAOS (dash.taosmidia.com): page_view e identidade do visitante no sck do checkout. Não carrega pixel. -->\n'
    '<script>window.__taos={k:"' + CHAVE + '",d:{u:"https://howxazulomyshdrasleh.supabase.co",a:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhvd3hhenVsb215c2hkcmFzbGVoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU0NTAwODksImV4cCI6MjA4MTAyNjA4OX0.iiU8ZzSFB2QSAN3y5N083Ix38BGBQC0w_I_9SRFYWuk"}};</script>\n'
    '<script async src="https://marcelomapas.com/t.js?v=' + VERSAO_T_JS + '"></script>\n'
)

REPASSE = (
    '<!-- Reserva da UTMify: no clique, repassa os parâmetros da página (utm_*, sck, src, fbclid) ao checkout se a UTMify ainda não tiver carregado. Só acrescenta o que o link não tem. -->' + '\n'
    '<script>document.addEventListener(\'click\',function(e){var a=e.target.closest&&e.target.closest(\'a[href*="pay.kiwify.com.br"]\');if(!a)return;try{var u=new URL(a.href),q=new URLSearchParams(location.search);q.forEach(function(v,k){if(!u.searchParams.has(k))u.searchParams.set(k,v)});a.href=u.toString()}catch(err){}},true);</script>' + '\n'
)

UTMIFY = 'cdn.utmify.com.br/scripts/utms/latest.js'
CHARSET = '<meta charset="utf-8">'


def instalar(html):
    """Põe o rastreamento logo depois do primeiro <meta charset> e o repasse logo depois da tag da UTMify."""
    if 'window.__taos=' not in html:
        i = html.index(CHARSET) + len(CHARSET)
        html = html[:i] + '\n' + RASTREAMENTO + html[i:].lstrip('\n')
    if 'Reserva da UTMify' not in html:
        i = html.index(UTMIFY)
        j = html.index('</script>', i) + len('</script>')
        html = html[:j] + '\n' + REPASSE.rstrip('\n') + html[j:]
    assert html.count('window.__taos=') == 1 and html.count('Reserva da UTMify') == 1
    assert html.index('window.__taos=') < html.index('marcelomapas.com/t.js')
    return html
