(function () {
  var STAR_SVG =
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="none" class="h-3.5 w-3.5"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.12 2.12 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.12 2.12 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.12 2.12 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.12 2.12 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.12 2.12 0 0 0 1.597-1.16z"></path></svg>';

  var TESTIMONIALS = [
    { initials: "FS", name: "Felipe Santos", role: "aprovado PM-SP", quote: "Fiz revisão final de Direito Penal em 40 minutos com o mapa. Na apostila levava o dia inteiro. Aprovado na PM-SP." },
    { initials: "CF", name: "Camila Ferreira", role: "aprovada PC-GO", quote: "Estudava trabalhando 8h por dia. Os mapas eram os únicos materiais que funcionavam em 20 minutos de pausa. Passei na PC-GO." },
    { initials: "RO", name: "Rafael Oliveira", role: "aprovado PRF", quote: "Tentei PRF duas vezes sem material visual. Na terceira, usei os Resumos Ilustrados 3.0 na revisão. Aprovado." },
    { initials: "ML", name: "Marcio Lima", role: "candidato PF", quote: "Dois anos de preparação pra PF. Esse material mudou como eu reviso. O mapa de Constitucional sozinho vale o investimento." },
    { initials: "AC", name: "Amanda Costa", role: "aprovada Guarda Municipal", quote: "Meu primeiro concurso. Tinha medo do volume de matéria. Os mapas me deram clareza pra revisar sem travar. Aprovada na Guarda Municipal." },
  ];

  var cardsHtml = TESTIMONIALS.map(function (t) {
    return (
      '<div class="rv"><figure class="card-premium flex h-full flex-col p-6 transition-all duration-200 hover:-translate-y-0.5 hover:border-ember/30">' +
      '<div class="mb-4 flex items-center justify-between"><div class="flex gap-0.5 text-ember" aria-label="5 estrelas">' +
      STAR_SVG + STAR_SVG + STAR_SVG + STAR_SVG + STAR_SVG +
      '</div><span class="font-mono text-[10px] uppercase tracking-wider text-ember/80">Aprovado</span></div>' +
      '<blockquote class="flex-1 text-base leading-relaxed text-bone-300">' + t.quote + '</blockquote>' +
      '<figcaption class="mt-5 flex items-center gap-3 border-t border-white/8 pt-4"><span class="grid h-9 w-9 shrink-0 place-items-center rounded-full border border-ember/40 bg-ember/10 font-mono text-xs font-700 text-ember">' + t.initials + '</span><span class="min-w-0"><span class="block font-display text-sm font-700 text-bone">' + t.name + '</span><span class="block font-mono text-[10px] uppercase tracking-wider text-bone-500">' + t.role + '</span></span></figcaption>' +
      "</figure></div>"
    );
  }).join("");
  document.getElementById("prova-cards").innerHTML = cardsHtml;

  var galleryHtml = "";
  for (var i = 1; i <= 8; i++) {
    galleryHtml +=
      '<div class="w-[72%] shrink-0 snap-center overflow-hidden rounded-lg border border-white/[0.06] sm:w-64">' +
      '<button type="button" data-zoom aria-label="Ampliar imagem: Mensagem de aluno sobre os mapas mentais do Marcelo (' + i + ')" class="group/zoom block w-full cursor-zoom-in">' +
      '<img alt="Mensagem de aluno sobre os mapas mentais do Marcelo (' + i + ')" loading="lazy" width="538" height="521" class="h-auto w-full" src="img/depoimentos/dep-' + i + '.webp" />' +
      "</button></div>";
  }
  document.getElementById("prova-gallery").innerHTML = galleryHtml;
})();
