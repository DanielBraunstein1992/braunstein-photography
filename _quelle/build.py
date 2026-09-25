#!/usr/bin/env python3
"""Erzeugt die Website Braunstein Photography aus den Inhaltsdateien.
Startseite: /home/claude/site/startseite.html (Vorlage) -> index.html
Blog:       blog/<slug>.json      -> blog/<slug>.html
Fotostorys: storys/<slug>.json    -> fotostorys/<slug>.html
"""
import json, os, re, shutil, html

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = '/mnt/user-data/outputs/braunstein-website'
CDN = 'https://cdn.prod.website-files.com/68ef69d6601002710ef48956/'
ALT = 'https://www.braunstein-photography.de'
BASIS = 'https://braunstein-photography.vercel.app'  # beim Domainwechsel auf https://www.braunstein-photography.de ändern
e = html.escape

listen = json.load(open(f'{SRC}/data_listen.json'))
blog_fertig = {f[:-5] for f in os.listdir(f'{SRC}/blog') if f.endswith('.json')}
story_fertig = {f[:-5] for f in os.listdir(f'{SRC}/storys') if f.endswith('.json')}

def blog_url(slug):  return f'/blog/{slug}' if slug in blog_fertig else f'{ALT}/blog/{slug}'
def story_url(slug): return f'/fotostorys/{slug}' if slug in story_fertig else f'{ALT}/fotostorys/{slug}'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Crimson+Pro:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jura:wght@300;400&display=swap" rel="stylesheet">'

KOPF = '''<header class="kopf">
  <a class="marke" href="/" aria-label="Braunstein Photography, zur Startseite"><img src="/assets/logo-weiss.png" alt="Braunstein Photography"></a>
  <nav id="hauptmenue" aria-label="Hauptnavigation">
    <a href="/ueber-mich"{a0}>Über mich</a>
    <a href="/fotostorys"{a1}>Fotostorys</a>
    <a href="/blog"{a2}>Blog</a>
    <a href="/faq"{a3}>FAQ</a>
    <a class="knopf knopf--hell" href="/kontakt">Kennenlernen vereinbaren</a>
  </nav>
  <button class="menue-knopf" type="button" aria-expanded="false" aria-controls="hauptmenue"><span>Menü</span></button>
</header>'''

FUSS = '''<section class="cta">
  <span class="klein">Nur rund 30 Hochzeiten im Jahr</span>
  <h2>Erzählt mir von eurem Tag.</h2>
  <p>Ich begleite bewusst nur eine begrenzte Zahl an Hochzeiten. So bleibt für jedes Paar genug Zeit.</p>
  <a class="knopf knopf--gold" href="/kontakt">Kennenlernen vereinbaren</a>
</section>
<footer>
  <div>
    <a class="marke" href="/"><img src="/assets/logo-weiss.png" alt="Braunstein Photography"></a>
    <p class="klein" style="margin-top:.8rem">Hochzeitsfotograf für Lübeck, Hamburg und Schleswig-Holstein<br><a href="tel:+4917614362401">+49 176 14362401</a></p>
  </div>
  <ul class="klein">
    <li><a href="/fotostorys">Fotostorys</a></li>
    <li><a href="/blog">Blog</a></li>
    <li><a href="/faq">FAQ</a></li>
    <li><a href="https://www.instagram.com/braunstein_photography/">Instagram</a></li>
    <li><a href="/impressum">Impressum</a></li>
    <li><a href="/datenschutz">Datenschutz</a></li>
  </ul>
</footer>'''

def seite(titel, beschreibung, inhalt, aktiv='', extra='', cta=True):
    a1 = ' aria-current="page"' if aktiv == 'storys' else ''
    a2 = ' aria-current="page"' if aktiv == 'blog' else ''
    a0 = ' aria-current="page"' if aktiv == 'ueber' else ''
    a3 = ' aria-current="page"' if aktiv == 'faq' else ''
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
</head>
<body class="unterseite">
{KOPF.format(a0=a0, a1=a1, a2=a2, a3=a3)}
<main>
{inhalt}
</main>
{FUSS if cta else FUSS[FUSS.index('<footer>'):]}
{extra}
<script>
(function(){{var k=document.querySelector('.kopf'),b=k&&k.querySelector('.menue-knopf');if(!b)return;
function s(o){{k.classList.toggle('offen',o);document.documentElement.classList.toggle('menue-offen',o);b.setAttribute('aria-expanded',o?'true':'false');b.firstChild.textContent=o?'Schließen':'Menü';}}
b.addEventListener('click',function(){{s(!k.classList.contains('offen'))}});
k.querySelectorAll('nav a').forEach(function(a){{a.addEventListener('click',function(){{s(false)}})}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')s(false)}});}})();
</script>
</body>
</html>
'''

def blog_karte(b):
    slug, titel, bild, text = b
    return f'''<a class="karte" href="{blog_url(slug)}">
  <img src="{CDN}{bild}" alt="Titelbild zum Artikel: {e(titel)}" loading="lazy">
  <h3>{e(titel)}</h3>
  <p>{e(text)}</p>
  <span class="klein mehr">Artikel lesen</span>
</a>'''

def story_karte(s):
    slug, titel, bild = s
    return f'''<a class="karte karte--story" href="{story_url(slug)}">
  <img src="{CDN}{bild}" alt="Hochzeit von {e(titel)}" loading="lazy">
  <h3>{e(titel)}</h3>
  <span class="klein mehr">Fotostory ansehen</span>
</a>'''

LIGHTBOX = '''<div class="lightbox" hidden><button class="lb-zu" aria-label="Schließen">×</button><button class="lb-pfeil lb-zurueck" aria-label="Vorheriges Bild">‹</button><img alt=""><button class="lb-pfeil lb-weiter" aria-label="Nächstes Bild">›</button></div>
<script>
(function(){
  var bilder=[].slice.call(document.querySelectorAll('.galerie img')),lb=document.querySelector('.lightbox');
  if(!lb||!bilder.length)return;var gross=lb.querySelector('img'),i=0;
  function zeige(n){i=(n+bilder.length)%bilder.length;gross.src=bilder[i].src;gross.alt=bilder[i].alt;lb.hidden=false;}
  bilder.forEach(function(b,n){b.addEventListener('click',function(){zeige(n)});});
  lb.querySelector('.lb-zu').onclick=function(){lb.hidden=true};
  lb.querySelector('.lb-zurueck').onclick=function(ev){ev.stopPropagation();zeige(i-1)};
  lb.querySelector('.lb-weiter').onclick=function(ev){ev.stopPropagation();zeige(i+1)};
  lb.addEventListener('click',function(ev){if(ev.target===lb)lb.hidden=true});
  document.addEventListener('keydown',function(ev){if(lb.hidden)return;if(ev.key==='Escape')lb.hidden=true;if(ev.key==='ArrowLeft')zeige(i-1);if(ev.key==='ArrowRight')zeige(i+1);});
})();
</script>'''

def baue():
    os.makedirs(f'{OUT}/blog', exist_ok=True)
    os.makedirs(f'{OUT}/fotostorys', exist_ok=True)
    os.makedirs(f'{OUT}/assets', exist_ok=True)
    shutil.copy(f'{SRC}/site.css', f'{OUT}/assets/site.css')
    if os.path.exists(f'{OUT}/assets/bilder'): shutil.rmtree(f'{OUT}/assets/bilder')
    shutil.copytree(f'{SRC}/bilder', f'{OUT}/assets/bilder')
    shutil.copy(f'{SRC}/logo-weiss.png', f'{OUT}/assets/logo-weiss.png')
    json.dump({"cleanUrls": True, "trailingSlash": False}, open(f'{OUT}/vercel.json', 'w'), indent=2)
    # Quelldateien mitliefern (werden von Vercel ignoriert)
    q = f'{OUT}/_quelle'
    if os.path.exists(q): shutil.rmtree(q)
    shutil.copytree(SRC, q, ignore=shutil.ignore_patterns('__pycache__'))
    open(f'{OUT}/.vercelignore', 'w').write('_quelle\n')

    # Blog-Übersicht
    karten = '\n'.join(blog_karte(b) for b in listen['blog'])
    inhalt = f'''<section class="seitenkopf">
  <span class="klein">Blog</span>
  <h1>Tipps und Geschichten für euren Tag.</h1>
  <p>Von der Location über das Licht bis zum Brautpaarshooting: Was ich in über 500 Hochzeiten gelernt habe.</p>
</section>
<section class="raster raster--blog">
{karten}
</section>'''
    open(f'{OUT}/blog/index.html', 'w').write(seite('Blog | Braunstein Photography', 'Tipps rund um Hochzeitsfotografie: Brautpaarshooting, Location, Licht und authentische Hochzeitsbilder.', inhalt, 'blog'))

    # Fotostory-Übersicht
    karten = '\n'.join(story_karte(s) for s in listen['storys'])
    inhalt = f'''<section class="seitenkopf">
  <span class="klein">Fotostorys</span>
  <h1>Diese Paare durfte ich begleiten.</h1>
  <p>Jede Hochzeit ist anders. Hier findet ihr eine Auswahl der Tage, bei denen ich mittendrin war.</p>
</section>
<section class="raster raster--storys">
{karten}
</section>'''
    open(f'{OUT}/fotostorys/index.html', 'w').write(seite('Fotostorys | Braunstein Photography', 'Echte Hochzeitsreportagen aus Lübeck, Hamburg und Schleswig-Holstein.', inhalt, 'storys'))

    # Blogartikel
    for i, b in enumerate(listen['blog']):
        slug = b[0]
        if slug not in blog_fertig: continue
        d = json.load(open(f'{SRC}/blog/{slug}.json'))
        teile = []
        for typ, wert in d['bloecke']:
            if typ == 'img' and wert == b[2]: continue
            if typ == 'img': teile.append(f'<figure><img src="{CDN}{wert}" alt="Bild zum Artikel {e(d["titel"])}" loading="lazy"></figure>')
            elif typ in ('h2', 'h3'): teile.append(f'<{typ}>{e(wert)}</{typ}>')
            elif typ == 'li': teile.append('<ul>' + ''.join(f'<li>{e(x)}</li>' for x in wert) + '</ul>')
            else: teile.append(f'<p>{e(wert)}</p>')
        weitere = [listen['blog'][(i + k) % len(listen['blog'])] for k in (1, 2, 3)]
        inhalt = f'''<article class="artikel-seite">
  <a class="zurueck klein" href="/blog">Zurück zum Blog</a>
  <h1>{e(d['titel'])}</h1>
  <figure class="artikel-titelbild"><img src="{CDN}{b[2]}" alt="Titelbild: {e(d['titel'])}"></figure>
  <div class="fliesstext">
{chr(10).join(teile)}
  </div>
</article>
<section class="weitere">
  <h2>Weitere Artikel</h2>
  <div class="raster raster--blog">{''.join(blog_karte(w) for w in weitere)}</div>
</section>'''
        beschr = b[3]
        open(f'{OUT}/blog/{slug}.html', 'w').write(seite(f"{d['titel']} | Braunstein Photography", beschr, inhalt, 'blog'))

    # Fotostorys
    for i, s in enumerate(listen['storys']):
        slug = s[0]
        if slug not in story_fertig: continue
        d = json.load(open(f'{SRC}/storys/{slug}.json'))
        bilder = '\n'.join(f'<img src="{CDN}{x}" alt="Hochzeit {e(d["titel"])}, Bild {n+1}" loading="lazy">' for n, x in enumerate(d['bilder']))
        stimme = f'<blockquote class="paarstimme"><p>„{e(d["stimme"])}“</p><cite class="klein">{e(d["titel"])}</cite></blockquote>' if d.get('stimme') else ''
        weitere = [listen['storys'][(i + k) % len(listen['storys'])] for k in (1, 2, 3)]
        inhalt = f'''<section class="story-kopf">
  <a class="zurueck klein" href="/fotostorys">Alle Fotostorys</a>
  <span class="klein datum">{e(d.get('datum', ''))}</span>
  <h1>{e(d['titel'])}</h1>
  {stimme}
</section>
<section class="galerie">
{bilder}
</section>
<section class="weitere">
  <h2>Weitere Fotostorys</h2>
  <div class="raster raster--storys">{''.join(story_karte(w) for w in weitere)}</div>
</section>'''
        open(f'{OUT}/fotostorys/{slug}.html', 'w').write(seite(f"Hochzeit {d['titel']} | Braunstein Photography", f"Fotostory: die Hochzeit von {d['titel']}, festgehalten von Daniel Braunstein.", inhalt, 'storys', LIGHTBOX))

    # Über mich
    d = json.load(open(f'{SRC}/ueber-mich.json'))
    def begriff(b): return f'<figure class="begriff"><q>{e(b[0])}</q><cite class="klein">{e(b[1])}</cite></figure>'
    anek = ''.join(f'<figure class="anekdote"><p>„{e(a[0])}“</p><cite class="klein">{e(a[1])}</cite></figure>' for a in d['anekdoten'])
    zeit = ''.join(f'<li><span class="klein zeit">{e(t[0])}</span><p>{e(t[1])}</p></li>' for t in d['tag'])
    inhalt = f'''<section class="um-kopf">
  <span class="klein">Über mich</span>
  <h1>Man kann viel über sich selbst schreiben.</h1>
  <p>Ich lasse lieber meine Paare erzählen.</p>
</section>
<section class="stimmenbild" aria-label="Was Paare über Daniel sagen">
  <div class="spalte links">{''.join(begriff(b) for b in d['links'])}</div>
  <figure class="bogen"><img src="{d['bild']}" alt="Daniel Braunstein zeigt lachend zwei Daumen nach oben"></figure>
  <div class="spalte rechts">{''.join(begriff(b) for b in d['rechts'])}</div>
</section>
<p class="herkunft klein">{e(d['herkunft'])}</p>
<section class="anekdoten">
  <h2>Und manchmal auch das.</h2>
  <div class="anekdoten-raster">{anek}</div>
</section>
<section class="tagesablauf">
  <div class="tagesablauf-kopf">
    <span class="klein">Hinter der Kamera</span>
    <h2>Ein Hochzeitstag, von der anderen Seite.</h2>
    <p>So kann ein Tag mit mir aussehen. Jede Hochzeit ist anders, aber ein paar Dinge passieren fast immer.</p>
  </div>
  <ol class="zeitleiste">{zeit}</ol>
</section>'''
    open(f'{OUT}/ueber-mich.html', 'w').write(seite('Über mich | Daniel Braunstein, Hochzeitsfotograf aus Lübeck', 'Was Brautpaare über Daniel Braunstein sagen: Hochzeitsfotograf aus Lübeck, seit 16 Jahren und mit über 500 Paaren.', inhalt, 'ueber'))

    # Kontakt
    schl = json.load(open(f'{SRC}/kontakt.json'))['web3forms_schluessel']
    stunden = ['bis 4 Stunden','6 Stunden','8 Stunden','10 Stunden oder mehr','Wissen wir noch nicht']
    chips = ''.join(f'<label><input type="radio" name="Begleitung" value="{s}"{" required" if i==0 else ""}><span>{s}</span></label>' for i, s in enumerate(stunden))
    inhalt = f"""<section class="kontakt">
  <div class="kontakt-intro">
    <span class="klein">Kontakt</span>
    <h1>Erzählt mir von eurem Tag.</h1>
    <p>Ein paar Eckdaten reichen mir für den Anfang. Ich melde mich innerhalb von 48 Stunden bei euch und sage euch, ob euer Termin noch frei ist.</p>
    <p>Ich begleite bewusst nur rund 30 Hochzeiten im Jahr. Fragt euer Datum also am besten frühzeitig an.</p>
    <div class="direkt">
      <p class="klein">Lieber direkt?</p>
      <p><a href="tel:+4917614362401">+49 176 14362401</a></p>
    </div>
  </div>
  <form class="formular" id="anfrage" action="https://api.web3forms.com/submit" method="POST">
    <input type="hidden" name="access_key" value="{schl}">
    <input type="hidden" name="subject" value="Neue Hochzeitsanfrage über die Website">
    <input type="hidden" name="from_name" value="Braunstein Photography Website">
    <input type="hidden" name="redirect" value="https://braunstein-photography.vercel.app/danke">
    <input type="checkbox" name="botcheck" class="unsichtbar" tabindex="-1" autocomplete="off">
    <div class="feldgruppe">
      <div class="feld"><label for="f-datum">Wann wollt ihr heiraten?</label><input id="f-datum" name="Hochzeitsdatum" type="date" required></div>
      <div class="feld"><label for="f-ort">Wo wollt ihr heiraten?</label><input id="f-ort" name="Ort / Location" type="text" placeholder="Location oder Ort" required></div>
    </div>
    <fieldset class="feld"><legend>An wie viele Stunden Begleitung habt ihr gedacht?</legend><div class="chips">{chips}</div></fieldset>
    <div class="feld"><label for="f-nachricht">Was möchtet ihr mir noch erzählen?</label><textarea id="f-nachricht" name="Nachricht" placeholder="Freie Trauung, Standesamt, besondere Wünsche, eure Geschichte …" required></textarea></div>
    <div class="feld"><label for="f-name">Eure Namen</label><input id="f-name" name="name" type="text" autocomplete="name" placeholder="z. B. Lena & Niklas" required></div>
    <div class="feldgruppe">
      <div class="feld"><label for="f-tel">Telefonnummer</label><input id="f-tel" name="Telefon" type="tel" autocomplete="tel" required></div>
      <div class="feld"><label for="f-mail">E-Mail</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
    </div>
    <label class="zustimmung"><input type="checkbox" name="Datenschutz" value="zugestimmt" required><span>Ich bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage verwendet werden. Mehr dazu in der <a href="/datenschutz">Datenschutzerklärung</a>.</span></label>
    <p class="klein pflicht">Alle Felder sind Pflichtfelder.</p>
    <p class="meldung" role="alert"></p>
    <button class="knopf" type="submit">Anfrage absenden</button>
  </form>
</section>
<script>
(function(){{
  var f=document.getElementById('anfrage');if(!f)return;
  f.querySelector('[name=redirect]').value=location.origin+'/danke';
  var dt=f.querySelector('#f-datum');if(dt){{dt.min=new Date().toISOString().slice(0,10);}}
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var k=f.querySelector('button'),m=f.querySelector('.meldung');
    k.disabled=true;k.textContent='Wird gesendet …';m.textContent='';
    var d=Object.fromEntries(new FormData(f));delete d.redirect;if(d.Hochzeitsdatum){{var t=d.Hochzeitsdatum.split('-');d.Hochzeitsdatum=t[2]+'.'+t[1]+'.'+t[0];}}
    fetch('https://api.web3forms.com/submit',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify(d)}})
      .then(function(r){{return r.json()}})
      .then(function(r){{if(r.success){{location.href='/danke'}}else{{throw new Error()}}}})
      .catch(function(){{m.textContent='Das hat leider nicht geklappt. Bitte versucht es noch einmal oder ruft mich direkt an: +49 176 14362401';k.disabled=false;k.textContent='Anfrage absenden'}});
  }});
}})();
</script>"""
    open(f'{OUT}/kontakt.html', 'w').write(seite('Kontakt | Braunstein Photography, Hochzeitsfotograf Lübeck', 'Fragt euren Hochzeitstermin an: Daniel Braunstein, Hochzeitsfotograf für Lübeck, Hamburg und Schleswig-Holstein.', inhalt, cta=False))

    # Danke
    inhalt = """<section class="danke">
  <span class="klein">Anfrage erhalten</span>
  <h1>Danke für eure Anfrage!</h1>
  <p class="unterzeile">Ich freue mich riesig, von euch zu hören.</p>
  <h2>So geht es weiter</h2>
  <ol class="schritte-danke">
    <li><div><strong>Ich melde mich innerhalb von 48 Stunden</strong><span>per Telefon oder E-Mail, je nachdem, wie ich euch am besten erreiche.</span></div></li>
    <li><div><strong>Ich sage euch, ob euer Termin noch frei ist</strong><span>Da ich nur rund 30 Hochzeiten im Jahr begleite, kläre ich das als Erstes.</span></div></li>
    <li><div><strong>Ein kurzes Telefonat über eure Wünsche</strong><span>Ihr erzählt mir von eurem Tag, und ich beantworte eure ersten Fragen.</span></div></li>
    <li><div><strong>Wir finden einen Termin zum Kennenlernen</strong><span>Ein entspanntes Gespräch mit euch beiden, damit wir sehen, ob die Chemie stimmt.</span></div></li>
  </ol>
  <p>Bis dahin könnt ihr gern schon in meinen Fotostorys stöbern.</p>
  <div class="danke-knoepfe">
    <a class="knopf knopf--dunkel" href="/fotostorys">Fotostorys ansehen</a>
    <a class="knopf knopf--rahmen" href="https://www.instagram.com/braunstein_photography/">Instagram</a>
  </div>
</section>"""
    open(f'{OUT}/danke.html', 'w').write(seite('Danke für eure Anfrage | Braunstein Photography', 'Eure Anfrage ist angekommen.', inhalt, cta=False).replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1))

    # FAQ
    fragen = json.load(open(f'{SRC}/faq.json'))
    liste = ''.join(f'<details class="frage"><summary>{e(q)}</summary><div class="antwort">{a}</div></details>' for q, a in fragen)
    inhalt = f"""<section class="seitenkopf">
  <span class="klein">Häufige Fragen</span>
  <h1>Was ihr euch vielleicht noch fragt.</h1>
  <p>Die Fragen, die mir Paare im Kennenlerngespräch am häufigsten stellen. Wenn eure nicht dabei ist, ruft mich einfach an oder schreibt mir.</p>
</section>
<section class="faq-liste">{liste}</section>"""
    open(f'{OUT}/faq.html', 'w').write(seite('Häufige Fragen | Braunstein Photography', 'Antworten auf die häufigsten Fragen rund um eure Hochzeitsfotografie: Ablauf, Wartezeit, Kosten und Posen.', inhalt, 'faq'))

    # Rechtliches
    def rtext(t):
        t = e(t).replace('\n', '<br>')
        return re.sub(r'(https?://[^\s<]+?)(?=[.,;)]?(\s|<|$))', r'<a href="\1" rel="noopener">\1</a>', t)
    for name, titel in (('impressum', 'Impressum'), ('datenschutz', 'Datenschutz')):
        d = json.load(open(f'{SRC}/recht/{name}.json'))
        teile = []
        for typ, wert in d['bloecke']:
            if typ in ('h2', 'h3'): teile.append(f'<{typ}>{e(wert)}</{typ}>')
            elif typ == 'li': teile.append('<ul>' + ''.join(f'<li>{rtext(x)}</li>' for x in wert) + '</ul>')
            else: teile.append(f'<p>{rtext(wert)}</p>')
        inhalt = f"""<article class="artikel-seite rechtstext">
  <h1>{e(d['titel'])}</h1>
  <div class="fliesstext">
{chr(10).join(teile)}
  </div>
</article>"""
        open(f'{OUT}/{name}.html', 'w').write(seite(f'{titel} | Braunstein Photography', f'{titel} von Braunstein Photography.', inhalt, cta=False))

    # Startseite: Links auf neue Unterseiten umstellen
    h = open(f'{SRC}/startseite.html').read()
    h = h.replace('<a href="#storys">Fotostorys</a>', '<a href="/fotostorys">Fotostorys</a>')
    h = h.replace('<a href="#blog">Blog</a>', '<a href="/blog">Blog</a>\n    <a href="/faq">FAQ</a>') if '<a href="/faq">FAQ</a>' not in h else h
    h = h.replace('<a href="#ueber">Über mich</a>', '<a href="/ueber-mich">Über mich</a>')
    h = h.replace(f'href="{ALT}/impressum"', 'href="/impressum"').replace(f'href="{ALT}/datenschutz"', 'href="/datenschutz"')
    h = h.replace('href="#kontakt"', 'href="/kontakt"').replace(f'href="{ALT}/kontakt"', 'href="/kontakt"')
    if 'href="/ueber-mich" class="mehr-link"' not in h:
        h = h.replace('<span class="klein">Hochzeiten im Jahr</span></div>\n        </div>', '<span class="klein">Hochzeiten im Jahr</span></div>\n        </div>\n        <a href="/ueber-mich" class="mehr-link klein" style="display:inline-block;margin-top:1.8rem;color:var(--gegenlicht);text-underline-offset:3px">Was meine Paare über mich sagen</a>', 1)
    h = h.replace(f'href="{ALT}/fotostorys"', 'href="/fotostorys"')
    h = h.replace(f'href="{ALT}/blog"', 'href="/blog"')
    h = re.sub(re.escape(ALT) + r'/fotostorys/([a-z0-9-]+)', lambda m: story_url(m.group(1)), h)
    h = re.sub(re.escape(ALT) + r'/blog/([a-z0-9-]+)', lambda m: blog_url(m.group(1)), h)
    open(f'{OUT}/index.html', 'w').write(h)

    # Favicon, Vorschaubild, Canonical in alle Seiten
    for f in ('favicon.ico', 'apple-touch-icon.png'): shutil.copy(f'{SRC}/{f}', f'{OUT}/{f}')
    for f in ('favicon-32.png', 'og-bild.jpg', 'zustimmung.js'): shutil.copy(f'{SRC}/{f}', f'{OUT}/assets/{f}')
    seiten = []
    for wurzel, _, dateien in os.walk(OUT):
        if '_quelle' in wurzel: continue
        for d_ in dateien:
            if not d_.endswith('.html'): continue
            voll = os.path.join(wurzel, d_); rel = os.path.relpath(voll, OUT)[:-5]
            pfad = '/' if rel == 'index' else '/' + (rel[:-6] if rel.endswith('/index') else rel)
            h = open(voll).read()
            if 'rel="icon"' not in h:
                titel = re.search(r'<title>(.*?)</title>', h, re.S).group(1)
                m = re.search(r'<meta name="description" content="([^"]*)"', h); beschr = m.group(1) if m else ''
                kopf = f"""<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="canonical" href="{BASIS}{pfad}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Braunstein Photography">
<meta property="og:locale" content="de_DE">
<meta property="og:url" content="{BASIS}{pfad}">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschr}">
<meta property="og:image" content="{BASIS}/assets/og-bild.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
</head>"""
                h = h.replace('</head>', kopf, 1)
            if 'zustimmung.js' not in h:
                h = h.replace('</body>', '<script src="/assets/zustimmung.js" defer></script>\n</body>', 1)
            open(voll, 'w').write(h)
            if 'noindex' not in h: seiten.append(pfad)
    seiten.sort(key=lambda p: (p != '/', p.count('/'), p))
    open(f'{OUT}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASIS}{p}</loc></url>\n' for p in seiten) + '</urlset>\n')
    open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASIS}/sitemap.xml\n')
    print(f'Blog: {len(blog_fertig)}/{len(listen["blog"])} Artikel, Fotostorys: {len(story_fertig)}/{len(listen["storys"])}')

if __name__ == '__main__':
    baue()
