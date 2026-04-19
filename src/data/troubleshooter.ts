export interface TroubleshootEntry {
  id: string;
  symptom: string;
  causes: string[];
  fixes: string[];
  section: string;
}

export const TROUBLESHOOT_DATA: TroubleshootEntry[] = [
  {
    id: 'collapsed',
    symptom: 'Dough collapsed or flat',
    causes: ['Overproofed', 'Fermented too warm', 'Too much yeast'],
    fixes: [
      'Reduce fermentation time by 15-20%',
      'Lower ambient temperature or move to cooler spot',
      'Cut yeast dose 20-30% in next batch',
      'Use poke test — if dent stays, bake immediately',
    ],
    section: 'Over-proofing',
  },
  {
    id: 'no_rise',
    symptom: "Dough doesn't rise",
    causes: ['Underproofed', 'Too cold', 'Old or dead yeast'],
    fixes: [
      'Extend proof time — trust poke test over clock',
      'Check ambient temperature — target 20-22°C for room proof',
      'Test yeast vitality: dissolve in 38°C water with a pinch of sugar, should foam in 5-10 min',
      'If using IDY, check expiry date and storage (airtight, cool, dark)',
    ],
    section: 'Under-proofing',
  },
  {
    id: 'tears_stretching',
    symptom: 'Dough tears when stretching',
    causes: [
      'Weak gluten (low W flour)',
      'Too much protease activity',
      'Over-fermented biga',
    ],
    fixes: [
      'Check biga pH — if below 4.8, biga is over-mature and dough will be weak',
      'Shorten total fermentation time',
      'Use higher W flour (W340+) in biga',
      'Increase salt percentage to 2.8-3.0% to inhibit protease',
      'Let balls warm longer before opening — cold dough tears',
    ],
    section: 'Gluten weakness',
  },
  {
    id: 'tight_rubbery',
    symptom: 'Dough is too tight or rubbery',
    causes: ['Underfermented', 'Too cold (especially balls)', 'Not sufficiently relaxed after balling'],
    fixes: [
      'Let balls sit at room temperature 30-60 min longer before opening',
      'Extend bulk fermentation (puntata) by 15-20 min',
      'Ensure balls are at room temperature before opening — cold balls are always tight',
      'Check poke test — if it snaps back immediately, it needs more time',
    ],
    section: 'Tight dough',
  },
  {
    id: 'sour_smell',
    symptom: 'Dough smells sour or off (acetone, sharp vinegar)',
    causes: [
      'Overfermentation',
      'Enzyme overload (low FN flour)',
      'LAB (lactic acid bacteria) contamination',
    ],
    fixes: [
      'Biga pH below 4.8 is irreversible — use as is but expect weaker structure',
      'Shorten fermentation by 20-30% in next batch',
      'Reduce biga yeast dose',
      'Lower fridge temperature to 4°C',
      'Check flour FN — if below 250, switch to higher FN flour for long processes',
      'Ensure all equipment is thoroughly cleaned before use',
    ],
    section: 'Over-fermentation',
  },
  {
    id: 'pale_crust',
    symptom: 'Crust is pale after baking',
    causes: [
      'Insufficient residual sugars (over-fermented or underfermented)',
      'Oven not hot enough or preheated long enough',
      'High FN flour with too-cold oven',
    ],
    fixes: [
      'Ensure stone/steel preheated minimum 60 min at max temp',
      'Check floor temperature with IR thermometer — target 400-420°C for pizza oven',
      'Add 0.2% diastatic malt if baking below 350°C and flour FN is above 340',
      'Extend cold retard to build residual sugars — 48h retard produces better Maillard color than 24h',
      'Use broiler/grill element for top heat in home oven',
    ],
    section: 'Browning / color',
  },
  {
    id: 'no_inflate',
    symptom: 'Rim did not inflate — no canotto effect',
    causes: [
      'Dough over-mixed (too elastic, cannot inflate)',
      'Blend P/L too high (above 0.65)',
      'Rim pressed during opening',
      'Dough over-proofed (gas cage failed)',
    ],
    fixes: [
      'Check blend P/L — if above 0.65, reduce or remove Casillo Aroma',
      'Stop mixing earlier — improved mix, NOT full windowpane',
      'Never touch the outer 2-2.5cm rim during opening',
      'Roll gas toward rim during opening with fingertips on center disc',
      'Open smaller disc (27-28cm for 270g ball) — concentrates gas in rim',
      'Check proof — dough must show slow poke-test rebound, not immediate snap-back',
    ],
    section: 'Canotto inflation',
  },
  {
    id: 'chewy_not_crunchy',
    symptom: 'Rim is chewy not crunchy',
    causes: [
      'Floor temperature too high (above 450°C) causing too-fast bake',
      'Total bake time too short (under 90 seconds)',
      'Rim interior never reached 95-98°C',
    ],
    fixes: [
      'Reduce floor to 400-420°C — lower floor + longer bake = crunch',
      'Extend bake to 90-150 seconds with 2-4 rotations',
      'Check rim with probe thermometer — target 95-98°C internal',
      'Allow 3-5 min stone recovery between pies',
      'Ensure dome at 450-480°C for top heat to dehydrate rim walls',
    ],
    section: 'Crunch / texture',
  },
  {
    id: 'soggy_base',
    symptom: 'Base is soggy or gummy (gum line)',
    causes: [
      'Floor temperature too low or stone not saturated',
      'Under-baked base',
      'Excess sauce/toppings moisture',
    ],
    fixes: [
      'Preheat stone/steel minimum 60 minutes at maximum temperature',
      'Check floor temp with IR thermometer — target 400°C minimum',
      'Extend bake time by 15-20 seconds',
      'Use less sauce — spread thinly',
      'Drain wet toppings (buffalo mozzarella, vegetables) before use',
      'Reduce hydration 2-3% if persistently soggy',
    ],
    section: 'Base / gum line',
  },
  {
    id: 'no_leopard',
    symptom: 'No leopard spots on crust',
    causes: [
      'Dome too cool relative to floor',
      'Surface too wet during bake',
      'Dough over-proofed (no residual sugars)',
    ],
    fixes: [
      'Increase dome temperature to 460-480°C',
      'Ensure dough balls not condensation-wet from fridge — let acclimatize 30-60 min',
      'Check cold retard time — longer retard (48h) builds more residual sugars for Maillard',
      'Avoid over-proofing which depletes all fermentable sugars',
    ],
    section: 'Leopard spots / Maillard',
  },
  {
    id: 'biga_wont_break',
    symptom: 'Biga is hard and compact, not web-like',
    causes: ['Under-matured biga', 'Too cold during fermentation', 'Too little yeast'],
    fixes: [
      'Check biga pH — target 5.0-5.3. If above 5.5, biga needs more time',
      'Give biga 1-2 extra hours at room temperature before refreshing',
      'Soak biga chunks in salt-water for 2-5 min before mixing — softens without over-working',
      'Increase yeast dose by 0.1-0.2% on biga flour in next batch',
    ],
    section: 'Biga ripeness',
  },
  {
    id: 'biga_over_mature',
    symptom: 'Biga smells like acetone / nail polish, grey or slimy',
    causes: ['Over-mature biga', 'Fridge too warm (above 7°C)', 'Too much yeast'],
    fixes: [
      'pH below 4.8 is irreversible — protease damage has occurred',
      'Discard and start fresh if possible',
      'If proceeding: expect weaker dough, less oven spring, shorter final proof window',
      'Check fridge temperature — target 4°C, not 6-7°C',
      'Reduce yeast dose 20-30% in next batch',
    ],
    section: 'Biga over-maturation',
  },
];
