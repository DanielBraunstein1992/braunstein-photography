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
                      title='Zeitplan-Vorlage für euren Hochzeitstag', author='Daniel Braunstein')
doc.addPageTemplates([PageTemplate(frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')], onPage=seite)])

def punkte(liste):
    return [Paragraph(p, s['punkt'], bulletText='·') for p in liste]

inhalt = [
    Paragraph('Zeitplan-Vorlage für euren Hochzeitstag', s['titel']),
    Paragraph('VON DANIEL BRAUNSTEIN, HOCHZEITSFOTOGRAF AUS LÜBECK', s['unter']),
    Paragraph('Den eigenen Hochzeitstag stellt man sich gut strukturiert und entspannt vor. Damit das gelingt, hilft ein '
              'Tagesablauf, der eure Wünsche abdeckt und trotzdem Luft lässt. Hier findet ihr ein Beispiel, die wichtigsten '
              'Fragen für euren eigenen Plan und ganz am Ende eine Vorlage zum Ausfüllen.', s['text']),
    Paragraph('Ein Beispiel: Standesamt und Trauung an einem Tag', s['h2']),
    Paragraph('Die Königsdisziplin. Natürlich ist das nur eine Empfehlung, aber so funktionieren zwei Trauungen an einem Tag:', s['text']),
]
beispiel = [('7 Uhr', 'Getting Ready'), ('9 Uhr', 'Paarshooting'), ('10 Uhr', 'Standesamtliche Trauung'),
            ('11 Uhr', 'Brunch oder Mittagessen'), ('14 Uhr', 'Kirchliche oder freie Trauung'), ('15 Uhr', 'Sektempfang an der Location'),
            ('16.30 Uhr', 'Hochzeitstorte, Kuchen und Nachmittagsaktivitäten'), ('19 Uhr', 'Abendessen mit Musik'),
            ('21 Uhr', 'Hochzeitstanz und Eröffnung der Tanzfläche'), ('23 Uhr', 'Snacks und Erfrischungen')]
t = Table([[Paragraph(z, s['zeit']), Paragraph(w, s['zelle'])] for z, w in beispiel], colWidths=[28 * mm, doc.width - 28 * mm])
t.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 0.5, SAND), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                       ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
inhalt += [t, Spacer(1, 4)]
inhalt += [
    Paragraph('So plant ihr euren eigenen Ablauf', s['h2']),
] + punkte([
    'Schreibt auf, wann die Trauung stattfindet und wann ihr gern zu Abend essen würdet.',
    'Bedenkt die Anfahrtszeiten zur Trauung und zur Location. Wann müsst ihr euch morgens fertig machen, wann losfahren, und wo wird geparkt?',
    'Direkt nach der Trauung braucht ihr Zeit für die Glückwünsche. Je nach Anzahl der Gäste sind 60 bis 90 Minuten sinnvoll.',
    'Wann sollen eure Paarbilder entstehen? Vor der Trauung ganz für euch, nach der Trauung voller Emotionen oder im Abendlicht?',
    'Plant am Nachmittag Zeitpuffer ein, eure Gäste haben bestimmt Überraschungen für euch. Legt ein paar Fixpunkte fest, zum Beispiel für die Gruppenfotos.',
    'Für das Abendessen braucht ihr mindestens 90 Minuten, damit alle entspannt essen und reden können.',
    'Überlegt, wann die Torte angeschnitten wird und wann der Hochzeitstanz folgt.',
])
inhalt += [PageBreak(),
    Paragraph('Wann ist die beste Zeit für eure Paarbilder?', s['h2']),
    Paragraph('<font name="TextB">Vor der Trauung, intim und ruhig.</font> Ihr habt Zeit und einen Moment nur für euch, und Frisur, Make-up und Outfits sitzen noch perfekt. '
              'Dafür seht ihr euch schon vor der Trauung, das solltet ihr vorher entscheiden.', s['text']),
    Paragraph('<font name="TextB">Nach der Trauung, voller Emotionen.</font> Am besten dann, wenn ohnehin ein Ortswechsel ansteht. '
              'Eure Gäste können in Ruhe ankommen, und ihr habt einen Moment für euch.', s['text']),
    Paragraph('<font name="TextB">In den Abendstunden.</font> Das goldene Licht verzaubert jedes Bild. Zwischen Empfang und Abendprogramm reichen '
              'manchmal schon 20 Minuten für wunderschöne Bilder im Sonnenuntergang.', s['text']),
    Spacer(1, 4),
    Paragraph('Mein Tipp: Sagt euren Gästen, wann die Gruppenfotos stattfinden, und gebt ihnen eine grobe Orientierung im Tagesablauf. '
              'Dann wartet niemand, und ihr könnt den Tag genießen.', s['tipp']),
    Paragraph('Euer Zeitplan', s['h2']),
]
leer = [[Paragraph('UHRZEIT', s['klein']), Paragraph('WAS PASSIERT', s['klein']), Paragraph('WO', s['klein']), Paragraph('NOTIZ', s['klein'])]] + [['', '', '', ''] for _ in range(15)]
lt = Table(leer, colWidths=[24 * mm, 70 * mm, 38 * mm, doc.width - 132 * mm], rowHeights=[7 * mm] + [8.2 * mm] * 15)
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
