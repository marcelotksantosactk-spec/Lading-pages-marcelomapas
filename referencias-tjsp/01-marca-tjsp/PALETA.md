# Cores do TJSP (medidas, não chutadas)

Tiradas dos pixels do logo oficial (`logo-tjsp-original.png`, baixado de
https://www.tjsp.jus.br/Download/Imagens/Logo/Logotipo_TJSP_original.png em 28/09/2026).
O CSS do portal do TJSP é Bootstrap genérico e não serve de referência de marca.

| Papel | Cor | De onde vem |
|---|---|---|
| Vermelho do brasão | `#D02020` | campo vermelho do escudo (a cor mais presente no logo) |
| Preto-azulado | `#101820` | listras escuras da bandeira de SP no logo |
| Branco | `#F8F8F8` | listras claras da bandeira |
| Dourado do brasão | `#A89838` | espada, balança e letras "S" e "P" |
| Dourado queimado | `#B07830` | sombras do dourado |

Referências de ambiente (fotos em `../02-fotos-tjsp/`): dourado dos salões e da cúpula,
madeira escura, tapete vermelho, pedra clara da fachada.

A bandeira de São Paulo tem 13 listras horizontais alternadas preto e branco e um retângulo
vermelho no canto; é daí que vêm as listras ao lado do escudo no logo.

## Logo em alta (20/10/2026)

Versão vetorial ou em alta resolução **não encontrada**: o portal do TJSP só serve `Logotipo_TJSP_original.png` (241x129; testei variações de nome .svg/.eps/2x e dão 404), o Wikimedia Commons não tem o logotipo do Tribunal (só o brasão do estado) e o portal não expõe manual de marca. Por isso `logo-tjsp-upscale-6x.png` (1446x774) é o original sobre fundo branco, ampliado 6x (Lanczos) com máscara de nitidez leve (raio 6, 120%). Serve para uso até ~460 px de largura (ampliação efetiva de menos de 2x). Para uso maior, pedir o arquivo ao TJSP.

## Logo em maior resolução (20/10/2026)

Procurei versão em alta/vetor e **não existe** em fonte aberta: o site oficial do TJSP só publica `Logotipo_TJSP_original.png` (241x129, a mesma que já temos; as demais URLs de `/Download/Imagens/Logo/` dão 404), o `apple-touch-icon.png` do portal tem 180x180 (só o escudo, sem as listras), e o Wikimedia Commons não tem o brasão do TJSP (só fotos do edifício; a imagem da Wikipédia para o tribunal é o brasão do Estado, que é outro). Sem login em nada.

`logo-tjsp-emblema-4x.png` (912x304, PNG com alfa): recorte do **emblema** (listras da bandeira + escudo) do `logo-tjsp-original.png`, sem as duas linhas de texto dourado ("TRIBUNAL DE JUSTIÇA" e "3 DE FEVEREIRO DE 1874"), que somem sobre fundo escuro. Ampliado 4x com Lanczos + máscara de nitidez leve; nenhum elemento redesenhado. Nítido até ~450 px de largura na tela do vídeo; acima disso fica macio.
