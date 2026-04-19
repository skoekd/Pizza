import type { UserInputs, ScheduleStage } from '../types';
import { toC, roomTempModifier, adjustedTime } from './calculations';

interface PuntataMinutes {
  base: number;
  min: number;
  max: number;
}

function puntataBase(pref: string): PuntataMinutes {
  if (pref === 'short') return { base: 52, min: 45, max: 60 };
  if (pref === 'long') return { base: 105, min: 90, max: 120 };
  return { base: 75, min: 60, max: 90 };
}

function aprettoBase(pref: string): { base: number; label: string } {
  if (pref === 'short') return { base: 105, label: '1.5–2h' };
  if (pref === 'long') return { base: 210, label: '3–4h' };
  return { base: 150, label: '2–3h' };
}

function fmt(minutes: number): string {
  if (minutes < 60) return `${minutes} min`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m === 0 ? `${h}h` : `${h}h ${m}min`;
}

export function buildSchedule(inputs: UserInputs): ScheduleStage[] {
  const roomC = toC(inputs.ambientTemp, inputs.tempUnit);
  const fridgeC = toC(inputs.fridgeTemp, inputs.tempUnit);
  const modifier = roomTempModifier(roomC);
  const timeline = inputs.timeline;

  const { base: puntataBase_ } = puntataBase(inputs.puntata);
  const adjPuntata = adjustedTime(puntataBase_, modifier);
  const { base: aprettoBase_ } = aprettoBase(inputs.appretto);
  const adjAppretto = adjustedTime(aprettoBase_, modifier);

  const stages: ScheduleStage[] = [];

  if (timeline === 24) {
    stages.push({
      label: '1. Mix Biga',
      offset: '−24h',
      action: `Mix biga (${inputs.bigaPct}% of flour at ${inputs.bigaHydration}% hydration). Lumpy shaggy texture — NOT smooth. Cover loosely for gas exchange.`,
      temp: `Room temp ${Math.round(roomC)}°C`,
      duration: '2-3 min mix',
      lookFor: 'All flour hydrated. Shaggy, pebbly, grape-sized clumps. No smooth ball.',
    });
    stages.push({
      label: '2. Biga Room Rest',
      offset: '−24h to −22h',
      action: 'Let biga rest at room temperature before refrigerating.',
      temp: `${Math.round(roomC)}°C`,
      duration: '1-2h',
      lookFor: 'Beginning of fermentation activity. Slight puff.',
    });
    stages.push({
      label: '3. Biga Cold Retard',
      offset: '−22h to −2h',
      action: `Transfer biga to refrigerator. Cover loosely — NOT airtight.`,
      temp: `${Math.round(fridgeC)}°C`,
      duration: '20h',
      lookFor:
        'Ripe at pH 5.0–5.3. Volume 1.5–2× original. Web-like gluten strands when pulled. Alcoholic-sweet smell.',
    });
    stages.push({
      label: '4. Remove Biga',
      offset: '−2h',
      action:
        'Remove biga from refrigerator. Check ripeness: pull a piece — gluten should web and extend. Smell: alcoholic, faint vinegar, not acetone.',
      temp: `${Math.round(roomC)}°C`,
      duration: '15–20 min temper',
      lookFor: 'pH 5.0–5.3. Webby gluten strands. No grey, no acetone smell.',
    });
    stages.push({
      label: '5. Mix Final Dough (Refresh)',
      offset: '−1.5h',
      action:
        'Dissolve salt in main refresh water. Add biga chunks (golf-ball to gnocchi sized). Soak 2-5 min. Add refresh flour gradually. Mix to improved mix (dough pulls from wall, translucent-thick windowpane). Add bassinage reserve in thin stream if hydration >72%. Add oil last if used.',
      temp: `Water at calculated temp`,
      duration: '7-12 min spiral / 10-15 min planetary',
      lookFor: 'Dough pulls cleanly from walls. Windowpane: translucent-thick, tears with slight puncture — NOT paper-thin. FDT 23-25°C.',
    });
    stages.push({
      label: '6. Puntata (Bulk Fermentation)',
      offset: '−1.5h',
      action: `Rest dough covered at room temperature. Perform coil folds as needed by hydration.`,
      temp: `${Math.round(roomC)}°C`,
      duration: fmt(adjPuntata),
      lookFor: `Slight puff, dough holds shape. Coil folds: ${inputs.totalHydration <= 72 ? '0–1 folds' : inputs.totalHydration <= 76 ? '1–2 folds at 20-30 min intervals' : '2–3 folds at 20-30 min intervals'}.`,
    });
    stages.push({
      label: '7. Ball',
      offset: `−${fmt(adjAppretto)}`,
      action:
        'Divide by weight. Gentle tuck-and-seal — NOT drum-tight. Ball should dome slightly and feel silky.',
      temp: `${Math.round(roomC)}°C`,
      duration: '5-10 min',
      lookFor: `${inputs.ballWeight}g per ball. Smooth domed surface. Silky but not tight.`,
    });
    stages.push({
      label: '8. Appretto (Final Proof)',
      offset: `−${fmt(adjAppretto)} to 0`,
      action:
        'Balls proof at room temperature in individual sealed containers. Do NOT stack. Watch for poke test.',
      temp: `${Math.round(roomC)}°C`,
      duration: `${fmt(adjAppretto)} (adjusted for ${Math.round(roomC)}°C)`,
      lookFor: 'Poke test: press 1cm — slow rebound over 3-5s = READY. Immediate snap-back = needs more time. Stays dented = over-proofed, bake immediately.',
    });
    stages.push({
      label: '9. Open and Bake',
      offset: '0',
      action:
        'Schiaffo (slap) or fingertip press from center outward. Keep 2–2.5cm rim untouched. Open to target disc size. Load to oven.',
      temp: `Floor ${inputs.floorTemp}°${inputs.tempUnit}, Dome ${inputs.domeTemp}°${inputs.tempUnit}`,
      duration: '90–150 seconds',
      lookFor: 'Rim inflates rapidly in first 40s. Leopard spots on rim. Hollow tap sound when done.',
    });
  }

  if (timeline === 48) {
    stages.push({
      label: '1. Mix Biga',
      offset: '−48h',
      action: `Mix biga (${inputs.bigaPct}% of flour at ${inputs.bigaHydration}% hydration). Lumpy shaggy texture — NOT smooth. Cover loosely.`,
      temp: `${Math.round(roomC)}°C`,
      duration: '2-3 min mix',
      lookFor: 'All flour hydrated. Shaggy, pebbly clumps. No gluten development.',
    });
    stages.push({
      label: '2. Biga Room Rest',
      offset: '−48h to −46h',
      action: 'Biga rests at room temperature before refrigerating.',
      temp: `${Math.round(roomC)}°C`,
      duration: '2h',
      lookFor: 'Slight puff, early fermentation signs.',
    });
    stages.push({
      label: '3. Biga Cold Retard',
      offset: '−46h to −26h',
      action: 'Biga cold retards in refrigerator. Cover loosely.',
      temp: `${Math.round(fridgeC)}°C`,
      duration: '20h',
      lookFor: 'pH 5.0–5.3. Volume 1.5–2×. Web-like strands.',
    });
    stages.push({
      label: '4. Confirm Biga Ripeness + Mix Refresh',
      offset: '−26h',
      action:
        'Remove biga. Verify ripeness. Mix final dough — salt water, biga chunks, refresh flour. Improved mix only.',
      temp: `${Math.round(roomC)}°C`,
      duration: '10-15 min mix',
      lookFor: 'pH 5.0–5.3. FDT 23-25°C. Dough pulls from bowl walls.',
    });
    stages.push({
      label: '5. Puntata',
      offset: '−25h',
      action: 'Bulk rest at room temperature with coil folds as needed.',
      temp: `${Math.round(roomC)}°C`,
      duration: fmt(adjPuntata),
      lookFor: 'Slight volume increase, dough holds shape.',
    });
    stages.push({
      label: '6. Ball + Cold Retard (Balls)',
      offset: '−24h',
      action:
        `Divide, ball gently, place in sealed individual containers. Cold retard at ${Math.round(fridgeC)}°C.`,
      temp: `${Math.round(fridgeC)}°C`,
      duration: '22h',
      lookFor: 'Balls slowly develop during cold retard — residual sugar accumulation.',
    });
    stages.push({
      label: '7. Remove Balls',
      offset: '−2h',
      action: 'Remove balls from refrigerator. Allow to acclimatize at room temperature.',
      temp: `${Math.round(roomC)}°C`,
      duration: `${fmt(adjAppretto)} (adjusted for ${Math.round(roomC)}°C)`,
      lookFor: 'Poke test: slow 3-5s rebound = ready. Surface smooth, slight jiggle on tray.',
    });
    stages.push({
      label: '8. Open and Bake',
      offset: '0',
      action: 'Open with schiaffo or fingertip technique. 2-2.5cm rim untouched always.',
      temp: `Floor ${inputs.floorTemp}°${inputs.tempUnit}, Dome ${inputs.domeTemp}°${inputs.tempUnit}`,
      duration: '90–150 seconds',
      lookFor: 'Rim inflates in first 40s. Hollow tap. Leopard spots.',
    });
  }

  if (timeline === 72) {
    stages.push({
      label: '1. Mix Biga',
      offset: '−72h',
      action: `Mix biga (${inputs.bigaPct}% of flour at ${inputs.bigaHydration}% hydration). Shaggy texture only.`,
      temp: `${Math.round(roomC)}°C`,
      duration: '2-3 min mix',
      lookFor: 'All flour hydrated. Shaggy and lumpy. No gluten development.',
    });
    stages.push({
      label: '2. Biga Room Rest',
      offset: '−72h to −70h',
      action: 'Biga rests at room temperature.',
      temp: `${Math.round(roomC)}°C`,
      duration: '2h',
      lookFor: 'Early fermentation activity.',
    });
    stages.push({
      label: '3. Biga Cold Retard',
      offset: '−70h to −50h',
      action: 'Biga cold retards. Cover loosely.',
      temp: `${Math.round(fridgeC)}°C`,
      duration: '20h',
      lookFor: 'pH 5.0–5.3 at end. Volume 1.5–2×.',
    });
    stages.push({
      label: '4. Refresh + Puntata',
      offset: '−50h',
      action:
        'Confirm biga ripeness. Mix final dough. Puntata at room temperature.',
      temp: `${Math.round(roomC)}°C`,
      duration: `Mix 10-15 min + Puntata ${fmt(adjPuntata)}`,
      lookFor: 'FDT 23-25°C. Dough pulls from walls.',
    });
    stages.push({
      label: '5. Ball + Cold Retard (48h)',
      offset: '−49h',
      action: `Divide, ball, seal individually. Cold retard at ${Math.round(fridgeC)}°C for 48h.`,
      temp: `${Math.round(fridgeC)}°C`,
      duration: '48h',
      lookFor: 'Maximum residual sugar accumulation. Flavor depth at 72h.',
    });
    stages.push({
      label: '6. Remove Balls',
      offset: '−2h',
      action: 'Remove from refrigerator. Final room temperature appretto.',
      temp: `${Math.round(roomC)}°C`,
      duration: `${fmt(adjAppretto)}`,
      lookFor: 'Poke test: slow 3-5s rebound. Slight jiggle. Ready to open.',
    });
    stages.push({
      label: '7. Open and Bake',
      offset: '0',
      action: 'Open carefully. 2-2.5cm rim always untouched.',
      temp: `Floor ${inputs.floorTemp}°${inputs.tempUnit}, Dome ${inputs.domeTemp}°${inputs.tempUnit}`,
      duration: '90–150 seconds',
      lookFor: 'Dramatic oven spring in 72h dough. Maximum leopard spots.',
    });
  }

  return stages;
}
