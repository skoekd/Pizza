from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin   = Cm(2.0)
    section.right_margin  = Cm(2.0)

# ── Colour palette ────────────────────────────────────────────────────────────
BLACK  = RGBColor(0x1a, 0x1a, 0x1a)
RED    = RGBColor(0xC0, 0x39, 0x2B)
GREY   = RGBColor(0x44, 0x44, 0x44)
LGREY  = RGBColor(0xF2, 0xF2, 0xF2)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
DKRED  = RGBColor(0x96, 0x28, 0x1E)

# ── Helper: shade a table cell ────────────────────────────────────────────────
def shade_cell(cell, hex_colour):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_colour)
    tcPr.append(shd)

def set_cell_border(cell, **kwargs):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top','left','bottom','right','insideH','insideV'):
        tag = OxmlElement(f'w:{edge}')
        tag.set(qn('w:val'),  kwargs.get('val',  'none'))
        tag.set(qn('w:sz'),   kwargs.get('sz',   '0'))
        tag.set(qn('w:space'),'0')
        tag.set(qn('w:color'),kwargs.get('color','auto'))
        tcBorders.append(tag)
    tcPr.append(tcBorders)

# ── Helper: paragraph helpers ─────────────────────────────────────────────────
def add_para(text='', bold=False, size=11, colour=BLACK, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, font='Calibri'):
    p   = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.bold        = bold
        run.font.name   = font
        run.font.size   = Pt(size)
        run.font.color.rgb = colour
    return p

def add_heading(text, size=16, colour=RED, space_before=14, space_after=4):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    run = p.add_run(text.upper())
    run.bold           = True
    run.font.name      = 'Calibri'
    run.font.size      = Pt(size)
    run.font.color.rgb = colour
    return p

def add_subheading(text, size=11, colour=GREY):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text.upper())
    run.bold           = True
    run.font.name      = 'Calibri'
    run.font.size      = Pt(size)
    run.font.color.rgb = colour
    return p

def add_rule(colour_hex='C0392B'):
    p   = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    pPr = p._p.get_or_add_pPr()
    pb  = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    '6')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), colour_hex)
    pb.append(bot)
    pPr.append(pb)
    return p

def mono(text, size=9.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(1)
    run = p.add_run(text)
    run.font.name  = 'Courier New'
    run.font.size  = Pt(size)
    run.font.color.rgb = GREY
    return p

def bullet(text, size=10.5):
    p   = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.font.name  = 'Calibri'
    run.font.size  = Pt(size)
    run.font.color.rgb = BLACK
    return p

# ── Simple 2-col info table ───────────────────────────────────────────────────
def info_table(rows):
    t = doc.add_table(rows=len(rows), cols=2)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, (label, val) in enumerate(rows):
        shade = 'F2F2F2' if i % 2 == 0 else 'FFFFFF'
        lc = t.cell(i, 0)
        vc = t.cell(i, 1)
        shade_cell(lc, shade)
        shade_cell(vc, shade)
        lp = lc.paragraphs[0]
        vp = vc.paragraphs[0]
        lr = lp.add_run(label)
        vr = vp.add_run(val)
        lr.bold = True
        lr.font.name = vr.font.name = 'Calibri'
        lr.font.size = vr.font.size = Pt(10)
        lr.font.color.rgb = BLACK
        vr.font.color.rgb = GREY
    t.columns[0].width = Cm(5.5)
    t.columns[1].width = Cm(9.5)
    doc.add_paragraph()

# ── Header block ─────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(2)
r = p.add_run('DOUGH EYED STYLE PIZZA DOUGH')
r.bold = True
r.font.name = 'Calibri'
r.font.size = Pt(22)
r.font.color.rgb = RED

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.paragraph_format.space_after = Pt(4)
r2 = p2.add_run('Contemporary Neapolitan  |  80% Biga  |  80% Hydration  |  8 × 260g Balls')
r2.font.name = 'Calibri'
r2.font.size = Pt(11)
r2.font.color.rgb = GREY

add_rule()

# ── OVERVIEW ─────────────────────────────────────────────────────────────────
add_heading('Overview', size=13, space_before=10)
info_table([
    ('Style',          'Contemporary Neapolitan'),
    ('Yield',          '8 dough balls × 260g'),
    ('Total Flour',    '1,140g'),
    ('Total Water',    '912g  (80% hydration)'),
    ('Pre-ferment',    '80% Biga / 20% Refresh'),
    ('Total Dough',    '~2,086g  (260.75g per ball)'),
    ('Oven',           'Electric deck  |  380–390°C'),
    ('Cook Time',      '2.5–4 minutes per pizza'),
])

# ── EQUIPMENT ────────────────────────────────────────────────────────────────
add_heading('Equipment', size=13, space_before=6)
for item in [
    'KYS Pro Baker 7 spiral mixer',
    'Probe thermometer  (essential)',
    '0.1g precision scale',
    'Standard kitchen scales',
    '8 airtight dough containers',
    'Dough scraper',
    'Oiled surface for folding',
]:
    bullet(item)
doc.add_paragraph()

# ── FLOUR ────────────────────────────────────────────────────────────────────
add_heading('Flour Breakdown', size=13, space_before=6)
add_rule()

add_subheading('Biga Flour — 912g  (80% of total)')
t = doc.add_table(rows=4, cols=4)
t.style = 'Table Grid'
headers = ['Flour', 'Weight', 'W Value', 'Protein']
vals    = [
    ('Casillo La 8 Plus',       '228g', 'W350', '14.5%'),
    ('Casillo Pizza Superiore', '456g', 'W340', '13.5%'),
    ('Casillo Aroma',           '228g', 'W280', '13.0%'),
]
for i, h in enumerate(headers):
    c = t.cell(0, i)
    shade_cell(c, 'C0392B')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
for ri, row in enumerate(vals):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate(row):
        c = t.cell(ri+1, ci)
        shade_cell(c, shade)
        r = c.paragraphs[0].add_run(val)
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        r.font.color.rgb = BLACK if ci == 0 else GREY
        if ci == 0:
            r.bold = True
doc.add_paragraph()

add_subheading('Refresh Flour — 228g  (20% of total)')
t2 = doc.add_table(rows=2, cols=4)
t2.style = 'Table Grid'
for i, h in enumerate(headers):
    c = t2.cell(0, i)
    shade_cell(c, 'C0392B')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
for ci, val in enumerate(('Caputo Nuvola', '228g', 'W270', '12.5%')):
    c = t2.cell(1, ci)
    shade_cell(c, 'F2F2F2')
    r = c.paragraphs[0].add_run(val)
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = BLACK if ci == 0 else GREY
    if ci == 0:
        r.bold = True
doc.add_paragraph()

add_para('Why this split: Strong flours (La 8 Plus + Superiore) survive the 24hr cold biga fermentation without degrading. '
         'Aroma adds flavour complexity. Nuvola goes in the refresh for maximum extensibility and open crumb on the day.',
         size=9.5, colour=GREY, space_after=4)

# ── WATER ────────────────────────────────────────────────────────────────────
add_heading('Water', size=13, space_before=10)
add_rule()
info_table([
    ('Total water',   '912g  =  80% of 1,140g flour'),
    ('Biga water',    '456g  =  50% of biga flour (912g)'),
    ('Refresh water', '456g  =  total water minus biga water'),
])

# ── YEAST ────────────────────────────────────────────────────────────────────
add_heading('Yeast & Seasoning', size=13, space_before=6)
add_rule()
info_table([
    ('Biga ADY',     '1.4g   (0.3% of biga flour, converted from fresh)'),
    ('Refresh ADY',  '1.7g   (3g per kg of total flour, converted from fresh)'),
    ('Salt',         '34g    (3% of total flour — refresh only)'),
    ('EVOO',         '23g    (2% of total flour — refresh only, added at 16°C)'),
])
add_para('A 0.1g precision scale is essential for measuring yeast accurately.', size=9.5, colour=GREY)

# ── TEMPERATURE ──────────────────────────────────────────────────────────────
add_heading('Temperature Calculations', size=13, space_before=10)
add_rule()

add_subheading('Mixer Friction Factors — KYS Pro Baker 7')
info_table([
    ('Biga  (5 min slow mix)',     '10°C'),
    ('Refresh  (24 min full mix)', '18°C'),
])

add_subheading('Biga Water Temperature Formula')
mono('Water temp  =  81  −  (room temp + flour temp + 10)')
add_para('Biga target FDT: 27°C    |    Acceptable range: 26–28°C', size=10, colour=GREY, space_after=2)
add_para('This session: room 23.5°C, flour 19°C  →  81 − (23.5 + 19 + 10)  =  28.5°C  →  29°C',
         size=9.5, colour=GREY, space_after=8)

add_subheading('Refresh Water Temperature Formula')
mono('Water temp  =  76  −  (room temp + flour temp + 4 + 18)')
add_para('Refresh target FDT: 19°C    |    Biga temp from fridge: 4°C', size=10, colour=GREY, space_after=2)
add_para('This session: room 21°C, flour 17°C  →  76 − (21 + 17 + 4 + 18)  =  16°C',
         size=9.5, colour=GREY, space_after=8)

# ── PAGE BREAK ────────────────────────────────────────────────────────────────
doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  STAGE 1 — BIGA
# ══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
r = p.add_run('STAGE 1 — BIGA')
r.bold = True
r.font.name = 'Calibri'
r.font.size = Pt(17)
r.font.color.rgb = WHITE
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(0)

# Red banner
pPr   = p._p.get_or_add_pPr()
shd   = OxmlElement('w:shd')
shd.set(qn('w:val'),   'clear')
shd.set(qn('w:color'), 'auto')
shd.set(qn('w:fill'),  'C0392B')
pPr.append(shd)
p.paragraph_format.left_indent = Cm(0.3)

doc.add_paragraph()

add_subheading('Biga — At A Glance')
info_table([
    ('Flour',       '912g  (La 8 Plus 228g + Pizza Superiore 456g + Aroma 228g)'),
    ('Water',       '456g  at calculated temperature'),
    ('Active Dry',  '1.4g'),
    ('Target FDT',  '27°C   (acceptable: 26–28°C)'),
    ('Mix time',    '5 minutes slow (~80 RPM)'),
    ('Ferment',     '24 hours cold retard at ~4°C'),
])

add_heading('Biga Instructions', size=12, space_before=8)
add_rule()

add_subheading('Before Mixing')
steps_biga_pre = [
    'Weigh biga flour into mixer bowl: La 8 Plus 228g + Pizza Superiore 456g + Aroma 228g.',
    'Measure room temperature and flour temperature with probe thermometer.',
    'Calculate biga water temperature:  Water = 81 − (room + flour + 10).',
    'Activate ADY: take ~50g from your 456g total water. Warm that 50g to ~35°C. '
     'Dissolve 1.4g ADY into it. Wait 5–10 minutes until foamy. '
     'Adjust remaining water temperature so the full 456g averages your calculated target.',
]
for i, s in enumerate(steps_biga_pre, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(3)
    r1 = p.add_run(f'{i}.  ')
    r1.bold = True
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = RED
    r2 = p.add_run(s)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = BLACK

add_subheading('Mixing')
mono('Pour 456g water into flour bowl')
mono('Mix on SLOW speed (~80 RPM) for exactly 5 minutes')
mono('Dough will look rough and shaggy — this is correct for a biga')
mono('Probe dough temperature in 3 different spots')
mono('Target: 27°C   |   Acceptable: 26–28°C')
doc.add_paragraph()

add_subheading('Into The Fridge')
for s in [
    'Cover bowl tightly with cling film or lid.',
    'Place straight into fridge immediately — do not leave at room temperature.',
    'Ferment for 24 hours at approximately 4°C.',
    'Note the exact time going in so you know when to pull it tomorrow.',
]:
    bullet(s)

# ══════════════════════════════════════════════════════════════════════════════
#  STAGE 2 — REFRESH
# ══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()

p = doc.add_paragraph()
r = p.add_run('STAGE 2 — REFRESH')
r.bold = True
r.font.name = 'Calibri'
r.font.size = Pt(17)
r.font.color.rgb = WHITE
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(0)
pPr = p._p.get_or_add_pPr()
shd = OxmlElement('w:shd')
shd.set(qn('w:val'),   'clear')
shd.set(qn('w:color'), 'auto')
shd.set(qn('w:fill'),  'C0392B')
pPr.append(shd)
p.paragraph_format.left_indent = Cm(0.3)

doc.add_paragraph()

add_subheading('Refresh — At A Glance')
info_table([
    ('Fresh flour',  '228g  (Caputo Nuvola)'),
    ('Water',        '456g  at calculated temperature'),
    ('Active Dry',   '1.7g  (dissolved before adding)'),
    ('Salt',         '34g   (added at 10 minute mark only)'),
    ('EVOO',         '23g   (added when dough hits 16°C only)'),
    ('Target FDT',   '19°C'),
    ('Mix time',     '~22–24 minutes total'),
])

add_heading('Water Bassinage — Pre-Split Before Starting', size=12, space_before=8)
add_rule()
add_para('Split your 456g of water into four portions and label them before mixing begins.', size=10, colour=GREY, space_after=4)

t3 = doc.add_table(rows=5, cols=3)
t3.style = 'Table Grid'
for i, h in enumerate(['Portion', 'Amount', 'When to Add']):
    c = t3.cell(0, i)
    shade_cell(c, 'C0392B')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
bass_rows = [
    ('Portion 1', '274g', 'Added first — 0:00'),
    ('Portion 2',  '91g', 'Added slowly — mins 2 to 8'),
    ('Portion 3',  '68g', 'Added slowly — after Portion 2'),
    ('Portion 4',  '23g', 'Reserved — added with salt at 10 min mark'),
]
for ri, (a, b, c_) in enumerate(bass_rows):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate((a, b, c_)):
        cell = t3.cell(ri+1, ci)
        shade_cell(cell, shade)
        run = cell.paragraphs[0].add_run(val)
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK if ci == 0 else GREY
        if ci == 0:
            run.bold = True

doc.add_paragraph()
mono('Total: 274 + 91 + 68 + 23 = 456g ✓')
doc.add_paragraph()

add_heading('Refresh Instructions', size=12, space_before=8)
add_rule()

add_subheading('Before Mixing')
pre_steps = [
    'Measure room temperature and flour temperature.',
    'Calculate refresh water temperature:  Water = 76 − (room + flour + 4 + 18).',
    'Pre-split 456g water into the four portions shown above.',
    'Dissolve 1.7g ADY in a small amount of warm water. Set aside.',
    'Have salt (34g) and EVOO (23g) weighed and ready — do not add yet.',
    'Weigh 228g Caputo Nuvola.',
    'Remove biga from fridge. Break into rough chunks.',
]
for i, s in enumerate(pre_steps, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(3)
    r1 = p.add_run(f'{i}.  ')
    r1.bold = True
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = RED
    r2 = p.add_run(s)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = BLACK

add_subheading('Mixing Sequence')
mix_steps = [
    ('0:00', 'Biga chunks + 228g Nuvola + dissolved ADY into bowl. Add Portion 1 (274g). SLOW speed (~80 RPM).'),
    ('0:02', 'Dough begins coming together. Slowly add Portion 2 (91g) — take your time over 6 minutes.'),
    ('0:08', 'Portion 2 fully added. Begin slowly adding Portion 3 (68g). Keep Portion 4 reserved.'),
    ('0:10', 'Add 34g SALT + Portion 4 (23g water). Continue SLOW for 5 more minutes.'),
    ('0:15', 'Switch to FAST speed (~220–250 RPM). Insert probe thermometer and monitor closely.'),
    ('16°C', 'Dough reaches 16°C  →  slowly drizzle in 23g EVOO. Continue mixing.'),
    ('19°C', 'Dough reaches 19°C  →  STOP MIXER immediately. Total mix: ~22–24 minutes.'),
]
t4 = doc.add_table(rows=len(mix_steps)+1, cols=2)
t4.style = 'Table Grid'
for i, h in enumerate(['Time / Temp', 'Action']):
    c = t4.cell(0, i)
    shade_cell(c, '1a1a1a')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
for ri, (time_, action) in enumerate(mix_steps):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    c0 = t4.cell(ri+1, 0)
    c1 = t4.cell(ri+1, 1)
    shade_cell(c0, shade)
    shade_cell(c1, shade)
    r0 = c0.paragraphs[0].add_run(time_)
    r0.bold = True
    r0.font.name = 'Calibri'
    r0.font.size = Pt(10)
    r0.font.color.rgb = RED
    r1 = c1.paragraphs[0].add_run(action)
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10)
    r1.font.color.rgb = BLACK
t4.columns[0].width = Cm(2.2)
t4.columns[1].width = Cm(12.8)
doc.add_paragraph()

# ── PAGE BREAK ────────────────────────────────────────────────────────────────
doc.add_page_break()

# ── AFTER MIXING ─────────────────────────────────────────────────────────────
add_heading('After Mixing — Fold, Rest & Ball', size=13, space_before=0)
add_rule()

fold_steps = [
    'Leave dough to rest in bowl with lid on for 5 minutes.',
    'Tip dough onto a lightly oiled surface.',
    'Perform 3–4 folds: stretch one side up and fold to the centre, rotate 90°, repeat.',
    'Shape into a smooth round mass. Lightly oil the top. Cover.',
    'Rest covered at room temperature for 20–30 minutes.',
    'Divide into 8 equal pieces at 260g each using scales.',
    'Shape each piece into a tight smooth ball.',
    'Place each ball into its own sealed container.',
    'Rest containers at room temperature for 30 minutes.',
    'Transfer all containers to fridge. Cold retard for 24 hours.',
]
for i, s in enumerate(fold_steps, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(4)
    r1 = p.add_run(f'{i}.  ')
    r1.bold = True
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = RED
    r2 = p.add_run(s)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = BLACK

# ── BAKING ───────────────────────────────────────────────────────────────────
add_heading('Baking', size=13, space_before=10)
add_rule()
info_table([
    ('Temper time',   '3 hours at room temperature before baking'),
    ('Oven temp',     '380–390°C  (electric deck oven)'),
    ('Cook time',     '2.5–4 minutes per pizza'),
    ('Watch for',     'Even browning on base and cornicione'),
])

# ── TIMELINE ─────────────────────────────────────────────────────────────────
add_heading('Timeline', size=13, space_before=10)
add_rule()

t5 = doc.add_table(rows=6, cols=3)
t5.style = 'Table Grid'
for i, h in enumerate(['Day', 'Time', 'Action']):
    c = t5.cell(0, i)
    shade_cell(c, 'C0392B')
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = WHITE
timeline = [
    ('Friday',   '~10:00 AM', 'Make biga  →  into fridge (24hrs CT)'),
    ('Saturday', '~10:00 AM', 'Refresh  →  fold  →  rest  →  ball  →  into fridge (24hrs CT)'),
    ('Sunday',   ' 2:00 PM',  'Remove all 8 balls from fridge. Leave at room temp, lids on.'),
    ('Sunday',   ' 5:00 PM',  'Bake at 380–390°C'),
    ('',         '',          'Dough balls rest 3 hours at room temp before baking.'),
]
for ri, (day, time_, act) in enumerate(timeline):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate((day, time_, act)):
        cell = t5.cell(ri+1, ci)
        shade_cell(cell, shade)
        run = cell.paragraphs[0].add_run(val)
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK if ci == 0 else GREY
        if ci == 0:
            run.bold = True
t5.columns[0].width = Cm(2.5)
t5.columns[1].width = Cm(2.8)
t5.columns[2].width = Cm(9.7)
doc.add_paragraph()

# ── FINAL NUMBERS CHECK ───────────────────────────────────────────────────────
add_heading('Final Numbers Check', size=13, space_before=10)
add_rule()

checks = [
    ('Biga flour',    '228 + 456 + 228  =  912g  (80% of 1,140g)', '✓'),
    ('Refresh flour', '228g Nuvola  (20% of 1,140g)',               '✓'),
    ('Total flour',   '912 + 228  =  1,140g',                       '✓'),
    ('Biga water',    '50% × 912  =  456g',                         '✓'),
    ('Refresh water', '912 − 456  =  456g',                         '✓'),
    ('Total water',   '456 + 456  =  912g  (80% of 1,140g)',        '✓'),
    ('Bassinage',     '274 + 91 + 68 + 23  =  456g',                '✓'),
    ('Salt',          '3% × 1,140  =  34g',                         '✓'),
    ('Oil',           '2% × 1,140  =  23g',                         '✓'),
    ('Biga ADY',      '(0.3% × 912) ÷ 2  =  1.4g',                 '✓'),
    ('Refresh ADY',   '(3g/kg × 1.14kg) ÷ 2  =  1.7g',             '✓'),
    ('Total dough',   '1,140 + 912 + 34  =  2,086g ÷ 8  =  260.75g','✓'),
]

t6 = doc.add_table(rows=len(checks), cols=3)
t6.style = 'Table Grid'
for ri, (label, calc, tick) in enumerate(checks):
    shade = 'F2F2F2' if ri % 2 == 0 else 'FFFFFF'
    c0 = t6.cell(ri, 0); c1 = t6.cell(ri, 1); c2 = t6.cell(ri, 2)
    shade_cell(c0, shade); shade_cell(c1, shade); shade_cell(c2, shade)
    r0 = c0.paragraphs[0].add_run(label)
    r1 = c1.paragraphs[0].add_run(calc)
    r2 = c2.paragraphs[0].add_run(tick)
    r0.bold = True
    for run, col in [(r0, BLACK), (r1, GREY), (r2, RGBColor(0x27, 0xAE, 0x60))]:
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = col
t6.columns[0].width = Cm(3.5)
t6.columns[1].width = Cm(10.0)
t6.columns[2].width = Cm(0.8)

# ── Save ─────────────────────────────────────────────────────────────────────
path = '/home/user/Pizza/Dough_Eyed_Style_Recipe.docx'
doc.save(path)
print(f'Saved: {path}')
