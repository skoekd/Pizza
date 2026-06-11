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
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GREEN  = RGBColor(0x27, 0xAE, 0x60)
ORANGE = RGBColor(0xE6, 0x7E, 0x22)
BLUE   = RGBColor(0x1A, 0x5F, 0x9E)

def shade_cell(cell, hex_colour):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_colour)
    tcPr.append(shd)

def add_para(text='', bold=False, italic=False, size=10.5, colour=BLACK,
             align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=5):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Calibri'
        run.font.size = Pt(size)
        run.font.color.rgb = colour
    return p

def add_h1(text, colour=RED):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.color.rgb = colour
    add_rule()

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.font.color.rgb = GREY

def add_rule(colour_hex='C0392B'):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pb  = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    '6')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), colour_hex)
    pb.append(bot)
    pPr.append(pb)

def mono(text, size=9.5, colour=GREY):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(size)
    run.font.color.rgb = colour

def bullet(text, bold_prefix='', prefix_colour=RED):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(3)
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.bold = True
        r1.font.name = 'Calibri'
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = prefix_colour
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = BLACK

def step(n, text, sub=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(4)
    if sub:
        p.paragraph_format.left_indent = Cm(0.8)
    r1 = p.add_run(f'{n}.  ')
    r1.bold = True
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = RED
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = BLACK

def info_table(rows, col_widths=(5.5, 9.5)):
    t = doc.add_table(rows=len(rows), cols=2)
    t.style = 'Table Grid'
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
    run.font.size = Pt(16)
    run.font.color.rgb = WHITE
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.left_indent  = Cm(0.4)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    pPr.append(shd)
    doc.add_paragraph()

def warning_box(text, fill='FEF3CD'):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x7D, 0x49, 0x00)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Cm(0.3)
    p.paragraph_format.right_indent = Cm(0.3)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    pPr.append(shd)
    doc.add_paragraph()

def make_table(headers, rows, header_fill='C0392B', col_widths=None):
    t = doc.add_table(rows=len(rows)+1, cols=len(headers))
    t.style = 'Table Grid'
    for i, h in enumerate(headers):
        c = t.cell(0, i)
        shade_cell(c, header_fill)
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        r.font.color.rgb = WHITE
    for ri, row in enumerate(rows):
        shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
        for ci, val in enumerate(row):
            cell = t.cell(ri+1, ci)
            shade_cell(cell, shade)
            run = cell.paragraphs[0].add_run(str(val))
            run.font.name = 'Calibri'
            run.font.size = Pt(10)
            run.font.color.rgb = BLACK if ci == 0 else GREY
            if ci == 0:
                run.bold = True
    if col_widths:
        for i, w in enumerate(col_widths):
            t.columns[i].width = Cm(w)
    doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════
#  COVER
# ═══════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(20)
p.paragraph_format.space_after  = Pt(4)
r = p.add_run('DOUGH EYED × GIGI STYLE')
r.bold = True
r.font.name = 'Calibri'
r.font.size = Pt(26)
r.font.color.rgb = RED

add_para('Contemporary Neapolitan  —  Version 2  —  Summer Edition',
         size=13, colour=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
add_para('80% Biga  |  75% Hydration  |  12 × 260g  |  Electric Deck 380–390°C',
         size=11, colour=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
add_para('Includes: Autolyse  |  Bulk Coil Folds  |  Summer Temperature Protocol',
         size=10, colour=ORANGE, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
add_rule()

# ═══════════════════════════════════════════════════════════════
#  SECTION 1 — WHAT'S CHANGED FROM VERSION 1
# ═══════════════════════════════════════════════════════════════
add_h1('What Changed From Version 1 — And Why')

make_table(
    ['Area', 'Version 1', 'Version 2', 'Reason'],
    [
        ('Hydration',      '80%',          '75%',
         'Pentosans in Aroma Tipo 1 absorb extra water. 75% handles better, still very open crumb.'),
        ('Balls',          '8 × 260g',     '12 × 260g',   'User requirement'),
        ('Autolyse',       'None',         '20 min',
         'Lets Nuvola hydrate before mechanical stress. Better extensibility, shorter mix time.'),
        ('Bulk folds',     'Skipped',      '3 × coil fold',
         'Critical miss in V1. Creates open alveolar crumb and oven spring.'),
        ('Yeast rate',     'Winter rate',  'Summer rate (−50%)',
         '30°C ambient accelerates fermentation. Less yeast needed.'),
        ('Biga water',     'Warm',         'Fridge-cold (~14°C)',
         'Summer room/flour temps require colder water to hit 27°C FDT.'),
        ('Refresh water',  'Cold',         'Ice water (0–2°C)',
         'Summer formula requires ice water. No other way to achieve 19°C FDT.'),
        ('RT proof time',  '3 hours',      '1.5–2 hours',
         '30°C ambient means balls proof much faster. Watch them, not the clock.'),
        ('ADY activation', 'Inconsistent', 'Always dissolve first in 35°C water', 'Ensures full yeast activity'),
    ],
    col_widths=[3.0, 2.5, 2.5, 7.0]
)

# ═══════════════════════════════════════════════════════════════
#  SECTION 2 — MASTER RECIPE NUMBERS
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Master Recipe — Full Ingredient List')

add_h2('Overview')
info_table([
    ('Yield',           '12 balls × 260g  =  3,120g total dough'),
    ('Total flour',     '1,733g'),
    ('Total water',     '1,300g  (75% hydration)'),
    ('Biga structure',  '80% of flour in biga  /  20% in refresh'),
    ('Style',           'Contemporary Neapolitan  —  Dough Eyed × Gigi'),
    ('Oven',            'Electric deck  |  380–390°C'),
])

add_h2('Biga Ingredients')
make_table(
    ['Flour', 'Weight', 'W Value', 'Type', 'Role'],
    [
        ('Casillo La 8 Plus',       '347g', 'W350', '0/00', 'Structural anchor — highest protein'),
        ('Casillo Pizza Superiore', '693g', 'W340', '0/00', 'Main biga base — bulk of the strength'),
        ('Casillo Aroma',           '346g', 'W280', 'TIPO 1', 'Germ & bran — ferments for 24hrs, softens sharp edges'),
        ('TOTAL biga flour',        '1,386g', '—', '—', '80% of total flour'),
        ('Biga water',              '693g',  '—', '—', '50% of biga flour  |  target ~14°C — see calc'),
        ('Active Dry Yeast',        '0.7g',  '—', '—', 'Summer rate  |  dissolve in 35°C water first'),
    ],
    header_fill='1A1A1A',
    col_widths=[4.5, 1.8, 1.8, 1.8, 5.1]
)

add_h2('Refresh Ingredients')
make_table(
    ['Ingredient', 'Weight', 'Notes'],
    [
        ('Caputo Nuvola',      '347g',  'Low P/L — extensibility for opening. Refresh flour only.'),
        ('Refresh water',      '607g',  'ICE WATER 0–2°C required in summer  |  see calc'),
        ('Active Dry Yeast',   '0.6g',  'Dissolve in small amount of warm water first'),
        ('Salt',               '52g',   'Added at 10-minute mark ONLY — not before'),
        ('EVOO',               '35g',   'Added when dough probe hits 16°C ONLY — not before'),
        ('TOTAL refresh flour','347g',  '20% of total flour'),
    ],
    col_widths=[4.0, 2.0, 9.0]
)

add_h2('Numbers Check')
make_table(
    ['Item', 'Calculation', 'Result', ''],
    [
        ('Total flour',    '1,386 + 347',             '1,733g',  '✓'),
        ('Total water',    '693 + 607',               '1,300g',  '✓'),
        ('Hydration',      '1,300 ÷ 1,733',           '75.0%',   '✓'),
        ('Biga %',         '1,386 ÷ 1,733',           '80.0%',   '✓'),
        ('Biga water',     '50% × 1,386',             '693g',    '✓'),
        ('Salt',           '3% × 1,733',              '52g',     '✓'),
        ('Oil',            '2% × 1,733',              '35g',     '✓'),
        ('La 8 Plus',      '25% × 1,386',             '347g',    '✓'),
        ('Superiore',      '50% × 1,386',             '693g',    '✓'),
        ('Aroma Tipo 1',   '25% × 1,386',             '346g',    '✓'),
        ('Per ball',       '3,120 ÷ 12',              '260g',    '✓'),
    ],
    header_fill='1A1A1A',
    col_widths=[3.5, 4.5, 3.5, 0.8]
)

# ── Bassinage split ──
add_h2('Refresh Water — Bassinage Pre-Split (607g total)')
add_para('Prepare and label all four portions BEFORE you begin mixing. '
         'All water should be ice water (0–2°C) — make ice water in advance.',
         size=10.5, colour=GREY, space_after=4)
make_table(
    ['Portion', 'Amount', '% of refresh water', 'When to Add'],
    [
        ('Portion 1 (base)',    '365g', '60%', 'Added at start — 0:00 with biga and new flour'),
        ('Portion 2',          '121g', '20%', 'Added slowly — mins 2–8'),
        ('Portion 3',          '91g',  '15%', 'Added slowly — after Portion 2 absorbed'),
        ('Portion 4 + salt',   '30g',  '5%',  'Added with 52g salt at 10-minute mark'),
        ('TOTAL',              '607g', '100%','—'),
    ],
    col_widths=[3.5, 2.0, 3.5, 6.0]
)

# ═══════════════════════════════════════════════════════════════
#  SECTION 3 — SUMMER TEMPERATURE PROTOCOL
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Summer Temperature Protocol')

add_para('Summer conditions (30°C outdoors, humid) fundamentally change your water temperatures. '
         'The standard formulas still apply but the outputs require ice water for the refresh. '
         'MEASURE your actual room and flour temperatures before every mix — do not guess.',
         size=10.5, space_after=6)

warning_box('SUMMER RULE: The refresh ALWAYS requires ice water. Prepare crushed ice and cold '
            'water in advance. Pre-chill your mixer bowl in the freezer for 30 minutes before '
            'the refresh mix begins. Every degree of warmth counts.')

add_h2('Your Mixer — KYS Pro Baker 7 Friction Factors')
info_table([
    ('Biga — 5 min slow mix',       '10°C friction factor'),
    ('Refresh — ~24 min full mix',  '18°C friction factor'),
])

add_h2('Biga Water Temperature Formula')
mono('Biga water temp  =  81  −  (room temp + flour temp + 10)')
add_para('Target biga FDT: 27°C   |   Acceptable: 26–28°C', size=10, colour=GREY, space_after=3)

make_table(
    ['If indoor room temp is...', 'And flour temp is...', 'Use biga water at...', 'Method'],
    [
        ('24°C', '22°C', '25°C', 'Cold tap water'),
        ('26°C', '23°C', '22°C', 'Fridge water'),
        ('28°C', '25°C', '18°C', 'Fridge water + small amount of ice'),
        ('30°C', '27°C', '14°C', 'Ice water mix'),
    ],
    col_widths=[4.0, 3.5, 3.5, 4.0]
)
add_para('Formula: measure your actual temps, then calculate. Do not guess.',
         size=10, colour=GREY, italic=True, space_after=6)

add_h2('Refresh Water Temperature Formula')
mono('Refresh water temp  =  76  −  (room temp + flour temp + biga temp + 18)')
mono('Biga temp from fridge  =  assume 4°C')
add_para('Target refresh FDT: 19°C   |   Stop mixer immediately at 19°C', size=10, colour=GREY, space_after=3)

make_table(
    ['If indoor room temp is...', 'And flour temp is...', 'Refresh water needed', 'Method'],
    [
        ('24°C', '22°C', '8°C',  'Very cold fridge water'),
        ('26°C', '23°C', '5°C',  'Fridge water + ice'),
        ('28°C', '25°C', '1°C',  'Ice water (0–2°C)'),
        ('30°C', '27°C', '−3°C', 'Ice water (0–2°C) — still works due to rounding/chilled bowl'),
    ],
    col_widths=[4.0, 3.5, 3.5, 4.0]
)

warning_box('At 28°C+ indoors, the formula gives a negative result. This is expected. '
            'Use ice water at 0–2°C and pre-chill your mixer bowl. The FDT will land at ~19°C. '
            'Work fast during refresh — every minute in a 30°C kitchen warms the dough.')

add_h2('How to Make Ice Water (0–2°C)')
for i, s in enumerate([
    'Fill a jug with 250g crushed ice.',
    'Add your 607g of cold water to the jug.',
    'Stir until ice is mostly dissolved — temperature will be 0–2°C.',
    'Pre-split into 4 labelled portions immediately before mixing begins.',
    'Keep remaining portions cold (in fridge or ice bath) while you add each one.',
], 1):
    step(i, s)

# ═══════════════════════════════════════════════════════════════
#  SECTION 4 — FLOUR SCIENCE (RECAP)
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Flour Science — Why This Blend Works')

add_h2('The Flour Roles Explained')
add_para('Each flour plays a specific biochemical role. This is not arbitrary — putting the wrong '
         'flour in the wrong stage damages the dough.', size=10.5, space_after=4)

make_table(
    ['Flour', 'Type', 'W', 'P/L (approx)', 'Where', 'Why'],
    [
        ('La 8 Plus',       '0/00', 'W350', '~0.70', 'Biga',
         'Highest protein. Glutenin-rich. Survives 24hr protease activity without degrading.'),
        ('Pizza Superiore', '0/00', 'W340', '~0.65', 'Biga',
         'Strong base. Provides bulk of the biga structure.'),
        ('Aroma',           'TIPO 1', 'W280', '~0.75', 'Biga',
         'Contains wheat germ (lipase → strengthens gluten) and bran (amylase → yeast food, '
         'Maillard → better colour). Sharp bran particles are enzymatically softened by '
         'the 24hr ferment. Generates aromatic compounds. NEVER put Tipo 1 in refresh — '
         'sharp particles cut the fresh gluten network.'),
        ('Nuvola',          '00',   'W270', '~0.45', 'Refresh',
         'Highly extensible (very low P/L). Provides the stretch needed for opening without '
         'tearing. Added fresh so sharp edges are not an issue — it has no bran.'),
    ],
    col_widths=[3.2, 1.4, 1.2, 2.0, 1.4, 5.8]
)

add_h2('Blended Dough P/L Estimate')
add_para('P/L balance determines whether dough springs back (too high) or tears (too low). '
         'Target for Neapolitan pizza: 0.50–0.65.', size=10.5, space_after=4)

make_table(
    ['Flour', '% of total dough', 'Approx P/L', 'Weighted contribution'],
    [
        ('La 8 Plus',       '20%', '0.70', '0.140'),
        ('Pizza Superiore', '40%', '0.65', '0.260'),
        ('Aroma Tipo 1',    '20%', '0.75', '0.150'),
        ('Nuvola',          '20%', '0.45', '0.090'),
        ('BLEND AVERAGE',   '100%', '—',   '0.64  ← within target range'),
    ],
    col_widths=[4.0, 3.5, 3.0, 4.5]
)
add_para('If the dough springs back strongly when opening: add 10% more Nuvola, reduce '
         'Superiore by same amount. If dough tears: reduce Nuvola, increase Superiore.',
         size=10, colour=GREY, italic=True, space_after=6)

add_h2('Pentosan Adjustment — Why We Dropped to 75%')
add_para('Casillo Aroma (Tipo 1) contains pentosans from the bran — non-starch polysaccharides '
         'that absorb up to 10× their weight in water. At 25% of total flour, the Aroma is '
         'absorbing more water than a standard refined flour calculation assumes.',
         size=10.5, space_after=4)
add_para('At 80% hydration (Version 1), the pentosans continued absorbing water during the '
         '24hr cold retard — effectively pushing the real hydration higher and making the '
         'balls progressively slacker. Dropping to 75% compensates for this. The crumb will '
         'still be very open at 75% with proper bulk folds.',
         size=10.5, space_after=6)

# ═══════════════════════════════════════════════════════════════
#  SECTION 5 — FERMENTATION SCIENCE
# ═══════════════════════════════════════════════════════════════
add_h1('What Is Actually Happening During Fermentation')

add_h2('Inside the Biga — 24hr Cold Retard')
add_para('This is not simply "yeast making bubbles." It is a cascade of biochemical activity:',
         size=10.5, space_after=4)
bullet('Yeast converts glucose → CO₂ (leavening) + ethanol (flavour precursor)',
       bold_prefix='Leavening: ')
bullet('At 4°C, yeast shifts metabolism toward ACETIC ACID production '
       '(sharp, complex, vinegary note) vs lactic acid (mild, yoghurty). '
       'This is the flavour signature of a cold-fermented biga.',
       bold_prefix='Flavour: ')
bullet('pH drops from ~6.5 to ~4.5–5.0. Acid tightens gluten (increases P/L). '
       'Yeast self-regulates — lower pH slows fermentation. Protects from bad bacteria.',
       bold_prefix='Acidification: ')
bullet('Amylase (from Aroma germ) breaks starch → maltose → glucose. Continuous yeast food supply.',
       bold_prefix='Amylase: ')
bullet('Protease breaks proteins → amino acids (Maillard reaction precursors → browning on crust). '
       'Slower at 4°C but still active. Contributes to leoparding.',
       bold_prefix='Protease: ')
bullet('Lipase (from Aroma germ) breaks fats → free fatty acids → bond with gluten '
       '→ oxidative cross-linking → STRENGTHENED gluten over time. '
       'This is why Tipo 1 biga doughs have better structure than refined-flour bigas.',
       bold_prefix='Lipase (Aroma): ')
doc.add_paragraph()

add_h2('Summer Impact on Biga Fermentation')
add_para('The biga is protected by the fridge once it\'s in. But the first 30–45 minutes at room '
         'temperature (mixing + transfer) are critical. At 30°C ambient, yeast activity is very '
         'fast before the fridge slows it. This is why you use less yeast (0.7g ADY vs 1.4g in winter) '
         'and get it into the fridge as quickly as possible after mixing.',
         size=10.5, space_after=6)

add_h2('Inside the Refresh — The Biochemical Interactions')
bullet('Acidified biga (pH ~4.5–5) immediately lowers the pH of the fresh flour/water mix. '
       'This is beneficial — tightens new gluten and adds flavour — but also challenges the fresh ADY.',
       bold_prefix='pH shock: ')
bullet('Fresh ADY is added to compensate, but 0.6g (summer) is intentionally low. '
       'Too much yeast in the refresh = over-proofing during the 24hr CT.',
       bold_prefix='Yeast: ')
bullet('Bassinage allows gluten to form at 60% hydration first (easier), '
       'then water is added gradually. Fat (oil) added last coats gluten strands for extensibility.',
       bold_prefix='Bassinage: ')
bullet('Salt added at 10 minutes tightens the gluten network and slows fermentation. '
       'Adding salt too early (in flour) would inhibit yeast before it activates.',
       bold_prefix='Salt timing: ')
bullet('Oil at 16°C: fat molecules intercalate between gluten strands — lubricating them. '
       'Also seals CO₂ bubbles. Added at 16°C (not higher) so it is incorporated before '
       'the gluten network is fully set.',
       bold_prefix='Oil timing: ')
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════
#  SECTION 6 — TIMELINE
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Full Weekend Timeline — Sunday 5PM Bake')

make_table(
    ['Day', 'Time', 'Action', 'Notes'],
    [
        ('Friday',   '7:00 PM', 'Measure room + flour temp. Calculate biga water temp.',
         'Measure twice, mix once.'),
        ('Friday',   '7:15 PM', 'Dissolve 0.7g ADY in 50ml of 35°C water. Wait 5–10 min until foamy.',
         'Do not skip — ADY needs activation in cold water recipe.'),
        ('Friday',   '7:20 PM', 'Mix biga: 347g La 8 Plus + 693g Superiore + 346g Aroma + 693g water + ADY. '
         '5 min slow speed only.',
         'Shaggy texture is correct.'),
        ('Friday',   '7:30 PM', 'Probe FDT in 3 spots. Target 27°C. Cover tightly. Into fridge immediately.',
         'Do not leave at room temp.'),
        ('Saturday', '7:30 PM', 'Pull biga from fridge.',
         '24hr ferment complete.'),
        ('Saturday', '7:35 PM', 'BEGIN AUTOLYSE: mix 347g Nuvola + 365g ice water (Portion 1) by hand. '
         'Rest covered 20 minutes.',
         'No yeast, no biga yet. Just flour + water hydrating.'),
        ('Saturday', '7:55 PM', 'Dissolve 0.6g ADY in small amount of warm water (separate). '
         'Break biga into rough chunks.',
         'Have all four water portions cold and labelled.'),
        ('Saturday', '8:00 PM', 'Begin refresh mix. Add biga chunks + dissolved ADY to autolyse dough. '
         'Slow speed. Add Portion 2 (121g) slowly over 6 minutes.',
         'Bassinage starts.'),
        ('Saturday', '8:08 PM', 'Begin adding Portion 3 (91g) slowly.',
         'Dough should be coming together.'),
        ('Saturday', '8:10 PM', 'Add 52g salt + Portion 4 (30g water). Continue slow 5 minutes.',
         'Salt tightens gluten.'),
        ('Saturday', '8:15 PM', 'Switch to FAST speed. Insert probe thermometer.',
         'Monitor constantly from here.'),
        ('Saturday', '16°C',    'Drizzle in 35g EVOO slowly while fast mixing continues.',
         'Do not add oil before 16°C.'),
        ('Saturday', '19°C',    'STOP MIXER. Total mix time ~22–24 min.',
         'Do not overshoot FDT.'),
        ('Saturday', '~8:25 PM','COIL FOLD 1 on full dough mass. Cover. Rest 15 min.',
         'This is the step that was skipped in V1.'),
        ('Saturday', '~8:40 PM','COIL FOLD 2. Cover. Rest 15 min.',
         'Dough should already feel stronger.'),
        ('Saturday', '~8:55 PM','COIL FOLD 3. Dough should feel noticeably more structured.',
         'One more fold if still very slack.'),
        ('Saturday', '~9:10 PM','Divide into 12 × 260g pieces. Ball tightly. Lightly oil tray.',
         'Tight skin tension is the goal.'),
        ('Saturday', '~9:15 PM','30 min rest at room temperature. Cover.',
         'Let balls relax before cold shock.'),
        ('Saturday', '~9:45 PM','Into fridge. 24hr cold retard at 4°C.',
         'No touching until Sunday afternoon.'),
        ('Sunday',   '3:00 PM', 'Pull tray from fridge. Leave covered at room temperature.',
         '30°C ambient = ~2hr proof. Watch the balls, not the clock.'),
        ('Sunday',   '3:30 PM', 'Turn oven to maximum (390°C). Allow full 1.5hr to reach temp.',
         'Stone/deck must be fully saturated with heat.'),
        ('Sunday',   '4:30 PM', 'CHECK BALLS: are they visibly puffed? Jiggling when tray shaken?',
         'If yes: ready soon. If no: give more time.'),
        ('Sunday',   '5:00 PM', 'BAKE.',
         'First pizza in. 2.5–4 min. Rotate halfway.'),
    ],
    col_widths=[1.8, 1.8, 8.4, 3.0]
)

# ═══════════════════════════════════════════════════════════════
#  SECTION 7 — STAGE BY STAGE PROCESS
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
banner('STAGE 1 — BIGA  (Friday Evening)')

add_h2('What You Are Doing And Why')
add_para('The biga is a stiff pre-ferment at 50% hydration. You are creating the conditions for '
         '24hrs of slow, cold, complex fermentation. The Tipo 1 Aroma flour is in here deliberately '
         '— the 24hr ferment enzymatically softens its bran particles and activates its '
         'germ lipase to strengthen the gluten.',
         size=10.5, space_after=6)

add_h2('Step by Step')
for i, s in enumerate([
    'Measure indoor room temperature and flour temperature with probe thermometer. Write them down.',
    'Calculate biga water temperature:  81 − (room + flour + 10).  Prepare that water.',
    'Take 50ml from your biga water. Warm to 35°C. Dissolve 0.7g ADY. '
     'Wait 5–10 minutes — it should look slightly foamy or creamy.',
    'Combine the remaining cold biga water with the ADY solution.',
    'Weigh flour into mixer bowl: La 8 Plus 347g + Pizza Superiore 693g + Aroma Tipo 1 346g.',
    'Pour all 693g water (with dissolved ADY) into the flour.',
    'Mix SLOW speed only for exactly 5 minutes. Dough will look rough and shaggy — this is correct.',
    'Probe FDT in 3 different spots. Target 27°C. If below 25°C: leave 10 min at room temp. '
     'If above 28°C: get it in the fridge immediately.',
    'Cover bowl tightly with cling film or lid. Transfer straight to fridge.',
    'Note the exact time. 24 hours from now is your refresh.',
], 1):
    step(i, s)

# ── STAGE 2 ──
doc.add_page_break()
banner('STAGE 2 — AUTOLYSE + REFRESH  (Saturday Evening)')

add_h2('The Autolyse — New Step Not In Version 1')
add_para('Autolyse is a 20-minute rest of the new flour and water only, before the biga is '
         'added. During this rest, the Nuvola flour hydrates and gluten begins forming passively '
         'with zero mechanical stress. Result: better extensibility, shorter final mix time, '
         'more open crumb. This is standard practice in high-hydration Neapolitan doughs.',
         size=10.5, space_after=4)

warning_box('SUMMER: All refresh water must be ice water (0–2°C). Prepare ice water BEFORE '
            'pulling the biga from the fridge. Pre-chill your mixer bowl in the freezer '
            'for 30 minutes.')

add_h2('Autolyse Steps')
for i, s in enumerate([
    'Prepare 607g ice water. Split into 4 labelled portions: 365g / 121g / 91g / 30g.',
    'Keep all portions cold — in fridge or ice bath.',
    'Pull biga from fridge. Do not bring to room temperature.',
    'In mixer bowl (chilled): combine 347g Nuvola + Portion 1 (365g ice water).',
    'Mix briefly by hand or 1 minute slow until just combined — no dry flour remaining.',
    'Cover. Rest 20 minutes. Do not mix.',
    'Meanwhile: dissolve 0.6g ADY in a small amount of warm water (35°C). Set aside.',
    'Break biga into rough fist-sized chunks.',
], 1):
    step(i, s)

add_h2('Refresh Mixing Sequence')
make_table(
    ['Time / Temp', 'Action'],
    [
        ('0:00',  'Add biga chunks + dissolved ADY to autolyse dough in bowl. Slow speed.'),
        ('0:00',  'Begin adding Portion 2 (121g) very slowly — take 6 full minutes.'),
        ('6:00',  'Portion 2 fully absorbed. Begin adding Portion 3 (91g) slowly.'),
        ('~8:00', 'Portion 3 absorbed. Add 52g SALT + Portion 4 (30g water). Continue slow 5 min.'),
        ('13:00', 'Switch to FAST speed. Insert probe thermometer. Watch temperature constantly.'),
        ('16°C',  'Drizzle 35g EVOO slowly into running mixer.'),
        ('19°C',  'STOP. Check probe in 2 spots. If both 19°C: done. Total time ~22–24 min.'),
    ],
    header_fill='1A1A1A',
    col_widths=[2.5, 12.5]
)

add_para('Do not overshoot 19°C. Once you stop, the dough will continue to warm slightly '
         'from residual friction. In a 30°C kitchen, every minute matters.',
         size=10, colour=ORANGE, italic=True, space_after=4)

# ── STAGE 3 ──
doc.add_page_break()
banner('STAGE 3 — BULK COIL FOLDS + BALLING  (Saturday Evening)')

add_h2('Why This Stage Makes Or Breaks The Crumb')
add_para('This is the step that was skipped in Version 1 and produced the flat, merged balls '
         'and closed crumb. Bulk coil folds on the full dough mass before balling do three things: '
         '(1) Align and layer gluten strands — trapping CO₂ in large, irregular pockets (open crumb); '
         '(2) Redistribute temperature evenly through the mass; '
         '(3) Build surface tension so when balled, the skin is pre-developed.',
         size=10.5, space_after=6)

add_h2('How to Coil Fold')
add_para('Tip dough onto a lightly OILED surface (not floured). Slide both hands under the '
         'centre of the dough. Lift the centre up and let both ends fold down under gravity. '
         'Rotate 90°. Repeat. That is one set.',
         size=10.5, space_after=4)

add_h2('Fold Schedule (15-minute intervals in summer)')
make_table(
    ['Time after mixing', 'Action'],
    [
        ('0 min',  'Leave dough in bowl, covered. Rest 5 minutes.'),
        ('5 min',  'Tip onto oiled surface. COIL FOLD 1: 4 lifts (N/S/E/W). Rough round shape. Cover.'),
        ('20 min', 'COIL FOLD 2: 4 lifts. Dough should already feel more structured and less sticky.'),
        ('35 min', 'COIL FOLD 3: 4 lifts. Dough should hold its shape and feel alive with tension.'),
        ('45 min', 'Optional COIL FOLD 4 if dough still feels very slack.'),
    ],
    header_fill='1A1A1A',
    col_widths=[4.0, 11.0]
)

warning_box('SUMMER: Work quickly during folds. Each minute at 30°C warms the dough. '
            'If the kitchen is very hot, do folds near an air vent or cool area.')

add_h2('Dividing and Balling')
for i, s in enumerate([
    'After final fold, leave dough to rest 5 minutes.',
    'Weigh 12 pieces at 260g each using scales and dough scraper.',
    'Ball each piece: stretch the surface skin firmly downward and under, '
     'pinching underneath. Rotate on the oiled surface to build tension. '
     'The top should be a smooth, taut dome.',
    'Place into well-oiled tray with space between each ball.',
    'Cover tray. Rest at room temperature for 30 minutes.',
    'Transfer to fridge. Cover tightly. Cold retard for 24 hours.',
    'Note the time. This is also when you will pull them on Sunday.',
], 1):
    step(i, s)

add_h2('What Good Balled Dough Looks Like Going In')
bullet('Smooth, taut surface skin — no tearing or rough edges')
bullet('Holds a domed shape without collapsing immediately')
bullet('Stays as individual balls — does not immediately merge with neighbours')
bullet('Some spreading over the 30min RT rest is normal, but they should remain distinct')

# ── STAGE 4 ──
doc.add_page_break()
banner('STAGE 4 — PROOF & BAKE  (Sunday)')

add_h2('Pulling From The Fridge — Summer Timing')
warning_box('At 30°C ambient, balls will proof approximately TWICE as fast as at 20°C. '
            'The standard 3-hour pull has become 1.5–2 hours. Watch the balls — not the clock.')

make_table(
    ['Stage', 'Time', 'What To Look For'],
    [
        ('Pull from fridge',    '3:00 PM',  'Balls are cold, firm, possibly domed from CT. Leave covered at RT.'),
        ('First check',         '3:45 PM',  'Any signs of life? Slight softening? Small puff on top?'),
        ('Second check',        '4:15 PM',  'Should be visibly larger and softer. Jiggle the tray lightly.'),
        ('Ready to open',       '~4:30–5:00 PM', 'Balls jiggle. Visibly puffed. Lightly press: impression fills back slowly.'),
        ('Over-proofed warning','Past 5:15 PM', 'Very flat, very sticky, no spring when pressed. Bake immediately if this happens.'),
    ],
    col_widths=[3.5, 2.5, 9.0]
)

add_h2('The Poke Test')
add_para('Press one finger ~1cm into the side of a ball. Watch what happens:', size=10.5, space_after=3)
bullet('Fills back immediately → under-proofed. Give more time.')
bullet('Fills back slowly over 3–5 seconds → perfect. Bake now.')
bullet('Stays depressed, does not fill back → over-proofed. Bake immediately.')

add_h2('Opening — Gigi Style (Open Cornicione)')
add_para('The goal is maximum oven spring and an open, airy cornicione. Every technique choice '
         'here affects the final result.', size=10.5, space_after=4)
for i, s in enumerate([
    'Dust your peel lightly with semolina. Not flour — semolina slides better.',
    'Place ball on a semolina-dusted work surface.',
    'Press from the CENTRE outward with three fingertips. Rotate the ball quarter turns. '
     'DO NOT press the outer 2cm crust edge — this becomes your cornicione. '
     'Protecting this edge is everything.',
    'When disk is ~20cm: pick up and hang over both fists. Let gravity stretch downward. '
     'Rotate slowly. Do not pull — let weight do the work.',
    'If dough resists and springs back: lay it down, rest 2 minutes, try again. '
     'Fighting tight gluten tears the dough.',
    'Target: 30–32cm diameter. Thick edge, thin centre.',
    'Check slide on peel before topping — shake peel gently. If dough sticks: lift edge, '
     'add more semolina underneath.',
    'Top quickly. Every second the dough sits on the peel it absorbs moisture and sticks.',
], 1):
    step(i, s)

add_h2('Baking')
info_table([
    ('Oven temp',         '380–390°C  (electric deck)'),
    ('Preheat time',      'Minimum 1.5 hours at full temperature before first pizza'),
    ('Launch',            'Confident quick motion — hesitation = sticking'),
    ('Bake time',         '2.5–4 minutes — watch, not timer'),
    ('Rotation',          'Rotate 180° after 90 seconds for even leoparding'),
    ('Done signal',       'Crust has leopard spotting, base sounds hollow, cornicione puffed and coloured'),
    ('Between pizzas',    'Allow 2 minutes for deck to recover heat before next launch'),
])

# ═══════════════════════════════════════════════════════════════
#  SECTION 8 — TROUBLESHOOTING
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Troubleshooting — Problems And Fixes')

make_table(
    ['Problem', 'Likely Cause', 'Fix'],
    [
        ('Biga FDT too low (below 25°C)',
         'Water was too cold',
         'Leave biga at room temp 15–20 min before fridge. Check temp again.'),
        ('Biga FDT too high (above 29°C)',
         'Water was too warm / room warmer than expected',
         'Get into fridge immediately. Reduce yeast next time.'),
        ('Balls merge and flatten overnight',
         'Insufficient bulk folds / too high hydration',
         'Re-ball cold (straight from fridge) next morning. Reduce to 73% next bake.'),
        ('Dough tears when opening',
         'Under-proofed / too cold / gluten too tight (high P)',
         'Rest 2–3 min before trying again. Ensure balls are at room temp before opening.'),
        ('Dough is impossible to open — keeps springing back',
         'P/L ratio too high — dough too elastic',
         'Increase Nuvola in next bake. Rest longer before opening.'),
        ('Cornicione flat — no oven spring',
         'Skipped bulk folds / over-proofed / crust edge pressed during opening',
         'Confirm folds were done. Protect crust edge during opening.'),
        ('Balls over-proof before baking',
         'Too warm at room temp / proofed too long / too much yeast',
         'Pull from fridge later. In 30°C kitchen, 90 minutes may be enough.'),
        ('Dough sticky and impossible to handle',
         'Over-proofed / too much water absorbed by Tipo 1 pentosans',
         'Chill hands, flour work surface lightly. Drop to 73% next bake.'),
        ('Crust pale — no leoparding',
         'Oven not hot enough / insufficient fermentation (amino acids)',
         'Preheat longer. Check oven thermometer. Ensure full 24hr biga ferment.'),
        ('Crust tastes flat / no complexity',
         'Short ferment / biga did not develop properly / FDT too low',
         'Confirm biga FDT 27°C. Ensure full 24hr cold retard. Consider 36hr biga.'),
    ],
    col_widths=[4.0, 5.0, 6.0]
)

# ═══════════════════════════════════════════════════════════════
#  QUICK REFERENCE — BACK PAGE
# ═══════════════════════════════════════════════════════════════
doc.add_page_break()
add_h1('Quick Reference Card')

add_h2('All Weights At A Glance')
make_table(
    ['Ingredient', 'Weight', 'Stage', 'Timing'],
    [
        ('Casillo La 8 Plus',       '347g',  'Biga',    'Friday'),
        ('Casillo Pizza Superiore', '693g',  'Biga',    'Friday'),
        ('Casillo Aroma Tipo 1',    '346g',  'Biga',    'Friday'),
        ('Biga water (calc. temp)', '693g',  'Biga',    'Friday'),
        ('ADY',                     '0.7g',  'Biga',    'Friday — dissolve in 35°C water first'),
        ('Caputo Nuvola',           '347g',  'Autolyse','Saturday — rest 20 min with water before biga'),
        ('Refresh water — P1',      '365g',  'Autolyse','Saturday — ice water, added at 0:00'),
        ('Refresh water — P2',      '121g',  'Refresh', 'Saturday — added slowly 0:02–0:08'),
        ('Refresh water — P3',      '91g',   'Refresh', 'Saturday — added after P2'),
        ('Refresh water — P4',      '30g',   'Refresh', 'Saturday — added with salt at 0:10'),
        ('ADY',                     '0.6g',  'Refresh', 'Saturday — dissolved before adding'),
        ('Salt',                    '52g',   'Refresh', 'Saturday — added at 10-minute mark ONLY'),
        ('EVOO',                    '35g',   'Refresh', 'Saturday — added when probe hits 16°C ONLY'),
    ],
    col_widths=[4.0, 1.8, 2.2, 7.0]
)

add_h2('Temperature Formulas')
mono('BIGA water temp   =  81  −  (room + flour + 10)',        size=10, colour=BLACK)
mono('REFRESH water temp =  76  −  (room + flour + 4 + 18)',   size=10, colour=BLACK)
mono('If result is below 5°C  →  use ice water',               size=10, colour=ORANGE)
doc.add_paragraph()

add_h2('Signs Dough Is Ready To Bake')
bullet('Visibly larger and domed vs when they came out of fridge')
bullet('Jiggle noticeably when tray is shaken')
bullet('Poke test: finger impression fills back slowly over 3–5 seconds')
bullet('Surface looks soft and pillowy, not tight and shiny')
doc.add_paragraph()

add_h2('Fermentation Temperatures (for reference)')
info_table([
    ('Yeast optimal activity',  '27–37°C'),
    ('Yeast dormant',           'Below 4°C'),
    ('Yeast dies',              'Above 50°C'),
    ('ADY activation water',    '35°C  (never above 43°C)'),
    ('Biga FDT target',         '27°C  (26–28°C acceptable)'),
    ('Refresh FDT target',      '19°C  (stop immediately)'),
    ('EVOO addition temp',      '16°C'),
    ('Salt addition',           '10-minute mark — not temperature-dependent'),
    ('CT fridge temp',          '4°C'),
])

# ── Save ──────────────────────────────────────────────────────
path = '/home/user/Pizza/Dough_Eyed_Gigi_V2_Summer.docx'
doc.save(path)
print(f'Saved: {path}')
