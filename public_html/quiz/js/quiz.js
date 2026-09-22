(function () {
  var BTN_BASE =
    "group inline-flex items-center justify-center gap-2.5 font-display font-700 uppercase tracking-[0.1em] cursor-pointer transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ember focus-visible:ring-offset-2 focus-visible:ring-offset-carbon-950 bg-grass text-carbon-950 hover:bg-grass-400 shadow-glowGreen hover:shadow-glowGreenLg hover:-translate-y-0.5 px-8 py-4 text-sm rounded-md";
  var ARROW_SVG =
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"><path d="M5 12h14M12 5l7 7-7 7"></path></svg>';
  var CHECK_SVG =
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4"><path d="M20 6 9 17l-5-5"></path></svg>';

  var QUESTIONS = [
    {
      screen: 1,
      question: "Qual concurso policial é seu foco agora?",
      progress: 20,
      options: [
        { label: "Polícia Militar (PM estadual)" },
        { label: "Polícia Civil (PC estadual)" },
        { label: "Polícia Rodoviária Federal (PRF)" },
        { label: "Polícia Federal (PF)" },
        { label: "Guarda Municipal ou outro" },
      ],
    },
    {
      screen: 2,
      question: "Há quanto tempo você está se preparando para esse concurso?",
      progress: 40,
      options: [
        { label: "Menos de 3 meses" },
        { label: "De 3 a 6 meses" },
        { label: "De 6 meses a 1 ano", tags: ["experiente"] },
        { label: "Mais de 1 ano", tags: ["experiente"] },
      ],
    },
    {
      screen: 3,
      question: "Neste momento da preparação, o que mais te preocupa?",
      progress: 60,
      options: [
        { label: "Não consigo revisar tudo a tempo", tags: ["retencao-critica"] },
        { label: "Leio muito mas não retenho na hora da prova", tags: ["retencao-critica"] },
        { label: "Não tenho material organizado por disciplina" },
        { label: "Pouco tempo disponível para estudar" },
      ],
    },
    {
      screen: 4,
      question: "Das 12 disciplinas do concurso, quantas você já estudou pelo menos uma vez?",
      progress: 80,
      options: [
        { label: "De 1 a 4 disciplinas" },
        { label: "De 5 a 8 disciplinas" },
        { label: "De 9 a 11 disciplinas", tags: ["reta-final"] },
        { label: "Todas as 12", tags: ["reta-final"] },
      ],
    },
    {
      screen: 5,
      question: "Qual é seu método principal de revisão hoje?",
      progress: 100,
      options: [
        { label: "Releitura de apostila ou livro" },
        { label: "Resumos em texto que eu mesmo faço" },
        { label: "Mapas mentais ou material visual", tags: ["ja-visual"] },
        { label: "Não tenho um método fixo" },
      ],
    },
  ];

  var CALC_STEPS = [
    "Analisando suas disciplinas...",
    "Verificando nível de prontidão...",
    "Preparando seu diagnóstico personalizado...",
  ];
  var CALC_DURATION_MS = 3600;

  var RESULT_BODY = [
    "Você já cobriu boa parte do conteúdo. O problema não é falta de estudo: é o método de revisão. Releitura de apostila não cria âncora visual — você lê, o prazo se aproxima, e o conteúdo não fica consolidado na hora da prova.",
    "Candidatos que chegam preparados revisam com material visual que o cérebro processa como estrutura, não como texto corrido. Uma disciplina inteira em 20 minutos, não em um dia.",
    "Assista ao vídeo acima. Ele mostra como os Resumos Ilustrados 3.0 resolvem exatamente o que o seu diagnóstico apontou.",
  ];
  var RESULTS = {
    principal: { title: "Diagnóstico: Candidato com Conteúdo Pronto e Revisão em Risco", body: RESULT_BODY },
    secundario: { title: "Diagnóstico: Candidato com Base Sólida e Potencial de Aceleração", body: RESULT_BODY },
    cta: "Quero meu Combo Policial agora",
  };

  var state = { screen: "intro", step: 0, answers: {}, resultStep: 0 };
  var root = document.getElementById("quiz-root");

  function letterFor(i) {
    return String.fromCharCode(65 + i);
  }

  function renderIntro() {
    root.innerHTML =
      '<div class="q-screen text-center">' +
      '<span class="mx-auto grid h-16 w-16 place-items-center rounded-2xl border border-ember/40 bg-ember/10 text-ember"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="h-8 w-8"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg></span>' +
      '<span class="mt-6 block stamp text-ember">Diagnóstico de prontidão</span>' +
      '<h1 class="mt-4 font-display text-4xl font-800 leading-tight sm:text-5xl">Descubra se você vai chegar preparado na sua prova policial</h1>' +
      '<p class="mx-auto mt-4 max-w-md text-base leading-relaxed text-bone-300">Responda 5 perguntas e receba um diagnóstico do seu nível de prontidão para o concurso.</p>' +
      '<button type="button" class="' +
      BTN_BASE +
      ' mt-8 q-start"><span>Iniciar diagnóstico</span>' +
      ARROW_SVG +
      "</button>" +
      '<p class="mt-5 font-mono text-[10px] uppercase tracking-wider text-bone-500">Menos de 1 minuto · 5 perguntas</p>' +
      "</div>";
    root.querySelector(".q-start").addEventListener("click", function () {
      state.screen = "question";
      state.step = 0;
      render();
    });
  }

  function renderQuestion() {
    var q = QUESTIONS[state.step];
    var selected = state.answers[q.screen];
    var optionsHtml = q.options
      .map(function (opt, i) {
        var isSel = selected === i;
        return (
          '<button type="button" class="group flex w-full cursor-pointer items-center gap-4 rounded-xl border p-5 text-left transition-all duration-200 hover:-translate-y-0.5 ' +
          (isSel ? "border-ember bg-ember/10" : "border-white/10 bg-carbon-800/60 hover:border-ember/50 hover:bg-carbon-800") +
          '" data-idx="' +
          i +
          '"><span class="grid h-9 w-9 shrink-0 place-items-center rounded-lg border font-mono text-sm font-700 transition-colors ' +
          (isSel ? "border-ember bg-ember text-carbon-950" : "border-white/20 text-bone-500 group-hover:border-ember/60") +
          '">' +
          (isSel ? CHECK_SVG : letterFor(i)) +
          '</span><span class="text-lg text-bone-300 group-hover:text-bone">' +
          opt.label +
          '</span><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="ml-auto h-4 w-4 shrink-0 text-bone-700 opacity-0 transition-all duration-200 group-hover:translate-x-1 group-hover:opacity-100"><path d="M5 12h14M12 5l7 7-7 7"></path></svg></button>'
        );
      })
      .join("");

    root.innerHTML =
      '<div class="q-screen">' +
      '<div class="mb-8 flex items-center gap-4">' +
      '<button type="button" class="font-mono text-xs text-bone-500 transition-colors hover:text-bone q-back">← Voltar</button>' +
      '<div class="flex-1"><div class="h-1.5 w-full overflow-hidden rounded-full bg-white/10"><div class="h-full bg-ember q-progress-fill" style="width:' +
      q.progress +
      '%"></div></div></div>' +
      '<span class="font-mono text-xs tabular-nums text-bone-500">' +
      (state.step + 1) +
      "/" +
      QUESTIONS.length +
      "</span></div>" +
      '<h2 class="font-display text-3xl font-800 leading-snug sm:text-4xl">' +
      q.question +
      "</h2>" +
      '<div class="mt-8 space-y-4">' +
      optionsHtml +
      "</div></div>";

    root.querySelector(".q-back").addEventListener("click", function () {
      if (state.step > 0) {
        state.step -= 1;
        render();
      } else {
        state.screen = "intro";
        render();
      }
    });

    root.querySelectorAll("[data-idx]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var idx = parseInt(btn.getAttribute("data-idx"), 10);
        state.answers[q.screen] = idx;
        if (state.step < QUESTIONS.length - 1) {
          state.step += 1;
          render();
        } else {
          state.screen = "calculating";
          render();
        }
      });
    });
  }

  function renderCalculating() {
    root.innerHTML =
      '<div class="q-screen text-center">' +
      '<div class="relative mx-auto h-24 w-24"><svg class="h-24 w-24 q-spinner-svg" viewBox="0 0 100 100">' +
      '<circle cx="50" cy="50" r="44" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="6"></circle>' +
      '<circle class="q-spinner-arc" cx="50" cy="50" r="44" fill="none" stroke="#FF910C" stroke-width="6" stroke-linecap="round"></circle>' +
      "</svg></div>" +
      '<h2 class="mt-8 font-display text-2xl font-800">Calculando seu diagnóstico de prontidão...</h2>' +
      '<div class="mt-5 h-6"><p class="font-mono text-xs uppercase tracking-wider text-ember q-calc-step"></p></div>' +
      "</div>";

    var arc = root.querySelector(".q-spinner-arc");
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        arc.style.strokeDashoffset = "0";
      });
    });

    var stepEl = root.querySelector(".q-calc-step");
    var i = 0;
    stepEl.textContent = CALC_STEPS[0];
    var interval = setInterval(function () {
      i = Math.min(i + 1, CALC_STEPS.length - 1);
      stepEl.textContent = CALC_STEPS[i];
    }, CALC_DURATION_MS / CALC_STEPS.length);

    setTimeout(function () {
      clearInterval(interval);
      state.screen = "result";
      state.resultStep = 0;
      render();
    }, CALC_DURATION_MS);
  }

  function getResult() {
    var answerIdx = state.answers[5];
    var opt = answerIdx != null ? QUESTIONS[4].options[answerIdx] : null;
    var isVisual = opt && opt.tags && opt.tags.indexOf("ja-visual") !== -1;
    return isVisual ? RESULTS.secundario : RESULTS.principal;
  }

  function renderResult() {
    var result = getResult();
    var dotsHtml = [0, 1]
      .map(function (i) {
        return (
          '<span class="h-1.5 flex-1 rounded-full transition-colors duration-300 ' +
          (i <= state.resultStep ? "bg-ember" : "bg-white/10") +
          '"></span>'
        );
      })
      .join("");
    var dotsBlock = '<div class="mx-auto mb-7 flex max-w-[200px] items-center justify-center gap-2">' + dotsHtml + "</div>";

    if (state.resultStep === 0) {
      root.innerHTML =
        '<div class="q-screen text-center">' +
        dotsBlock +
        '<span class="stamp text-ember">Diagnóstico concluído</span>' +
        '<h1 class="mt-4 font-display text-2xl font-800 leading-tight sm:text-3xl">' +
        result.title +
        "</h1>" +
        '<div class="mt-6 space-y-3 text-left">' +
        result.body
          .slice(0, 2)
          .map(function (p) {
            return '<p class="text-sm leading-relaxed text-bone-300">' + p + "</p>";
          })
          .join("") +
        "</div>" +
        '<button type="button" class="' +
        BTN_BASE +
        ' mt-8 w-full q-see-reco"><span>Ver minha recomendação</span>' +
        ARROW_SVG +
        "</button></div>";
      root.querySelector(".q-see-reco").addEventListener("click", function () {
        state.resultStep = 1;
        render();
      });
    } else {
      root.innerHTML =
        '<div class="q-screen text-center">' +
        dotsBlock +
        '<span class="block stamp text-ember">Sua recomendação</span>' +
        '<div class="mt-5"><div class="corner-frame relative mx-auto aspect-video w-full overflow-hidden rounded-xl border border-white/10 bg-carbon-900 shadow-card"><vslplay-player id="1670d70d-411c-4a85-be80-ca13c4eec7e9" aria-label="Seu diagnóstico" class="absolute inset-0 block h-full w-full"></vslplay-player></div></div>' +
        '<p class="mt-6 text-left text-sm leading-relaxed text-bone-300">' +
        result.body[2] +
        "</p>" +
        '<a href="https://pay.kiwify.com.br/Jjp3tM5" target="_blank" rel="noopener noreferrer" class="' +
        BTN_BASE +
        ' mt-7 w-full"><span>' +
        RESULTS.cta +
        "</span>" +
        ARROW_SVG +
        "</a></div>";
      if (!document.querySelector('script[src="https://cdn.vslplay.com/player.js"]')) {
        var s = document.createElement("script");
        s.src = "https://cdn.vslplay.com/player.js";
        s.defer = true;
        document.body.appendChild(s);
      }
    }
  }

  function render() {
    if (state.screen === "intro") renderIntro();
    else if (state.screen === "question") renderQuestion();
    else if (state.screen === "calculating") renderCalculating();
    else if (state.screen === "result") renderResult();
  }

  render();
})();
