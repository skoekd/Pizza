import type { Flour } from '../types';

export const FLOUR_DATABASE: Flour[] = [
  {
    id: 'caputo_blue',
    name: 'Caputo Blue (Pizzeria 00)',
    w: 270,
    pl: 0.55,
    protein: 12.5,
    fn: 350,
    stability: 9,
    type: '00',
    notes:
      'Ideal refresh flour for canotto. High FN suits long biga cold ferment. Too weak (W270) for biga lasting 18h+ — use as refresh only.',
    canUseInBiga: false,
    canUseInRefresh: true,
  },
  {
    id: 'casillo_aroma',
    name: 'Casillo Aroma',
    w: 280,
    pl: 0.75,
    protein: 13.0,
    fn: 325,
    stability: 10,
    type: '1',
    notes:
      'P/L 0.75 disqualifying for canotto. Formulated for thin Roman scrocchiarella. Max 10-15% as flavor accent only. Type 1 = higher ash, faster enzymes, narrower window.',
    canUseInBiga: false,
    canUseInRefresh: true,
  },
  {
    id: 'casillo_superiore',
    name: 'Casillo Pizza Superiore',
    w: 340,
    pl: 0.55,
    protein: 13.5,
    fn: 300,
    stability: 12,
    type: '00',
    notes:
      'Versatile all-arounder. Works as biga flour or refresh flour. Good for 48h process. Viable as 100% flour at 72% hydration.',
    canUseInBiga: true,
    canUseInRefresh: true,
  },
  {
    id: 'casillo_la8',
    name: 'Casillo La 8 Plus',
    w: 350,
    pl: 0.6,
    protein: 14.5,
    fn: 300,
    stability: 14,
    type: '00',
    notes:
      'Top pick for canotto biga. Marketed for contemporary canotto and high-hydration long cold ferment. W350 survives 18-24h biga plus 48h cold retard.',
    canUseInBiga: true,
    canUseInRefresh: true,
  },
];

export const CUSTOM_FLOUR_TEMPLATE: Flour = {
  id: 'custom',
  name: 'Custom Flour',
  w: 320,
  pl: 0.55,
  protein: 13.0,
  fn: 300,
  stability: 10,
  type: '00',
  notes: '',
  canUseInBiga: true,
  canUseInRefresh: true,
};

export function getFlour(id: string): Flour | undefined {
  return FLOUR_DATABASE.find((f) => f.id === id);
}

export const CANOTTO_FRAMEWORKS = [
  {
    id: 'A',
    name: 'Framework A — Strength in biga, extensibility in refresh (Recommended)',
    description:
      'Biga: 100% Casillo La 8 Plus · Refresh: 100% Caputo Blue. Effective blend W≈310, P/L≈0.57. Best for 48-72h.',
    bigaFlours: [{ id: 'casillo_la8', pct: 100 }],
    refreshFlours: [{ id: 'caputo_blue', pct: 100 }],
  },
  {
    id: 'B',
    name: 'Framework B — Single-mill Casillo',
    description:
      'Biga: 100% La 8 Plus · Refresh: 70% Pizza Superiore + 30% La 8 Plus. Blend W≈345, P/L≈0.59. Best for 72h, high hydration 75-78%.',
    bigaFlours: [{ id: 'casillo_la8', pct: 100 }],
    refreshFlours: [
      { id: 'casillo_superiore', pct: 70 },
      { id: 'casillo_la8', pct: 30 },
    ],
  },
  {
    id: 'C',
    name: 'Framework C — Accessible (no La 8 Plus needed)',
    description:
      'Biga: 100% Casillo Pizza Superiore · Refresh: 100% Caputo Blue. Effective blend W≈305, P/L≈0.55. More forgiving fermentation window. Best for 48h when La 8 Plus is unavailable.',
    bigaFlours: [{ id: 'casillo_superiore', pct: 100 }],
    refreshFlours: [{ id: 'caputo_blue', pct: 100 }],
  },
  {
    id: 'D',
    name: 'Framework D — 100% Biga',
    description:
      'All flour in biga as La 8 Plus at 44-48% hydration. Refresh = water + salt only. Maximum flavor complexity, tightest margin. For experienced bakers, 48-72h.',
    bigaFlours: [{ id: 'casillo_la8', pct: 100 }],
    refreshFlours: [],
  },
];
