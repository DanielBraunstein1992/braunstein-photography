#!/usr/bin/env python3
"""Erzeugt die Zeitplan-Vorlage (PDF) für die Landingpage. Inhalte aus Daniels Blogartikeln."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, PageBreak)
from reportlab.lib.styles import ParagraphStyle

HIER = os.path.dirname(os.path.abspath(__file__))
SCHRIFT = os.environ.get('SCHRIFTEN', '/tmp/claude-0/fonts')
ZIEL = os.path.join(HIER, '..', 'downloads', 'zeitplan-vorlage-hochzeitstag.pdf')

for n, f in [('Display', 'CG-500.ttf'), ('DisplayI', 'CG-500i.ttf'), ('Text', 'CP-300.ttf'),
             ('TextB', 'CP-500.ttf'), ('TextI', 'CP-300i.ttf'), ('Klein', 'Jura-400.ttf')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(SCHRIFT, f)))

TIEFSEE, SCHIEFER, GOLD, SAND, NEBEL, WEISS = (HexColor(x) for x in
    ('#1E2C30', '#4A585C', '#8F5F1C', '#D9CDB8', '#E8ECE9', '#F9FAF8'))

s = {
    'titel': ParagraphStyle('titel', fontName='Display', fontSize=34, leading=36, textColor=TIEFSEE, spaceAfter=6),
    'unter': ParagraphStyle('unter', fontName='Klein', fontSize=9, leading=12, textColor=GOLD, spaceAfter=14),
    'h2': ParagraphStyle('h2', fontName='Display', fontSize=20, leading=23, textColor=TIEFSEE, spaceBefore=14, spaceAfter=6),
    'text': ParagraphStyle('text', fontName='Text', fontSize=11, leading=15.5, textColor=TIEFSEE, spaceAfter=6),
    'klein': ParagraphStyle('klein', fontName='Klein', fontSize=8.5, leading=11, textColor=SCHIEFER),
    'punkt': ParagraphStyle('punkt', fontName='Text', fontSize=10.5, leading=14.5, textColor=TIEFSEE, leftIndent=12, bulletIndent=0, spaceAfter=3),
    'zeit': ParagraphStyle('zeit', fontName='Klein', fontSize=9.5, leading=13, textColor=GOLD),
    'zelle': ParagraphStyle('zelle', fontName='Text', fontSize=10.5, leading=13.5, textColor=TIEFSEE),
    'tipp': ParagraphStyle('tipp', fontName='TextI', fontSize=11, leading=15.5, textColor=TIEFSEE),
}

def seite(c, doc):
    c.saveState()
    c.setFillColor(TIEFSEE); c.rect(0, 0, A4[0], 14 * mm, stroke=0, fill=1)
    c.setFillColor(SAND); c.setFont('Klein', 8)
    c.drawString(18 * mm, 5.5 * mm, 'Braunstein Photography · Hochzeitsfotograf aus Lübeck')
    c.drawRightString(A4[0] - 18 * mm, 5.5 * mm, 'braunstein-photography.de · +49 176 14362401')
    c.restoreState()

doc = BaseDocTemplate(ZIEL, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=22 * mm,
                      title='Mein Zeitplan für euren Hochzeitstag', author='Daniel Braunstein')
doc.addPageTemplates([PageTemplate(frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')], onPage=seite)])

def punkte(liste):
    return [Paragraph(p, s['punkt'], bulletText='·') for p in liste]

inhalt = [
    Paragraph('Mein Zeitplan für euren Hochzeitstag', s['titel']),
    Paragraph('VON DANIEL BRAUNSTEIN, HOCHZEITSFOTOGRAF AUS LÜBECK · AUS ÜBER 500 HOCHZEITEN', s['unter']),
    Paragraph('So plane ich einen ganzen Tag mit standesamtlicher und kirchlicher Trauung. Natürlich ist jede Hochzeit anders, '
              'aber dieser Ablauf hat sich bei mir immer wieder bewährt. Ganz am Ende findet ihr eine Vorlage für euren eigenen Plan.', s['text']),
    Paragraph('Ein Tag mit Standesamt und Kirche', s['h2']),
]
ablauf = [
    ('8 Uhr', 'Getting Ready', ''),
    ('9.50 Uhr', 'First Look (optional)', 'Nur ihr zwei. Eure Gäste warten schon im Standesamt oder um die Ecke. Ein intimer Moment zu zweit, bevor es losgeht.'),
    ('10 Uhr', 'Standesamtliche Trauung', 'Danach können wir eure Gäste Spalier stehen lassen.'),
    ('11 Uhr', 'Brautpaarshooting, 30 Minuten', 'Kurz und knackig.'),
    ('12 Uhr', 'Mittagessen', ''),
    ('14 Uhr', 'Kirchliche Trauung', 'Danach nehmt ihr draußen die Glückwünsche entgegen. Bei 100 Gästen dauert das bei mir etwa 20 Minuten.'),
    ('15 Uhr', 'Sektempfang', ''),
    ('15.30 Uhr', 'Großes Gruppenbild und weitere Gruppenbilder', ''),
    ('16.30 Uhr', 'Hochzeitstorte', ''),
    ('16.45 Uhr', 'Brautpaarshooting, 20 bis 30 Minuten', ''),
    ('19 Uhr', 'Abendessen', ''),
    ('20.30 Uhr', 'Sonnenuntergangs-Shooting bis 21 Uhr', ''),
    ('21 Uhr', 'Hochzeitstanz', 'Danach wird nur noch gefeiert.'),
    ('24 Uhr', 'Mitternachtssnack', ''),
]
zeilen = []
for z, w, n in ablauf:
    txt = f'<font name="TextB">{w}</font>' + (f'<br/><font name="TextI" color="#4A585C">{n}</font>' if n else '')
    zeilen.append([Paragraph(z, s['zeit']), Paragraph(txt, s['zelle'])])
t = Table(zeilen, colWidths=[24 * mm, doc.width - 24 * mm])
t.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 0.5, SAND), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                       ('TOPPADDING', (0, 0), (-1, -1), 3.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 3.2)]))
inhalt += [t, Spacer(1, 8)]
hinweis = Table([[Paragraph('<font name="Display" size="15" color="#1E2C30">Warum ich die Paarbilder aufteile</font><br/>'
                            'Ich teile die Brautpaarshootings bewusst in kurze Sequenzen. Ihr sollt mit euren Gästen feiern '
                            'und nicht drei Stunden mit mir Hochzeitsbilder machen.', s['text'])]], colWidths=[doc.width])
hinweis.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), NEBEL), ('LEFTPADDING', (0, 0), (-1, -1), 12),
                             ('RIGHTPADDING', (0, 0), (-1, -1), 12), ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
inhalt += [KeepTogether(hinweis), PageBreak(),
    Paragraph('Meine Tipps aus Erfahrung', s['h2']),
    Paragraph('<font name="TextB">Die Torte am Nachmittag.</font> Aus Erfahrung passt die Hochzeitstorte am besten um 16.30 Uhr. '
              'Den Rest könnt ihr abends wunderbar noch einmal zum Dessert dazustellen.', s['text']),
    Paragraph('<font name="TextB">Der Hochzeitstanz um 21 Uhr.</font> Eure Gäste und ihr wollt irgendwann einfach feiern. '
              'Schaut, dass bis dahin alle Programmpunkte erledigt sind, damit ihr danach nur noch Party machen könnt.', s['text']),
    Paragraph('<font name="TextB">Spalier und Glückwünsche.</font> Nach dem Standesamt können eure Gäste Spalier stehen. '
              'Nach der kirchlichen Trauung nehmt ihr die Glückwünsche draußen entgegen, bei 100 Gästen sind das etwa 20 Minuten.', s['text']),
    Paragraph('<font name="TextB">Sagt es euren Gästen.</font> Wenn alle wissen, wann die Gruppenbilder stattfinden, '
              'wartet niemand, und ihr könnt den Tag genießen.', s['text']),
    Paragraph('So plant ihr euren eigenen Ablauf', s['h2']),
] + punkte([
    'Schreibt auf, wann die Trauung stattfindet und wann ihr zu Abend essen wollt.',
    'Bedenkt die Anfahrtszeiten zur Trauung und zur Location, und wo geparkt wird.',
    'Plant am Nachmittag Zeitpuffer ein, eure Gäste haben bestimmt Überraschungen für euch.',
    'Für das Abendessen braucht ihr mindestens 90 Minuten.',
    'Schaut, wann bei euch die Sonne untergeht, und plant das Sonnenuntergangs-Shooting davor ein.',
]) + [Paragraph('Euer Zeitplan', s['h2'])]
leer = [[Paragraph('UHRZEIT', s['klein']), Paragraph('WAS PASSIERT', s['klein']), Paragraph('WO', s['klein']), Paragraph('NOTIZ', s['klein'])]] + [['', '', '', ''] for _ in range(11)]
lt = Table(leer, colWidths=[24 * mm, 70 * mm, 38 * mm, doc.width - 132 * mm], rowHeights=[7 * mm] + [8 * mm] * 11)
lt.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 0.5, SAND), ('LINEBELOW', (0, 0), (-1, 0), 0.8, GOLD),
                        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM')]))
inhalt += [lt, Spacer(1, 10)]
kasten = Table([[Paragraph('<font name="Display" size="16" color="#1E2C30">Ist euer Datum noch frei?</font><br/>'
                           'Ich begleite rund 30 Hochzeiten im Jahr. Schreibt mir einfach: '
                           '<font name="TextB">braunstein-photography.de/anfrage</font> oder <font name="TextB">+49 176 14362401</font>.', s['text'])]],
               colWidths=[doc.width])
kasten.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), NEBEL), ('LEFTPADDING', (0, 0), (-1, -1), 12),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 12), ('TOPPADDING', (0, 0), (-1, -1), 10), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
inhalt += [KeepTogether(kasten)]
os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
doc.build(inhalt)
print('PDF:', os.path.abspath(ZIEL))
