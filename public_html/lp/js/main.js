(function () {
  document.documentElement.classList.add("js-on");

  // ---------- reveal on scroll ----------
  var targets = document.querySelectorAll(".rv");
  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "-40px" }
  );
  targets.forEach(function (t) {
    io.observe(t);
  });

  // ---------- FAQ accordion ----------
  var faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach(function (item) {
    var button = item.querySelector("button");
    var panel = item.querySelector(".faq-panel");
    button.addEventListener("click", function () {
      var isOpen = item.classList.contains("open");
      faqItems.forEach(function (i) {
        i.classList.remove("open");
        i.querySelector("button").setAttribute("aria-expanded", "false");
      });
      if (!isOpen) {
        item.classList.add("open");
        button.setAttribute("aria-expanded", "true");
      }
    });
    panel.hidden = false;
  });

  // ---------- sticky mobile CTA ----------
  var sticky = document.getElementById("sticky-cta");
  if (sticky) {
    function onScroll() {
      if (window.scrollY > window.innerHeight * 0.8) {
        sticky.classList.remove("hide");
      } else {
        sticky.classList.add("hide");
      }
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // ---------- image zoom lightbox ----------
  var lightbox = document.getElementById("lightbox");
  var lightboxImg = document.getElementById("lightbox-img");
  if (lightbox && lightboxImg) {
    document.querySelectorAll("[data-zoom]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var img = btn.querySelector("img");
        lightboxImg.src = img.currentSrc || img.src;
        lightboxImg.alt = img.alt;
        lightbox.classList.add("open");
        document.body.style.overflow = "hidden";
      });
    });
    function closeLightbox() {
      lightbox.classList.remove("open");
      document.body.style.overflow = "";
    }
    lightbox.addEventListener("click", closeLightbox);
    lightbox.querySelector(".lightbox-close").addEventListener("click", function (e) {
      e.stopPropagation();
      closeLightbox();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeLightbox();
    });
  }

  // ---------- carousels (prova social: mensagens de alunos) ----------
  document.querySelectorAll("[data-carousel]").forEach(function (car) {
    var track = car.querySelector(".carousel-track");
    car.querySelectorAll(".carousel-arrow").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var dir = parseInt(btn.getAttribute("data-dir"), 10);
        track.scrollBy({ left: dir * track.clientWidth * 0.8, behavior: "smooth" });
      });
    });
  });
})();
