"""Monta o padrão de fundo (ícones de tribunal em traço fino, estilo Gaby no Tribunal)
a partir dos ícones da Tabler (MIT). Gera um ladrilho SVG que repete sem emenda."""
import re, random
ICONES = ['scale', 'gavel', 'building-bank', 'book', 'feather', 'certificate', 'writing-sign', 'license']
T = 440


def corpo(nome):
    s = open(f'{nome}.svg').read()
    return ''.join(p for p in re.findall(r'<path[^>]*/>', s) if 'stroke="none"' not in p)


def ladrilho(cor, opacidade, saida, semente=7):
    random.seed(semente)
    pos = [(60, 70), (230, 40), (370, 120), (120, 220), (300, 250), (40, 360), (200, 380), (380, 350)]
    g = []
    for (x, y), nome in zip(pos, ICONES):
        tam = random.choice([46, 54, 62])
        rot = random.uniform(-18, 18)
        k = tam / 24
        for dx in (0, -T, T):
            for dy in (0, -T, T):
                g.append(f'<g transform="translate({x+dx} {y+dy}) rotate({rot:.1f}) scale({k:.2f}) translate(-12 -12)">{corpo(nome)}</g>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{T}" height="{T}" viewBox="0 0 {T} {T}">'
           f'<g fill="none" stroke="{cor}" stroke-opacity="{opacidade}" stroke-width="0.65" '
           f'stroke-linecap="round" stroke-linejoin="round">{"".join(g)}</g></svg>')
    open(saida, 'w').write(svg)


if __name__ == '__main__':
    ladrilho('#8C7A2E', 0.22, 'padrao-claro.svg')
    ladrilho('#E3C766', 0.10, 'padrao-escuro.svg', semente=11)
    print('ok')
