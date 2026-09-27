/* Einwilligung und Meta-Pixel – Braunstein Photography */
(function () {
  var PIXEL_ID = '1004904100364264';
  var SCHLUESSEL = 'bp-zustimmung';
  var geladen = false;

  function lesen() { try { return localStorage.getItem(SCHLUESSEL); } catch (e) { return null; } }
  function speichern(w) { try { localStorage.setItem(SCHLUESSEL, w); } catch (e) {} }

  function pixelLaden() {
    if (geladen) return; geladen = true;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', PIXEL_ID);
    window.fbq('track', 'PageView');
    if (/^\/danke(\.html)?\/?$/.test(location.pathname)) window.fbq('track', 'Lead');
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"]');
    if (a && geladen && window.fbq) window.fbq('track', 'Contact');
  });

  var stil = document.createElement('style');
  stil.textContent =
    '.zustimmung-box{position:fixed;left:clamp(.8rem,3vw,2rem);right:clamp(.8rem,3vw,2rem);bottom:calc(clamp(.8rem,3vw,2rem) + env(safe-area-inset-bottom,0px));z-index:60;max-width:30rem;background:#F9FAF8;color:#1E2C30;box-shadow:0 24px 60px -20px rgba(0,0,0,.45);padding:1.5rem 1.6rem;font-family:"Crimson Pro",Georgia,serif;font-size:1.05rem;line-height:1.55}' +
    '.zustimmung-box h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:400;font-size:1.6rem;margin:0 0 .6rem;line-height:1.15}' +
    '.zustimmung-box p{margin:0 0 1.2rem;color:#4A585C}' +
    '.zustimmung-box a{color:#1E2C30}' +
    '.zustimmung-knoepfe{display:flex;gap:.7rem;flex-wrap:wrap}' +
    '.zustimmung-knoepfe button{flex:1 1 8rem;font-family:"Jura","Segoe UI",sans-serif;font-size:.88rem;letter-spacing:.05em;padding:.85rem 1rem;border:1px solid #1E2C30;background:#1E2C30;color:#F9FAF8;cursor:pointer}' +
    '.zustimmung-knoepfe button:hover{background:#9A6620;border-color:#9A6620;color:#F9FAF8}' +
    '.zustimmung-link{background:none;border:0;padding:0;font:inherit;color:inherit;cursor:pointer;letter-spacing:inherit}' +
    '.zustimmung-link:hover{color:#F9FAF8}';
  document.head.appendChild(stil);

  function banner() {
    if (document.querySelector('.zustimmung-box')) return;
    var box = document.createElement('div');
    box.className = 'zustimmung-box';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'Datenschutz-Einstellungen');
    box.innerHTML =
      '<h2>Datenschutz-Einstellungen</h2>' +
      '<p>Diese Website verwendet das Meta-Pixel, um die Wirksamkeit von Werbeanzeigen zu messen. Das Pixel wird nur mit Ihrer Einwilligung geladen. Sie können Ihre Auswahl jederzeit über „Cookie-Einstellungen“ am Seitenende ändern. Weitere Informationen finden Sie in der <a href="/datenschutz">Datenschutzerklärung</a>.</p>' +
      '<div class="zustimmung-knoepfe"><button type="button" data-w="nein">Ablehnen</button><button type="button" data-w="ja">Akzeptieren</button></div>';
    box.addEventListener('click', function (e) {
      var w = e.target.getAttribute && e.target.getAttribute('data-w');
      if (!w) return;
      speichern(w); box.remove();
      if (w === 'ja') pixelLaden();
      else if (geladen) location.reload();
    });
    document.body.appendChild(box);
  }

  function fussLink() {
    var ul = document.querySelector('footer ul');
    if (!ul || ul.querySelector('.zustimmung-link')) return;
    var li = document.createElement('li');
    li.innerHTML = '<button type="button" class="zustimmung-link">Cookie-Einstellungen</button>';
    li.firstChild.addEventListener('click', banner);
    ul.appendChild(li);
  }

  function start() {
    fussLink();
    var w = lesen();
    if (w === 'ja') pixelLaden();
    else if (w !== 'nein') banner();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
