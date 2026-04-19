import type {
  UserInputs,
  BlendStats,
  Weights,
  Temperatures,
  FlourEntry,
  MixerType,
} from '../types';
import { FLOUR_DATABASE } from '../data/flours';

// ─── Unit conversion ─────────────────────────────────────────────────────────

export function toC(val: number, unit: 'C' | 'F'): number {
  return unit === 'F' ? (val - 32) * (5 / 9) : val;
}

export function fromC(val: number, unit: 'C' | 'F'): number {
  return unit === 'F' ? val * (9 / 5) + 32 : val;
}

export function round1(n: number): number {
  return Math.round(n * 10) / 10;
}

export function round0(n: number): number {
  return Math.round(n);
}

// ─── Flour blend stats (Section 3I) ─────────────────────────────────────────

export function calcBlendStats(entries: FlourEntry[]): BlendStats {
  let w = 0, pl = 0, fn = 0, stab = 0, stabWeight = 0;
  for (const e of entries) {
    const flour = e.customFlour ?? FLOUR_DATABASE.find((f) => f.id === e.flourId);
    if (!flour || e.percentage <= 0) continue;
    const pct = e.percentage / 100;
    w += flour.w * pct;
    pl += flour.pl * pct;
    fn += flour.fn * pct;
    stab += flour.stability * pct;
    stabWeight += pct;
  }
  if (stabWeight > 0) stab = stab / stabWeight;

  const maxHydrationDirect = (w / 1000) * 100 + 20;

  return {
    w: round1(w),
    pl: round1(pl * 100) / 100,
    fn: round0(fn),
    stability: round1(stab),
    maxHydration: round1(maxHydrationDirect),
  };
}

// Section 3J — hydration ceiling
export function hydrationCeiling(blendW: number, bigaPct: number): number {
  const base = (blendW / 1000) * 100 + 20;
  if (bigaPct >= 100) return round1(base + 12);
  if (bigaPct >= 50) return round1(base + 7);
  return round1(base);
}

// ─── Core weight math (Sections 3A–3E) ───────────────────────────────────────

export function calcWeights(inputs: UserInputs): Weights {
  const {
    numPizzas,
    ballWeight,
    bigaPct,
    bigaHydration,
    totalHydration,
    saltPct,
    oilEnabled,
    oilPct,
    maltEnabled,
    maltPct,
    yeastType,
  } = inputs;

  const totalDough = numPizzas * ballWeight;

  // 3A
  const hydDec = totalHydration / 100;
  const saltDec = saltPct / 100;
  const oilDec = oilEnabled ? oilPct / 100 : 0;
  const maltDec = maltEnabled ? maltPct / 100 : 0;
  const totalFlour = totalDough / (1 + hydDec + saltDec + oilDec + maltDec);

  // 3B
  const bigaFlour = totalFlour * (bigaPct / 100);
  const refreshFlour = totalFlour - bigaFlour;

  // 3C
  const bigaWater = bigaFlour * (bigaHydration / 100);
  const totalWater = totalFlour * hydDec;
  const refreshWater = totalWater - bigaWater;
  const bassinage =
    totalHydration > 72 ? refreshWater * 0.08 : 0;
  const mainRefreshWater = refreshWater - bassinage;

  // 3D
  const salt = totalFlour * saltDec;
  const oil = oilEnabled ? totalFlour * oilDec : 0;
  const malt = maltEnabled ? totalFlour * maltDec : 0;

  // 3F/3G — yeast
  const bigaYeastFreshPct = calcBigaYeastPct(inputs.ambientTemp);
  const bigaYeastFresh = bigaFlour * (bigaYeastFreshPct / 100);
  const bigaYeast = convertYeast(bigaYeastFresh, yeastType);

  const refreshYeastFreshPct = Math.max(
    0,
    0.2 - (bigaPct / 100) * 0.15,
  );
  const refreshYeastFresh = totalFlour * refreshYeastFreshPct;
  const refreshYeast = convertYeast(refreshYeastFresh, yeastType);

  const r = (v: number) => round1(v);

  return {
    totalDough: r(totalDough),
    totalFlour: r(totalFlour),
    bigaFlour: r(bigaFlour),
    refreshFlour: r(refreshFlour),
    totalWater: r(totalWater),
    bigaWater: r(bigaWater),
    refreshWater: r(refreshWater),
    bassinage: r(bassinage),
    mainRefreshWater: r(mainRefreshWater),
    salt: r(salt),
    oil: r(oil),
    malt: r(malt),
    bigaYeast: r(bigaYeast),
    refreshYeast: r(refreshYeast),
  };
}

// ─── Biga yeast % by temperature (Section 3F) ────────────────────────────────

export function calcBigaYeastPct(ambientTempC: number): number {
  const raw = 1.0 - (ambientTempC - 18) * 0.05;
  return round1(Math.min(1.5, Math.max(0.3, raw)));
}

// ─── Yeast type conversion (Section 3E) ──────────────────────────────────────

export function convertYeast(freshGrams: number, type: 'fresh' | 'idy' | 'ady'): number {
  if (type === 'idy') return freshGrams / 3;
  if (type === 'ady') return freshGrams / 2.5;
  return freshGrams;
}

export const YEAST_LABELS: Record<string, string> = {
  fresh: 'Fresh yeast',
  idy: 'Instant dry yeast (IDY)',
  ady: 'Active dry yeast (ADY)',
};

// ─── Friction factors (Section 3H) ───────────────────────────────────────────

export function frictionFactor(mixer: MixerType): number {
  const map: Record<MixerType, number> = {
    hand: 3,
    fork: 4,
    spiral: 10,
    planetary: 6,
    planetary_long: 10,
  };
  return map[mixer];
}

// ─── DDT — water temperatures (Section 3H) ───────────────────────────────────

export function calcTemperatures(inputs: UserInputs, _weights: Weights): Temperatures {
  const {
    flourTemp: flourTempInput,
    ambientTemp: ambientTempInput,
    fridgeTemp: fridgeTempInput,
    tempUnit,
    mixerType,
    bigaPct,
  } = inputs;

  const flourTemp = toC(flourTempInput, tempUnit);
  const roomTemp = toC(ambientTempInput, tempUnit);
  const fridgeTemp = toC(fridgeTempInput, tempUnit);
  const ff = frictionFactor(mixerType);

  // Biga water temp: M=3, target exit 23°C (contemporary canotto per Gigi protocol)
  let bigaWaterTemp = 69 - flourTemp - roomTemp - ff;
  bigaWaterTemp = round1(bigaWaterTemp);
  const useIceForBiga = bigaWaterTemp < 4;
  const bigaIceFraction = useIceForBiga
    ? round1(Math.max(0, (4 - bigaWaterTemp) / 4))
    : 0;
  bigaWaterTemp = Math.max(0, bigaWaterTemp);

  // Final dough water temp: M=3, target FDT 24°C + cold biga offset
  const bigaDec = bigaPct / 100;
  let finalWaterTemp =
    72 - flourTemp - roomTemp - ff + (roomTemp - fridgeTemp) * bigaDec;
  finalWaterTemp = round1(finalWaterTemp);

  // Clamp to safe range
  const bigaWaterClamped = Math.min(43, Math.max(0, bigaWaterTemp));
  const finalWaterClamped = Math.min(43, Math.max(0, finalWaterTemp));

  const bigaYeastPct = calcBigaYeastPct(roomTemp);
  const refreshYeastPct = round1(Math.max(0, 0.2 - bigaDec * 0.15));

  return {
    bigaWater: bigaWaterClamped,
    finalDoughWater: finalWaterClamped,
    frictionFactor: ff,
    targetBigaExit: 23,
    targetFDT: 24,
    bigaYeastPct,
    refreshYeastPct,
    useIceForBiga,
    bigaIceFraction,
  };
}

// ─── Room temp modifier (Section 3M) ─────────────────────────────────────────

export function roomTempModifier(roomTempC: number): number {
  const raw = 1 - (roomTempC - 21) * 0.075;
  return Math.min(1.8, Math.max(0.4, raw));
}

export function adjustedTime(baseMin: number, modifier: number): number {
  return Math.round((baseMin * modifier) / 15) * 15;
}

// ─── Ball → disc size (Section 8B) ───────────────────────────────────────────

export function ballToDisc(ballWeightG: number): string {
  const map: Array<[number, string]> = [
    [240, '26-28 cm'],
    [260, '27-29 cm'],
    [270, '28-30 cm'],
    [280, '29-31 cm'],
    [300, '30-33 cm'],
  ];
  let closest = map[0];
  let minDiff = Infinity;
  for (const entry of map) {
    const diff = Math.abs(entry[0] - ballWeightG);
    if (diff < minDiff) { minDiff = diff; closest = entry; }
  }
  return closest[1];
}

// ─── Framework detector ───────────────────────────────────────────────────────

export function detectFramework(entries: FlourEntry[], bigaPct: number): string {
  const ids = entries.map((e) => e.flourId).sort().join(',');
  if (bigaPct === 100) return 'D';
  if (ids.includes('casillo_la8') && ids.includes('caputo_blue') && !ids.includes('casillo_aroma')) return 'A';
  if (ids.includes('casillo_la8') && ids.includes('casillo_superiore') && !ids.includes('caputo_blue')) return 'B';
  if (ids.includes('casillo_la8') && ids.includes('caputo_blue') && ids.includes('casillo_aroma')) return 'C';
  return '—';
}
