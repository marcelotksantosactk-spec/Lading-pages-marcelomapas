// Rastreamento da TAOS para o resumosmapasdireito.com (WordPress do Marcelo), numa linha só no <head> do site:
//   <script async src="https://marcelomapas.com/taos-wp.js?v=1"></script>
// Faz o mesmo que as páginas da TAOS no marcelomapas.com (ver rastreamento.py): configura e carrega o t.js
// (page_view e identidade no sck da Kiwify, sem pixel e sem compra) e põe a reserva da UTMify no clique.
// Mesmos scripts de rastreamento.py; mudou aqui, mude o ?v= no WordPress (a Cloudflare guarda .js por 180 dias).
window.__taos={k:"067ac0999349691af43ab4b2",d:{u:"https://gpfcpisrasfxfpgpyicy.supabase.co",a:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdwZmNwaXNyYXNmeGZwZ3B5aWN5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI3NzIxMjEsImV4cCI6MjEwODM0ODEyMX0.4yJcNhIP3Y867r_qxfbeEcN0i9bgKf2cqEoP8-jKL4k"}};
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href*="pay.kiwify.com.br"]');if(!a)return;try{var u=new URL(a.href),q=new URLSearchParams(location.search);q.forEach(function(v,k){if(!u.searchParams.has(k))u.searchParams.set(k,v)});a.href=u.toString()}catch(err){}},true);
(function(){var s=document.createElement('script');s.async=true;s.src='https://marcelomapas.com/t.js?v=eb01b922';(document.head||document.documentElement).appendChild(s);})();
