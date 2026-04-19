import React from 'react';
import type { RecipeResult } from '../../types';
import { FLOUR_DATABASE } from '../../data/flours';
import { YEAST_LABELS, toC, fromC } from '../../lib/calculations';

interface Props {
  result: RecipeResult;
}

function Row({ label, value, highlight }: { label: string; value: string; highlight?: boolean }) {
  return (
    <div className="result-row">
      <span className="result-label">{label}</span>
      <span className={highlight ? 'result-value-highlight' : 'result-value'}>{value}</span>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="card mb-3">
      <div className="section-title mb-3">{title}</div>
      {children}
    </div>
  );
}

export function RecipeOutput({ result }: Props) {
  const { inputs, blend, weights, temps, warnings, schedule } = result;
  const unit = inputs.tempUnit;

  const fmtTemp = (c: number) => `${fromC(c, unit).toFixed(0)}°${unit}`;
  const fmtG = (g: number) => `${g.toFixed(1)}g`;

  const yeastLabel = YEAST_LABELS[inputs.yeastType];

  const errors = warnings.filter(w => w.severity === 'error');
  const warningItems = warnings.filter(w => w.severity === 'warning');
  const notes = warnings.filter(w => w.severity === 'note');

  const waterTempNote = temps.finalDoughWater > 30
    ? `High water temp is expected when using cold biga — the cold biga acts as a refrigerant in the DDT calculation. This is correct.`
    : null;

  const floorC = toC(inputs.floorTemp, unit);

  return (
    <div>
      {/* Header */}
      <div className="card mb-3 border-amber-600/30">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div>
            <h2 className="text-xl font-bold text-amber-300">Canotto Pizza Dough</h2>
            <p className="text-stone-400 text-sm mt-0.5">
              {inputs.bigaPct}% Biga · {inputs.timeline}h process
              {result.framework !== '—' ? ` · Framework ${result.framework}` : ''}
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold font-mono text-stone-100">
              {inputs.numPizzas} pizzas
            </div>
            <div className="text-stone-400 text-sm">× {inputs.ballWeight}g = {weights.totalDough.toFixed(0)}g total</div>
          </div>
        </div>
      </div>

      {/* Warnings */}
      {warnings.length > 0 && (
        <div className="mb-3 space-y-2">
          {errors.map(w => (
            <div key={w.id} className="error-box">
              <span className="font-bold">ERROR: {w.title}</span> — {w.message}
            </div>
          ))}
          {warningItems.map(w => (
            <div key={w.id} className="warning-box">
              <span className="font-bold">⚠ {w.title}</span> — {w.message}
            </div>
          ))}
          {notes.map(w => (
            <div key={w.id} className="note-box">
              <span className="font-bold">ℹ {w.title}</span> — {w.message}
            </div>
          ))}
        </div>
      )}

      {/* Flour Blend Assessment */}
      <Section title="Flour Blend Assessment">
        <div className="space-y-0">
          {inputs.flourEntries.map((e, i) => {
            const fl = e.customFlour ?? FLOUR_DATABASE.find(f => f.id === e.flourId);
            return (
              <Row key={i} label={fl?.name ?? e.flourId}
                value={`${fmtG(weights.totalFlour * e.percentage / 100)} (${e.percentage}%)`} />
            );
          })}
        </div>
        <div className="mt-3 space-y-0">
          <Row label="Blend W (strength)"
            value={`${blend.w} — ${blend.w >= 330 ? 'Very Strong' : blend.w >= 290 ? 'Strong' : 'Marginal'}`} />
          <Row label="Blend P/L (tenacity/extensibility)"
            value={blend.pl.toFixed(2)}
            highlight={blend.pl <= 0.65} />
          <Row label="P/L Assessment"
            value={blend.pl <= 0.60 ? '✓ Canotto range (0.50–0.60)' : blend.pl <= 0.65 ? '~ Acceptable, monitor' : '✗ Above canotto target'} />
          <Row label="Blend FN (enzyme activity)"
            value={`${blend.fn} — ${blend.fn >= 300 ? 'Good for long biga' : blend.fn >= 250 ? 'Acceptable' : 'High amylase — monitor'}`} />
          <Row label="Blend Stability"
            value={`${blend.stability} min — ${blend.stability >= 10 ? 'Good' : blend.stability >= 8 ? 'Acceptable' : 'Low — reduce mix time'}`} />
          <Row label={`Max hydration (${inputs.bigaPct}% biga)`}
            value={`${blend.maxHydration + (inputs.bigaPct >= 100 ? 12 : inputs.bigaPct >= 50 ? 7 : 0)}% — currently at ${inputs.totalHydration}%`} />
          <Row label="Disc diameter (ball size)"
            value={`${result.discDiameter} (for ${inputs.ballWeight}g ball)`} />
        </div>
      </Section>

      {/* BIGA */}
      <Section title={`Biga (${inputs.bigaPct}% of flour)`}>
        <div className="space-y-0">
          <Row label="Biga flour" value={fmtG(weights.bigaFlour)} highlight />
          <Row label="Biga water" value={`${fmtG(weights.bigaWater)} at ${fmtTemp(temps.bigaWater)}`} highlight />
          {temps.useIceForBiga && (
            <div className="warning-box my-2">
              Ice required for biga water: use ~{Math.round(temps.bigaIceFraction * 100)}% of water weight as ice.
            </div>
          )}
          <Row label={`Biga yeast (${yeastLabel})`} value={`${fmtG(weights.bigaYeast)} (${temps.bigaYeastPct}% fresh equiv. on biga flour)`} />
          <Row label="Biga salt" value="0g — NEVER add salt to biga" />
          <Row label="Biga hydration" value={`${inputs.bigaHydration}%`} />
          <Row label="Target exit temperature" value={fmtTemp(19)} />
        </div>
        <div className="mt-3 note-box">
          <strong>Mix:</strong> 2-3 min low speed only. End state: shaggy and lumpy, like coarse couscous — NOT smooth. Cover with perforated cling film. Never airtight.
        </div>
        <div className="mt-3">
          <div className="text-xs font-bold text-stone-400 uppercase tracking-wider mb-2">Biga Ripeness Checklist</div>
          <div className="space-y-0.5">
            {[
              'Volume: 1.5–2× original. Puffed chunks with visible webby strands — NOT a smooth dome',
              'Smell: alcoholic (ethanol), lightly acetic, yogurt-adjacent, sweet wheat — NOT acetone or sharp vinegar',
              'Feel: pull a piece — gluten strands extend and web. NOT brittle short tears or slimy',
              'pH: 5.0–5.3 (tight canotto target: 5.1–5.2). Use probe pH meter — strips are inadequate',
              'Visual: spider-web-like strands visible when pulling. Sticky but not wet. Small gas bubbles throughout',
            ].map((item, i) => (
              <div key={i} className="checklist-item">
                <span className="text-amber-500 mt-0.5">◆</span>
                <span>{item}</span>
              </div>
            ))}
          </div>
          <div className="mt-2 error-box text-xs">
            <strong>Over-mature (irreversible):</strong> grey/slimy surface, acetone smell, brittle strands, pH below 4.8. Do not use.
          </div>
        </div>
      </Section>

      {/* Refresh */}
      <Section title="Refresh (Final Dough)">
        <div className="space-y-0">
          {inputs.bigaPct < 100 && (
            <Row label="Refresh flour" value={fmtG(weights.refreshFlour)} highlight />
          )}
          {inputs.bigaPct >= 100 && (
            <Row label="Refresh flour" value="0g — 100% biga, no additional flour" />
          )}
          <Row label="Refresh water (main)" value={`${fmtG(weights.mainRefreshWater)} at ${fmtTemp(temps.finalDoughWater)}`} highlight />
          {weights.bassinage > 0 && (
            <Row label="Bassinage reserve" value={`${fmtG(weights.bassinage)} — add in thin stream at end of mix`} />
          )}
          <Row label="Salt" value={`${fmtG(weights.salt)} dissolved in refresh water before mixing`} />
          {weights.refreshYeast > 0 ? (
            <Row label={`Additional yeast (${yeastLabel})`} value={fmtG(weights.refreshYeast)} />
          ) : (
            <Row label="Additional yeast" value="0g — biga yeast population sufficient" />
          )}
          {inputs.oilEnabled && weights.oil > 0 && (
            <Row label="Oil" value={`${fmtG(weights.oil)} — add last, after bassinage`} />
          )}
          {inputs.maltEnabled && weights.malt > 0 && (
            <Row label="Diastatic malt" value={`${fmtG(weights.malt)} — add with refresh flour`} />
          )}
          <Row label="Total hydration" value={`${inputs.totalHydration}%`} />
        </div>
        {weights.bassinage > 0 && (
          <div className="mt-2 note-box text-xs">
            Bassinage required at {inputs.totalHydration}% hydration. Reserve {fmtG(weights.bassinage)} and add in a thin stream in the final 60-90 seconds of mixing.
          </div>
        )}
        {inputs.yeastType === 'ady' && (
          <div className="mt-2 warning-box text-xs">
            ADY: rehydrate in 38-43°C water for 5-10 min before use. Do not add directly.
          </div>
        )}
      </Section>

      {/* DDT */}
      <Section title="DDT — Desired Dough Temperature">
        <div className="space-y-0">
          <Row label="Target FDT" value={fmtTemp(24)} />
          <Row label={`Flour temperature`} value={fmtTemp(toC(inputs.flourTemp, unit))} />
          <Row label={`Room temperature`} value={fmtTemp(toC(inputs.ambientTemp, unit))} />
          <Row label={`Fridge temperature (biga)`} value={fmtTemp(toC(inputs.fridgeTemp, unit))} />
          <Row label={`Friction factor (${inputs.mixerType})`} value={`+${temps.frictionFactor}°C`} />
          <Row label="Biga water temperature" value={fmtTemp(temps.bigaWater)} highlight />
          <Row label="Final dough water temperature" value={fmtTemp(temps.finalDoughWater)} highlight />
        </div>
        {waterTempNote && (
          <div className="mt-2 note-box text-xs">{waterTempNote}</div>
        )}
        {temps.finalDoughWater > 39 && (
          <div className="mt-2 warning-box text-xs">
            Water temperature {fmtTemp(temps.finalDoughWater)} is warm. Yeast begins to die above 43°C. Measure carefully.
          </div>
        )}
      </Section>

      {/* Total Weights Summary */}
      <Section title="Total Ingredient Weights">
        <div className="space-y-0">
          <Row label="Total dough" value={fmtG(weights.totalDough)} highlight />
          <Row label="Total flour" value={fmtG(weights.totalFlour)} />
          <Row label="Total water" value={fmtG(weights.totalWater)} />
          <Row label="Salt" value={fmtG(weights.salt)} />
          {inputs.oilEnabled && <Row label="Oil" value={fmtG(weights.oil)} />}
          {inputs.maltEnabled && <Row label="Diastatic malt" value={fmtG(weights.malt)} />}
          <Row label={`Biga yeast (${yeastLabel})`} value={fmtG(weights.bigaYeast)} />
          {weights.refreshYeast > 0 && (
            <Row label={`Refresh yeast (${yeastLabel})`} value={fmtG(weights.refreshYeast)} />
          )}
        </div>
      </Section>

      {/* Schedule */}
      <Section title="Stage-by-Stage Schedule">
        <div className="space-y-4">
          {schedule.map((stage, i) => (
            <div key={i} className="step-block">
              <div className="flex items-baseline gap-3 mb-1">
                <span className="text-amber-400 font-bold text-sm">{stage.label}</span>
                <span className="text-stone-500 text-xs font-mono">{stage.offset}</span>
              </div>
              <p className="text-sm text-stone-200 mb-1">{stage.action}</p>
              <div className="flex flex-wrap gap-3 text-xs">
                <span className="text-stone-500">⏱ {stage.duration}</span>
                <span className="text-stone-500">🌡 {stage.temp}</span>
              </div>
              {stage.lookFor && (
                <p className="text-xs text-amber-600/80 mt-1 italic">Look for: {stage.lookFor}</p>
              )}
            </div>
          ))}
        </div>
      </Section>

      {/* Five Leverage Points */}
      <Section title="Five Leverage Points — Canotto">
        <div className="space-y-2">
          {[
            {
              n: 1,
              title: `Flour P/L ${blend.pl.toFixed(2)}`,
              body: blend.pl <= 0.60
                ? '✓ In canotto range (0.50–0.60). Rim inflation is mechanically enabled.'
                : '⚠ Above canotto target. Rim may resist inflation. Reduce high-tenacity flours.',
            },
            {
              n: 2,
              title: 'Biga ripeness measured by pH 5.0–5.3',
              body: 'Not by smell or clock alone. A probe pH meter eliminates the guesswork that makes biga-based pizza feel unpredictable. One hour and 0.2 pH units is the difference between a great bake and structural failure.',
            },
            {
              n: 3,
              title: 'Stop mixing at improved mix — NOT full windowpane',
              body: 'Canotto extensibility is lost by over-mixing, not gained. Stop when dough pulls from walls and windowpane is translucent-thick. Full paper-thin windowpane = tight rim that cannot inflate.',
            },
            {
              n: 4,
              title: `Cold retard at ${fmtTemp(toC(inputs.fridgeTemp, unit))} for ${inputs.timeline === 24 ? '~20h' : inputs.timeline === 48 ? '22-48h' : '48h'}`,
              body: 'Residual sugar accumulation (Maillard currency), amino acid deepening (flavor), and slow protease polishing of extensibility without destroying structure.',
            },
            {
              n: 5,
              title: `Floor ${inputs.floorTemp}°${unit}, bake 90–150 seconds`,
              body: floorC > 450
                ? '⚠ Floor above 450°C targets chewy Neapolitan texture. Reduce to 400-420°C for canotto crunch. Drive rim interior to 95-98°C.'
                : `✓ ${fmtTemp(floorC)} floor with extended bake allows rim walls to dehydrate after gelatinization = crunch. Drive rim interior to 95-98°C.`,
            },
          ].map(({ n, title, body }) => (
            <div key={n} className="flex gap-3 p-3 rounded-lg bg-stone-800/50">
              <div className="w-6 h-6 rounded-full bg-amber-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-amber-400 text-xs font-bold">{n}</span>
              </div>
              <div>
                <div className="text-sm font-medium text-stone-200">{title}</div>
                <div className="text-xs text-stone-400 mt-0.5">{body}</div>
              </div>
            </div>
          ))}
        </div>
      </Section>

      {/* Ball ripeness checklist */}
      <Section title="Ball Readiness Checklist (Pre-Bake)">
        <div className="space-y-0.5">
          {[
            'Poke test: press 1cm deep — READY = slow rebound over 3-5s | UNDER = immediate snap-back | OVER = stays dented (bake immediately)',
            'Surface: smooth, taut, slightly domed. Small subsurface bubbles visible under skin',
            'Volume: approximately doubled from balled weight',
            'Jiggle test: tray vibration produces a wave through the dough',
            'Edge: releases cleanly from container with slight stretch',
          ].map((item, i) => (
            <div key={i} className="checklist-item">
              <span className="text-emerald-500 mt-0.5">◆</span>
              <span>{item}</span>
            </div>
          ))}
        </div>
        <div className="mt-2 error-box text-xs">
          <strong>Over-proofed (irreversible):</strong> Dough collapsed/flat, sticky, large surface bubbles popping, strong alcohol/acetone smell, no oven spring. "From the outside it still looks like dough. But the outcome is already decided." — Schmitz
        </div>
      </Section>

      {/* Baking reference */}
      <Section title="Baking Protocol">
        <div className="space-y-0">
          <Row label="Floor temperature" value={`${inputs.floorTemp}°${unit}`} />
          <Row label="Dome temperature" value={`${inputs.domeTemp}°${unit}`} />
          <Row label="Bake time" value="90–150 seconds" />
          <Row label="Rotations" value="2–4 total" />
          <Row label="First rotation" value="At 30–40s (before 15s risks tearing)" />
          <Row label="Rim internal target" value="95–98°C (not the bread standard of 92°C)" />
          <Row label="Recovery between pies" value="3–5 min for stone re-saturation" />
        </div>
        <div className="mt-3 space-y-0.5">
          <div className="text-xs font-bold text-stone-400 uppercase tracking-wider mb-1">Positive Bake Indicators</div>
          {[
            'Rim taps hollow or papery — crunch confirmed',
            'Small cracks on rim top and sides (steam venting)',
            'Dense leopard spots on rim — not solid char patches',
            'Rim height 3–4+ cm',
            'Uniformly golden base with dark freckles',
          ].map((item, i) => (
            <div key={i} className="checklist-item text-xs">
              <span className="text-emerald-500">✓</span>
              <span>{item}</span>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}
