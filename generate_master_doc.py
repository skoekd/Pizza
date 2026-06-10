from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

for section in doc.sections:
    section.top_margin    = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin   = Cm(2.0)
    section.right_margin  = Cm(2.0)

BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
RED    = RGBColor(0xC0, 0x39, 0x2B)
GREY   = RGBColor(0x55, 0x55, 0x55)
LGREY  = RGBColor(0xF2, 0xF2, 0xF2)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GREEN  = RGBColor(0x27, 0xAE, 0x60)
ORANGE = RGBColor(0xE6, 0x7E, 0x22)

def shade_cell(cell, hex_colour):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_colour)
    tcPr.append(shd)

def add_para(text='', bold=False, italic=False, size=10.5, colour=BLACK,
             align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=5,
             font='Calibri'):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = font
        run.font.size = Pt(size)
        run.font.color.rgb = colour
    return p

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(15)
    run.font.color.rgb = RED
    add_rule('C0392B')
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.color.rgb = GREY
    return p

def add_rule(colour_hex='C0392B'):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(3)
    pPr = p._p.get_or_add_pPr()
    pb  = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    '6')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), colour_hex)
    pb.append(bot)
    pPr.append(pb)

def mono(text, size=9.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(1)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(size)
    run.font.color.rgb = GREY
    return p

def bullet(text, colour=BLACK, bold_prefix=''):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(3)
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.bold = True
        r1.font.name = 'Calibri'
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = colour
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = BLACK
    return p

def numbered_step(n, text, highlight_colour=RED):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(4)
    r1 = p.add_run(f'{n}.  ')
    r1.bold = True
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = highlight_colour
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = BLACK

def info_table(rows, col_widths=(5.5, 9.5)):
    t = doc.add_table(rows=len(rows), cols=2)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, (label, val) in enumerate(rows):
        shade = 'F2F2F2' if i % 2 == 0 else 'FFFFFF'
        lc = t.cell(i, 0)
        vc = t.cell(i, 1)
        shade_cell(lc, shade)
        shade_cell(vc, shade)
        lr = lc.paragraphs[0].add_run(label)
        vr = vc.paragraphs[0].add_run(val)
        lr.bold = True
        for r, c in [(lr, BLACK), (vr, GREY)]:
            r.font.name = 'Calibri'
            r.font.size = Pt(10)
            r.font.color.rgb = c
    t.columns[0].width = Cm(col_widths[0])
    t.columns[1].width = Cm(col_widths[1])
    doc.add_paragraph()

def banner(text, fill='C0392B'):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(17)
    run.font.color.rgb = WHITE
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Cm(0.3)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  fill)
    pPr.append(shd)
    doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════
#  COVER
# ═══════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(20)
p.paragraph_format.space_after  = Pt(4)
r = p.add_run('DOUGH EYED STYLE PIZZA')
r.bold = True
r.font.name = 'Calibri'
r.font.size = Pt(26)
r.font.color.rgb = RED

add_para('Master Reference Document  —  Research, Recipe & Bake Notes',
         size=12, colour=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_para('Contemporary Neapolitan  |  80% Biga  |  80% Hydration  |  8 × 260g',
         size=10.5, colour=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
add_rule()

# ═══════════════════════════════════════════════════════════════
#  SECTION 1 — ABOUT DOUGH EYED
# ═══════════════════════════════════════════════════════════════
add_h1('Section 1 — About Dough Eyed Pizza')

add_para('Dough Eyed is a contemporary Neapolitan pizza restaurant based in York, UK. '
         'The head chef and co-owner is Adam Gardener (@adamgpizza on Instagram). '
         'The restaurant account is @dough_eyed. Their style sits outside strict AVPN rules — '
         'they use electric deck ovens at 380–390°C rather than wood-fired, and they lean into '
         'a biga-based dough that prioritises flavour complexity and an open, airy cornicione.',
         size=10.5, colour=BLACK, space_after=6)

add_h2('Their Commercial Process (researched)')
info_table([
    ('Style',           'Contemporary Neapolitan — not strict AVPN'),
    ('Oven',            'Electric deck oven at 380–390°C'),
    ('Mixer',           'Sunmix Queen 60 commercial spiral mixer'),
    ('Pre-ferment',     'BIGA — commercial fresh yeast, 24hr cold retard'),
    ('Hydration',       '~80%'),
    ('Flour blend',     'Molino Pizzuti: 75% Tipo 0 / 20% Manitoba / 5% Tipo 1'),
    ('Yeast rate',      '3g fresh yeast per kg total flour'),
    ('Structure',       '80% flour in biga / 20% flour in refresh'),
    ('Biga scale',      '20,000g flour in biga + 5,000g in refresh'),
    ('Biga FDT',        '27°C  (mixed to this closing temperature)'),
    ('Cold retard',     '24hrs at ~4°C after balling'),
])

add_h2('Key Instagram Sources')
bullet(' @dough_eyed — restaurant account (York, UK)')
bullet(' @adamgpizza — Adam Gardener, Co-owner & Head Chef')
add_para('Screenshots from Adam\'s account confirmed: biga process, closing temperature of 27°C, '
         '24hr cold retard, and the balled dough appearance after CT.',
         size=10, colour=GREY, space_after=8)

# ═══════════════════════════════════════════════════════════════
#  SECTION 2 — KEY CONCEPTS
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Section 2 — Key Concepts & Terminology')

add_h2('BIGA')
add_para('A stiff Italian pre-ferment. Typically 50% hydration — meaning the water added equals '
         '50% of the biga flour weight. Mixed briefly (5 minutes slow), then cold-fermented for '
         '24 hours. The long cold ferment develops complex organic acids and extensible gluten. '
         'Strong flours go in the biga because they need to survive the long fermentation without '
         'degrading.',
         size=10.5, space_after=6)

add_h2('Bassinage')
add_para('The technique of adding water in stages during the refresh mix rather than all at once. '
         'Starts at ~60% hydration to build gluten structure first, then water is added gradually '
         'to bring the dough up to 80%. This prevents the dough becoming a slack mess before '
         'the gluten network is developed.',
         size=10.5, space_after=6)

add_h2('FDT — Final Dough Temperature / Closing Temperature')
add_para('"Closing temperature" is what Adam calls it. The temperature the dough is at when you '
         'stop the mixer. This is not the oven temperature — it is the dough temperature measured '
         'with a probe thermometer during mixing. The target temperature drives the water '
         'temperature you use. Every degree off changes yeast activity and fermentation rate.',
         size=10.5, space_after=6)
info_table([
    ('Biga target FDT',    '27°C   (range: 26–28°C)'),
    ('Refresh target FDT', '19°C   (stop mixer the moment you hit this)'),
])

add_h2('Water Temperature Formula')
add_para('The water temperature is calculated backwards from the target FDT, accounting for '
         'the ambient room temperature, flour temperature, and the heat added by the mixer '
         '(friction factor). Each mixer has its own friction factor.',
         size=10.5, space_after=4)

add_para('BIGA formula (3 factors — no pre-ferment temp):', bold=True, size=10.5, space_after=2)
mono('Water temp  =  (Target FDT × 3)  −  (room temp + flour temp + friction factor)')
mono('Friction factor for KYS Pro Baker 7 on biga (5-min slow): 10°C')
mono('Example:  (27 × 3) − (23.5 + 19 + 10)  =  81 − 52.5  =  28.5°C  →  round to 29°C')
doc.add_paragraph()

add_para('REFRESH formula (4 factors — includes cold biga temp):', bold=True, size=10.5, space_after=2)
mono('Water temp  =  (Target FDT × 4)  −  (room + flour + biga temp + friction factor)')
mono('Friction factor for KYS Pro Baker 7 on full mix (24-min): 18°C')
mono('Biga temp from fridge: assumed 4°C')
mono('Example:  (19 × 4) − (21 + 17 + 4 + 18)  =  76 − 60  =  16°C')
doc.add_paragraph()

add_h2('Active Dry Yeast Conversions')
add_para('Dough Eyed uses commercial fresh yeast. When converting to Active Dry Yeast (ADY):',
         size=10.5, space_after=3)
info_table([
    ('Fresh → Active Dry Yeast', 'Divide fresh yeast weight by 2'),
    ('Fresh → Instant Yeast',    'Divide fresh yeast weight by 3'),
    ('ADY — bloom first?',       'Dissolve in ~50ml of warm (35°C) water. Wait 5–10 min until foamy. '
                                  'Required when mixing water is cold (as in this recipe).'),
])

add_h2('Why Strong Flour in Biga / Light Flour in Refresh')
add_para('Strong flours (high W-value, high protein) are used in the biga because the gluten '
         'network must survive 24 hours of cold fermentation. Weaker flours would degrade '
         'and produce a slack, overworked dough.',
         size=10.5, space_after=3)
add_para('Extensible, lighter flours (lower W-value) go in the refresh because they '
         'contribute the stretch needed for pizza opening. Adding them at this late stage '
         'means they don\'t need to survive fermentation — they just need to give the final '
         'dough extensibility and an open crumb.',
         size=10.5, space_after=6)

add_h2('Coil Folds vs Bulk Folds')
add_para('Coil folds on individual balls build some surface tension but are less effective than '
         'bulk folds on the full dough mass. Bulk folds (performed before balling) create '
         'layered gluten structure throughout the dough and trap gas in large irregular pockets. '
         'This is what creates an open, airy cornicione with oven spring. Skipping bulk folds '
         'produces a denser, more uniform crumb.',
         size=10.5, space_after=6)

# ═══════════════════════════════════════════════════════════════
#  SECTION 3 — FLOURS
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Section 3 — Flour Selection & Properties')

add_h2('Available Flours (user\'s pantry)')
t = doc.add_table(rows=5, cols=4)
t.style = 'Table Grid'
t.alignment = WD_TABLE_ALIGNMENT.LEFT
for i, h in enumerate(['Flour', 'Protein', 'W Value', 'Role']):
    c = t.cell(0, i)
    shade_cell(c, 'C0392B')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
flour_data = [
    ('Casillo La 8 Plus',       '14.5%', 'W350', 'BIGA — strongest flour, structure anchor'),
    ('Casillo Pizza Superiore', '13.5%', 'W340', 'BIGA — main biga flour by volume'),
    ('Casillo Aroma',           '13.0%', 'W280', 'BIGA — flavour complexity'),
    ('Caputo Nuvola',           '12.5%', 'W270', 'REFRESH — extensibility and open crumb'),
]
for ri, row in enumerate(flour_data):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate(row):
        cell = t.cell(ri + 1, ci)
        shade_cell(cell, shade)
        run = cell.paragraphs[0].add_run(val)
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK if ci == 0 else GREY
        if ci == 0:
            run.bold = True
t.columns[0].width = Cm(4.5)
t.columns[1].width = Cm(2.0)
t.columns[2].width = Cm(2.0)
t.columns[3].width = Cm(6.5)
doc.add_paragraph()

add_para('Note: Caputo Blue (W260–280, 12.5%) is a valid alternative to Nuvola in the refresh '
         'if Nuvola is unavailable. Do NOT put Caputo Blue in the biga — it is not strong enough '
         'to survive 24hr fermentation.',
         size=10, colour=GREY, space_after=8)

# ═══════════════════════════════════════════════════════════════
#  SECTION 4 — MASTER RECIPE
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Section 4 — Master Recipe')

add_h2('Recipe Overview')
info_table([
    ('Yield',           '8 dough balls × 260g'),
    ('Total flour',     '1,140g'),
    ('Total water',     '912g  (80% hydration)'),
    ('Pre-ferment',     '80% Biga structure'),
    ('Total dough',     '~2,086g'),
    ('Oven',            'Electric deck  |  380–390°C'),
    ('Bake time',       '2.5–4 minutes per pizza'),
])

add_h2('Full Ingredient List')
t2 = doc.add_table(rows=9, cols=3)
t2.style = 'Table Grid'
t2.alignment = WD_TABLE_ALIGNMENT.LEFT
for i, h in enumerate(['Ingredient', 'Weight', 'Stage']):
    c = t2.cell(0, i)
    shade_cell(c, '1A1A1A')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
ing_rows = [
    ('Casillo La 8 Plus',       '228g', 'Biga'),
    ('Casillo Pizza Superiore', '456g', 'Biga'),
    ('Casillo Aroma',           '228g', 'Biga'),
    ('Biga water (calc. temp)', '456g', 'Biga'),
    ('Active Dry Yeast',        '1.4g', 'Biga'),
    ('Caputo Nuvola',           '228g', 'Refresh'),
    ('Refresh water (calc. temp)', '456g', 'Refresh'),
    ('Active Dry Yeast',        '1.7g', 'Refresh'),
]
for ri, (ing, wt, stage) in enumerate(ing_rows):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate((ing, wt, stage)):
        cell = t2.cell(ri + 1, ci)
        shade_cell(cell, shade)
        run = cell.paragraphs[0].add_run(val)
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK if ci == 0 else GREY
        if ci == 0:
            run.bold = True
t2.columns[0].width = Cm(6.0)
t2.columns[1].width = Cm(2.5)
t2.columns[2].width = Cm(3.5)
doc.add_paragraph()

add_para('Salt: 34g  (3% of total flour)  —  added at refresh only, at the 10-minute mark',
         bold=True, size=10.5, space_after=2)
add_para('EVOO: 23g  (2% of total flour)  —  added at refresh only, when dough hits 16°C',
         bold=True, size=10.5, space_after=8)

# ── Numbers check ──
add_h2('Numbers Check')
checks = [
    ('Biga flour',    '228 + 456 + 228 = 912g', '80% of 1,140g total', '✓'),
    ('Refresh flour', '228g Nuvola', '20% of 1,140g total', '✓'),
    ('Total flour',   '912 + 228 = 1,140g', '', '✓'),
    ('Biga water',    '50% × 912 = 456g', 'Biga hydration 50%', '✓'),
    ('Refresh water', '912 − 456 = 456g', 'Remaining from total', '✓'),
    ('Total water',   '456 + 456 = 912g', '80% of 1,140g', '✓'),
    ('Salt',          '3% × 1,140 = 34g', '', '✓'),
    ('Oil',           '2% × 1,140 = 23g', '', '✓'),
    ('Biga ADY',      '(0.3% × 912) ÷ 2 = 1.4g', 'From fresh yeast rate', '✓'),
    ('Refresh ADY',   '(3g/kg × 1.14kg) ÷ 2 = 1.7g', 'From fresh yeast rate', '✓'),
    ('Per ball',      '2,086g ÷ 8 = 260.75g', '', '✓'),
]
tc = doc.add_table(rows=len(checks)+1, cols=4)
tc.style = 'Table Grid'
for i, h in enumerate(['Item', 'Calculation', 'Notes', '']):
    c = tc.cell(0, i)
    shade_cell(c, 'C0392B')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
for ri, (item, calc, note, tick) in enumerate(checks):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate((item, calc, note, tick)):
        cell = tc.cell(ri+1, ci)
        shade_cell(cell, shade)
        run = cell.paragraphs[0].add_run(val)
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        col = GREEN if ci == 3 else (BLACK if ci == 0 else GREY)
        run.font.color.rgb = col
        if ci == 0:
            run.bold = True
tc.columns[0].width = Cm(3.0)
tc.columns[1].width = Cm(5.5)
tc.columns[2].width = Cm(5.0)
tc.columns[3].width = Cm(0.8)
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════
#  SECTION 5 — STAGE BY STAGE PROCESS
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
banner('STAGE 1 — BIGA')

add_h2('At A Glance')
info_table([
    ('Flour',      '912g  (La 8 Plus 228g + Pizza Superiore 456g + Aroma 228g)'),
    ('Water',      '456g  at calculated temperature  (target ~29°C in winter conditions)'),
    ('ADY',        '1.4g  (dissolved in 50ml warm water first)'),
    ('Target FDT', '27°C   |   Acceptable range: 26–28°C'),
    ('Mix time',   '5 minutes on slow speed (~80 RPM)'),
    ('Ferment',    '24 hours cold retard in fridge at ~4°C'),
])

add_h2('Step by Step')
for i, step in enumerate([
    'Measure room temperature and flour temperature with probe thermometer.',
    'Calculate biga water temperature:  Water = 81 − (room + flour + 10).',
    'Take ~50ml from your total 456g water. Warm that 50ml to ~35°C. '
     'Dissolve 1.4g ADY in it. Wait 5–10 minutes until foamy/creamy. '
     'Cool the remaining water so that when combined, the full 456g averages your calculated target.',
    'Weigh biga flour into mixer bowl: La 8 Plus 228g + Pizza Superiore 456g + Aroma 228g.',
    'Pour the full 456g water (with dissolved ADY) into the flour.',
    'Mix on SLOW speed for exactly 5 minutes. Dough will look rough and shaggy — this is correct.',
    'Probe the dough temperature in 3 different spots. Target: 27°C.',
    'Cover bowl tightly with cling film or lid. Transfer straight to fridge — do not leave at room temp.',
    'Cold ferment for 24 hours at ~4°C. Note the exact time in.',
], 1):
    numbered_step(i, step)

add_h2('What The Biga Should Look Like')
bullet('Rough, slightly crumbly texture — not smooth like final dough', bold_prefix='Texture: ')
bullet('Not a single cohesive ball — that\'s fine', bold_prefix='Shape: ')
bullet('Small bubbles and some expansion after 24hrs — sign of active yeast', bold_prefix='After CT: ')

# ── STAGE 2 ──
doc.add_page_break()
banner('STAGE 2 — REFRESH')

add_h2('At A Glance')
info_table([
    ('New flour',   '228g  Caputo Nuvola (or Caputo Blue)'),
    ('Water',       '456g  at calculated temperature  (target ~16°C in winter conditions)'),
    ('ADY',         '1.7g  (dissolved before adding)'),
    ('Salt',        '34g   — added at 10-minute mark only'),
    ('EVOO',        '23g   — added only when dough hits 16°C'),
    ('Target FDT',  '19°C  — STOP MIXER immediately on reaching this'),
    ('Mix time',    '~22–24 minutes total'),
])

add_h2('Bassinage — Pre-Split Your Water Before Starting')
add_para('Divide your 456g of refresh water into four portions before you begin mixing. '
         'Label them. Have them ready in separate containers.',
         size=10.5, space_after=4)

tb = doc.add_table(rows=5, cols=3)
tb.style = 'Table Grid'
for i, h in enumerate(['Portion', 'Amount', 'When to Add']):
    c = tb.cell(0, i)
    shade_cell(c, 'C0392B')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
bass = [
    ('Portion 1 (60%)',  '274g', 'Added at start — 0:00'),
    ('Portion 2 (20%)',   '91g', 'Added slowly, mins 2–8'),
    ('Portion 3 (15%)',   '68g', 'Added slowly after Portion 2'),
    ('Portion 4 (5%)',    '23g', 'Added with salt at 10-min mark'),
]
for ri, row in enumerate(bass):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate(row):
        cell = tb.cell(ri+1, ci)
        shade_cell(cell, shade)
        run = cell.paragraphs[0].add_run(val)
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK if ci == 0 else GREY
        if ci == 0:
            run.bold = True
tb.columns[0].width = Cm(3.5)
tb.columns[1].width = Cm(2.0)
tb.columns[2].width = Cm(9.5)
doc.add_paragraph()
mono('Total: 274 + 91 + 68 + 23 = 456g  ✓')
doc.add_paragraph()

add_h2('Mixing Sequence')
mix_steps = [
    ('0:00',  'Biga chunks + 228g Nuvola + dissolved ADY into bowl. Add Portion 1 (274g). SLOW speed.'),
    ('2:00',  'Dough coming together. Begin adding Portion 2 (91g) slowly — take 6 minutes.'),
    ('8:00',  'Portion 2 fully added. Begin adding Portion 3 (68g) slowly.'),
    ('10:00', 'Add 34g SALT + Portion 4 (23g). Continue slow for 5 more minutes.'),
    ('15:00', 'Switch to FAST speed (~220–250 RPM). Insert probe. Monitor temperature closely.'),
    ('16°C',  'Dough hits 16°C → drizzle in 23g EVOO slowly while mixing continues.'),
    ('19°C',  'Dough hits 19°C → STOP MIXER immediately. Total time ~22–24 minutes.'),
]
tm = doc.add_table(rows=len(mix_steps)+1, cols=2)
tm.style = 'Table Grid'
for i, h in enumerate(['Time / Temp', 'Action']):
    c = tm.cell(0, i)
    shade_cell(c, '1A1A1A')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
for ri, (t_, a) in enumerate(mix_steps):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    c0 = tm.cell(ri+1, 0)
    c1 = tm.cell(ri+1, 1)
    shade_cell(c0, shade)
    shade_cell(c1, shade)
    r0 = c0.paragraphs[0].add_run(t_)
    r0.bold = True
    r0.font.name = 'Calibri'
    r0.font.size = Pt(10)
    r0.font.color.rgb = RED
    r1 = c1.paragraphs[0].add_run(a)
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10)
    r1.font.color.rgb = BLACK
tm.columns[0].width = Cm(2.5)
tm.columns[1].width = Cm(12.5)
doc.add_paragraph()

# ── STAGE 3 ──
doc.add_page_break()
banner('STAGE 3 — FOLD, BALL & COLD RETARD')

add_h2('This Stage Is Critical — Do Not Skip The Bulk Folds')
add_para('The bulk fold before balling is what creates the open, airy crumb and oven spring. '
         'Skipping it produces smaller, more uniform bubbles and less structure in the cornicione. '
         'See Bake 1 notes for the consequence of skipping this step.',
         size=10.5, colour=ORANGE, space_after=6)

add_h2('Step by Step')
for i, step in enumerate([
    'After mixer stops, leave dough to rest in bowl, covered, for 5 minutes.',
    'Tip dough onto a lightly oiled surface — do not flour.',
    'Perform COIL FOLD 1: slide both hands under dough, lift the centre, let each end fold down. '
     'Rotate 90°. Repeat. This counts as one fold.',
    'Cover and rest 20 minutes.',
    'Perform COIL FOLD 2. Cover and rest 20 minutes.',
    'Perform COIL FOLD 3. Cover and rest 20 minutes.',
    'Perform COIL FOLD 4 if dough feels slack. Rest 15 minutes.',
    'Divide into 8 equal pieces of 260g each using scales.',
    'Ball each piece: stretch the surface skin down and under, rotate until taut. '
     'The top surface should be smooth and tight.',
    'Place each ball into its own oiled container or a well-oiled tray.',
    'Leave at room temperature for 30 minutes to settle.',
    'Transfer to fridge. Cold retard for 24 hours at ~4°C.',
], 1):
    numbered_step(i, step)

add_h2('What Good Balls Look Like Going Into The Fridge')
bullet('Round with a tight, smooth top skin')
bullet('Hold their shape without spreading immediately')
bullet('Slightly domed — not perfectly flat')
add_para('Note: at 80% hydration balls will always be slacker than 65–75% dough. '
         'Some spreading is normal and expected. The structure should still be visible.',
         size=10, colour=GREY, space_after=8)

# ── STAGE 4 ──
banner('STAGE 4 — PROOF & BAKE')

add_h2('Proofing Before Service')
info_table([
    ('When to pull',     '3 hours before baking'),
    ('How',              'Remove tray from fridge. Leave covered at room temperature.'),
    ('What to look for', 'Balls slowly puff up and dome as they warm. Jiggle slightly when tray is shaken.'),
    ('Ready to bake',    'When visibly puffed and jiggling. Do not let them over-proof.'),
    ('If over-proofed',  'Very flat, sticky, hard to open — bake immediately or dough degrades quickly'),
])

add_h2('Separating & Opening')
for i, step in enumerate([
    'Use a well-oiled dough scraper to separate individual balls from tray — do not pull or tear.',
    'Place on a lightly semolina-dusted surface.',
    'Press gently from the centre outward with fingertips. Leave 1.5–2cm crust untouched.',
    'Let gravity stretch — pick up the dough and let it hang, rotating gently.',
    'At 80% hydration the dough is very extensible — use a light touch. It will tear if forced.',
    'Target diameter: ~30–32cm',
], 1):
    numbered_step(i, step)

add_h2('Baking')
info_table([
    ('Oven temperature', '380–390°C (electric deck oven)'),
    ('Stone/deck preheat', 'Minimum 45 minutes at full temp before first pizza'),
    ('Launch method',    'Semolina on peel. Check slide before launching.'),
    ('Bake time',        '2.5–4 minutes — watch, not timer'),
    ('Rotation',         'Rotate 180° halfway through for even colour'),
    ('Done when',        'Leopard spotting on crust, base sounds hollow, cornicione is puffed'),
])

# ═══════════════════════════════════════════════════════════════
#  SECTION 6 — TIMELINE
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Section 5 — Master Timeline (Friday Biga → Sunday Bake)')

tl = doc.add_table(rows=8, cols=3)
tl.style = 'Table Grid'
for i, h in enumerate(['Day', 'Time', 'Action']):
    c = tl.cell(0, i)
    shade_cell(c, 'C0392B')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
timeline = [
    ('Friday',   '~10:00 AM', 'Mix biga. Probe FDT (target 27°C). Cover and into fridge.'),
    ('Saturday', '~10:00 AM', 'Pull biga. Mix refresh. FDT target 19°C.'),
    ('Saturday', '~10:30 AM', 'Coil folds × 4 on bulk dough (20 min intervals).'),
    ('Saturday', '~12:30 PM', 'Divide and ball. 30 min rest at RT. Into fridge (24hr CT).'),
    ('Sunday',   '  2:00 PM', 'Pull all 8 balls from fridge. Leave covered at RT.'),
    ('Sunday',   '  4:45 PM', 'Preheat oven to 390°C if not already at temp.'),
    ('Sunday',   '  5:00 PM', 'Bake. First pizza in oven.'),
]
for ri, (day, time_, act) in enumerate(timeline):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate((day, time_, act)):
        cell = tl.cell(ri+1, ci)
        shade_cell(cell, shade)
        run = cell.paragraphs[0].add_run(val)
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK if ci == 0 else GREY
        if ci == 0:
            run.bold = True
tl.columns[0].width = Cm(2.5)
tl.columns[1].width = Cm(2.5)
tl.columns[2].width = Cm(10.0)
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════
#  SECTION 7 — BAKE 1 NOTES
# ═══════════════════════════════════════════════════════════════
add_h1('Section 6 — Bake 1 Session Notes & Lessons Learned')

add_h2('What Went Right')
bullet('Biga hit 26.9–27.1°C — perfect closing temperature')
bullet('Refresh water temperature calculated correctly (16°C) from actual measured temps')
bullet('Dough showed honeycomb cracking on surface in CT — sign of healthy fermentation')
bullet('Leopard spotting on the cornicione was excellent — oven temp correct')
bullet('Taste was described as awesome — fermentation flavour came through')
bullet('Crispiness was good')
bullet('Toppings and overall pizza appearance was high quality')

add_h2('What Went Wrong')
bullet('Skipped bulk coil folds on the dough mass before balling — went straight from mixer to balls. '
       'This is the single biggest mistake. See impact below.', bold_prefix='CRITICAL: ')
bullet('Balls were very slack and merged together in the tray overnight due to no bulk structure')
bullet('Re-balling was required at ~11PM the night before to rebuild tension')
bullet('Crumb was denser and more closed than target — direct result of skipping bulk folds')
bullet('Less oven spring than target — cornicione didn\'t dome or open as much as desired')
bullet('ADY was added directly to cold water without pre-dissolving — may have slowed biga activation')

add_h2('Impact of Skipping Bulk Folds — Technical Explanation')
add_para('Bulk folds (coil folds on the full dough mass before balling) serve two purposes: '
         '(1) they build a layered gluten network that traps CO2 in large, irregular pockets — '
         'which becomes the open, alveolar crumb; (2) they build enough surface tension that '
         'when the dough is balled, the skin is already partially developed.',
         size=10.5, space_after=4)
add_para('Without bulk folds: the gas distributes into small uniform bubbles. '
         'The balls have no pre-built structure. At 80% hydration they spread immediately '
         'and merge in the tray. Re-balling can partially rescue this but the internal '
         'crumb structure cannot be fully recovered.',
         size=10.5, space_after=6)

add_h2('Bake 1 Actual Measurements')
info_table([
    ('Biga: room temp',     '23.5°C'),
    ('Biga: flour temp',    '19°C'),
    ('Biga: water temp used', '29°C'),
    ('Biga: FDT achieved',  '26.9–27.1°C  ✓'),
    ('Refresh: room temp',  '21°C'),
    ('Refresh: flour temp', '17°C'),
    ('Refresh: water temp', '16°C'),
    ('Flour used in refresh', 'Caputo Nuvola (had plenty available)'),
])

add_h2('Comparison: User\'s Balls vs Adam G\'s Balls After CT')
add_para('Adam\'s @adamgpizza home bake showed very tall, domed balls after 24hr CT. '
         'User\'s balls were flat and merged. Key differences:',
         size=10.5, space_after=4)
t_comp = doc.add_table(rows=5, cols=3)
t_comp.style = 'Table Grid'
for i, h in enumerate(['Factor', 'Adam G', 'This Bake']):
    c = t_comp.cell(0, i)
    shade_cell(c, '1A1A1A')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
comp_data = [
    ('Hydration',     '~75% (estimated)', '80%'),
    ('Bulk folds',    'Yes — before balling', 'Skipped'),
    ('Ball state',    'Tall, domed, separated', 'Flat, merged, slack'),
    ('Photo timing',  'After full 24hr CT',    'After re-balling, still cold'),
]
for ri, row in enumerate(comp_data):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate(row):
        cell = t_comp.cell(ri+1, ci)
        shade_cell(cell, shade)
        run = cell.paragraphs[0].add_run(val)
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK if ci == 0 else GREY
        if ci == 0:
            run.bold = True
t_comp.columns[0].width = Cm(3.5)
t_comp.columns[1].width = Cm(5.5)
t_comp.columns[2].width = Cm(5.5)
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════
#  SECTION 8 — NEXT BAKE
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Section 7 — Changes For Next Bake')

add_h2('Priority Fixes (in order of impact)')

for i, step in enumerate([
    'DO THE BULK FOLDS. After the refresh, perform 4 × coil folds on the full dough mass '
     'at 20-minute intervals before balling. This is the single biggest improvement available.',
    'Pre-dissolve ADY properly. Take 50ml from biga water, warm to 35°C, dissolve ADY, '
     'wait until foamy before adding to cold water. Do not skip this step.',
    'Ball tighter. After bulk folds the dough will be easier to shape with a good tight skin. '
     'Take your time with each ball.',
    'Consider dropping to 78% hydration for the next bake if handling remains difficult. '
     '78% still produces an open, Neapolitan-style crumb with noticeably better ball structure.',
    'Opening technique: be patient when stretching. At high hydration the dough is very extensible — '
     'gravity and time do the work. Do not rush or force it.',
], 1):
    numbered_step(i, step)

add_h2('What To Keep The Same')
bullet('Flour blend — the flavour was excellent, no changes needed')
bullet('Yeast quantities — 1.4g biga / 1.7g refresh is correct')
bullet('Biga FDT target — 27°C is confirmed correct')
bullet('Refresh FDT target — 19°C is correct')
bullet('Biga hydration — 50% is correct')
bullet('Oven temperature — 380–390°C is correct, leoparding was excellent')

add_h2('Pasta Vecchia Option (Next Bake Enhancement)')
add_para('If you have leftover dough from a previous bake, you can add it as "pasta vecchia" '
         '(old dough) during the refresh. Add 5–10% of the new dough weight in chunks of old '
         'dough alongside the biga. This contributes additional fermentation complexity and '
         'flavour depth that is difficult to achieve any other way.',
         size=10.5, colour=GREY, space_after=8)

add_h2('Quick Reference — Formulas')
mono('Biga water temp  =  81 − (room temp + flour temp + 10)')
mono('Refresh water temp  =  76 − (room temp + flour temp + 4 + 18)')
mono('ADY from fresh  =  fresh yeast weight ÷ 2')
mono('Instant yeast from fresh  =  fresh yeast weight ÷ 3')
doc.add_paragraph()
add_para('These formulas are calibrated for the KYS Pro Baker 7 spiral mixer. '
         'The friction factors (10°C biga / 18°C refresh) are specific to this machine. '
         'If you change mixers, you will need to re-establish the friction factor.',
         size=10, colour=GREY, space_after=8)

# ── Save ──────────────────────────────────────────────────────
path = '/home/user/Pizza/Dough_Eyed_Master_Document.docx'
doc.save(path)
print(f'Saved: {path}')
