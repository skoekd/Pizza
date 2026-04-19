import type { UserInputs, Warning, BlendStats } from '../types';
import { hydrationCeiling, toC } from './calculations';

export function buildWarnings(
  inputs: UserInputs,
  blend: BlendStats,
): Warning[] {
  const warnings: Warning[] = [];
  const roomTempC = toC(inputs.ambientTemp, inputs.tempUnit);
  const fridgeTempC = toC(inputs.fridgeTemp, inputs.tempUnit);

  const push = (
    id: string,
    severity: Warning['severity'],
    title: string,
    message: string,
  ) => warnings.push({ id, severity, title, message });

  // 4A — P/L warnings
  if (blend.pl > 0.65) {
    push(
      'pl_high',
      'warning',
      'P/L too high for canotto',
      `Your flour blend P/L of ${blend.pl.toFixed(2)} exceeds the canotto target of 0.50–0.60. The dough may resist opening and the rim may not inflate. Reduce high-tenacity flours.`,
    );
  }
  if (blend.pl < 0.45) {
    push(
      'pl_low',
      'warning',
      'P/L very low',
      `Blend P/L ${blend.pl.toFixed(2)} is very low. Dough may be too extensible to hold gas structure. Consider adding a stronger flour.`,
    );
  }

  // Casillo Aroma cap check
  const aromaEntry = inputs.flourEntries.find((e) => e.flourId === 'casillo_aroma');
  if (aromaEntry && aromaEntry.percentage > 15) {
    push(
      'aroma_high',
      'warning',
      'Casillo Aroma exceeds 15%',
      `Casillo Aroma has P/L 0.75 and is formulated for thin Roman-style pizza, not canotto. Above 15% it tightens the dough and blocks rim inflation. Recommend maximum 10%. Note: Aroma is also Type 1 flour — higher ash, faster enzymes, narrower fermentation window.`,
    );
  }

  // 4B — W vs timeline
  if (blend.w < 280 && inputs.timeline === 72) {
    push(
      'w_too_weak_72',
      'error',
      'Flour too weak for 72h process',
      `This flour blend (W ${blend.w}) is too weak for a 72h process. Maximum recommended: 24-36h. Use W 330+ for 72h.`,
    );
  }
  if (blend.w < 300 && inputs.timeline === 48) {
    push(
      'w_marginal_48',
      'warning',
      'W marginal for 48h',
      `W ${blend.w} is marginal for a 48h process. Monitor biga pH closely. Reduce biga duration if pH drops below 5.0 before scheduled refresh.`,
    );
  }
  if (blend.w > 340 && inputs.timeline === 24) {
    push(
      'w_strong_24',
      'warning',
      'Very strong flour for 24h process',
      `This flour (W ${blend.w}) is designed for extended fermentation. A 24h process may produce a tight, bready rim. Consider 48h for full maturation and flavor development.`,
    );
  }

  // 4C — FN warnings
  if (blend.fn > 360 && toC(inputs.floorTemp, inputs.tempUnit) < 300) {
    push(
      'fn_high_low_oven',
      'warning',
      'High FN + low oven temperature',
      `High FN ${blend.fn} (low amylase activity) means your crust may bake pale at oven temperatures below 300°C. Consider adding 0.2–0.3% diastatic malt.`,
    );
  }
  if (blend.fn < 250) {
    push(
      'fn_low',
      'warning',
      'Low FN — high enzyme activity',
      `FN ${blend.fn} indicates high amylase activity. With long fermentation this may produce gummy, sticky dough. Reduce fermentation time or use higher FN flour.`,
    );
  }
  if (
    blend.fn > 300 &&
    inputs.maltEnabled &&
    inputs.maltPct > 0.3 &&
    toC(inputs.floorTemp, inputs.tempUnit) > 380
  ) {
    push(
      'malt_unnecessary',
      'note',
      'Malt likely unnecessary',
      `Malt addition is likely unnecessary at these oven temperatures with FN ${blend.fn}. Risk of over-browning. Consider reducing to 0.1% or removing.`,
    );
  }

  // 4D — Stability
  if (blend.stability < 8 && inputs.timeline > 24) {
    push(
      'stability_low',
      'warning',
      'Low farinograph stability',
      `Low stability (${blend.stability} min) suggests limited mixing tolerance and reduced cold retard window. Reduce mixing time and target 24h maximum total fermentation.`,
    );
  }

  // 4E — Hydration
  const maxHyd = hydrationCeiling(blend.w, inputs.bigaPct);
  if (inputs.totalHydration > maxHyd + 3) {
    push(
      'hydration_too_high',
      'warning',
      'Hydration may exceed flour capacity',
      `Your target hydration of ${inputs.totalHydration}% may exceed the structural capacity of this blend (W ${blend.w}). Recommended maximum: ${maxHyd}%.`,
    );
  }
  if (inputs.totalHydration > 76 && inputs.mixerType === 'hand') {
    push(
      'hydration_hand',
      'warning',
      'High hydration difficult by hand',
      `Hydration above 76% is very difficult to mix by hand. Consider a spiral or planetary mixer, or reduce to 72-74%.`,
    );
  }

  // 4F — Water temperature warnings (handled in output via Temperatures object)

  // 4G — Baking
  if (inputs.ovenType === 'home_no_steel') {
    push(
      'no_steel',
      'warning',
      'No baking steel — crunch very difficult',
      `A home oven without a baking steel or stone cannot reliably achieve canotto crunch. Strongly recommend a baking steel (preferred) or cordierite stone. Preheat minimum 60 minutes.`,
    );
  }
  if (toC(inputs.floorTemp, inputs.tempUnit) > 450) {
    push(
      'floor_too_hot',
      'warning',
      'Floor temp > 450°C targets chewy Neapolitan',
      `Floor temperature above 450°C is the STG Neapolitan profile — optimized for soft, chewy texture in 60-75s. For canotto crunch, reduce floor to 400-420°C and extend bake to 90-150s.`,
    );
  }

  // 4H — Fridge
  if (fridgeTempC > 7) {
    push(
      'fridge_warm',
      'warning',
      'Fridge temperature above 7°C',
      `Fridge temperature above 7°C significantly accelerates cold retard fermentation. Monitor dough more frequently. Enzyme activity at 7°C is ~1.5× that at 4°C.`,
    );
  }
  if (fridgeTempC < 2) {
    push(
      'fridge_cold',
      'warning',
      'Fridge below 2°C — risk of yeast cold-stress',
      `Fridge below 2°C risks yeast cold-stress and autolysis over extended retards (48h+). Ideal canotto cold retard: 4°C.`,
    );
  }

  // Summer/hot kitchen note
  if (roomTempC > 28) {
    push(
      'hot_kitchen',
      'note',
      'Hot kitchen detected',
      `Room temperature ${Math.round(roomTempC)}°C — biga water may require ice slurry. Watch final proof carefully. Signs of over-proof appear 20-30% faster than in a standard kitchen.`,
    );
  }
  if (roomTempC < 17) {
    push(
      'cool_kitchen',
      'note',
      'Cool kitchen detected',
      `Room temperature ${Math.round(roomTempC)}°C — dough may need 20-30% more room temperature time. Trust the poke test over the clock.`,
    );
  }

  // ADY reminder
  if (inputs.yeastType === 'ady') {
    push(
      'ady_rehydrate',
      'note',
      'ADY requires rehydration',
      `Active dry yeast must be rehydrated in 38-43°C water for 5-10 minutes before use. Do NOT add directly to dough.`,
    );
  }

  return warnings;
}
