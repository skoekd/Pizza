import { useState } from 'react';
import type { UserInputs, FlourEntry, TempUnit, YeastType, MixerType, OvenType, Timeline, PuntataType, AprettoType } from '../../types';
import { FLOUR_DATABASE, CANOTTO_FRAMEWORKS } from '../../data/flours';
import { FieldRow, SectionHeading } from '../shared/FieldRow';

const DEFAULT_INPUTS: UserInputs = {
  tempUnit: 'C',
  ambientTemp: 22,
  flourTemp: 20,
  fridgeTemp: 4,
  numPizzas: 6,
  ballWeight: 270,
  bigaPct: 50,
  bigaHydration: 48,
  totalHydration: 72,
  timeline: 48,
  puntata: 'standard',
  appretto: 'standard',
  flourEntries: [
    { flourId: 'casillo_la8', percentage: 50 },
    { flourId: 'caputo_blue', percentage: 50 },
  ],
  yeastType: 'idy',
  saltPct: 2.5,
  oilEnabled: false,
  oilPct: 2,
  maltEnabled: false,
  maltPct: 0.2,
  mixerType: 'planetary',
  ovenType: 'gas_pizza',
  floorTemp: 410,
  domeTemp: 460,
};

interface Props {
  onCalculate: (inputs: UserInputs) => void;
}

export function InputForm({ onCalculate }: Props) {
  const [inputs, setInputs] = useState<UserInputs>(DEFAULT_INPUTS);
  const [flourSum, setFlourSum] = useState(100);
  const [selectedFramework, setSelectedFramework] = useState<string | null>(null);

  function set<K extends keyof UserInputs>(key: K, value: UserInputs[K]) {
    setInputs((prev) => ({ ...prev, [key]: value }));
  }

  function applyFramework(fwId: string) {
    const fw = CANOTTO_FRAMEWORKS.find((f) => f.id === fwId);
    if (!fw) return;
    const bigaPct = fwId === 'D' ? 100 : inputs.bigaPct;
    const entries: FlourEntry[] = [];

    if (fwId === 'D') {
      entries.push({ flourId: fw.bigaFlours[0].id, percentage: 100 });
    } else {
      const bigaDec = bigaPct / 100;
      const refreshDec = 1 - bigaDec;
      const flourMap: Record<string, number> = {};
      for (const b of fw.bigaFlours) {
        flourMap[b.id] = (flourMap[b.id] || 0) + (b.pct / 100) * bigaDec * 100;
      }
      for (const r of fw.refreshFlours) {
        flourMap[r.id] = (flourMap[r.id] || 0) + (r.pct / 100) * refreshDec * 100;
      }
      for (const [id, pct] of Object.entries(flourMap)) {
        entries.push({ flourId: id, percentage: Math.round(pct) });
      }
    }

    const sum = entries.reduce((a, e) => a + e.percentage, 0);
    setFlourSum(sum);
    setSelectedFramework(fwId);
    setInputs((prev) => ({ ...prev, bigaPct, flourEntries: entries }));
  }

  function updateFlourEntry(idx: number, field: keyof FlourEntry, value: string | number) {
    const updated = inputs.flourEntries.map((e, i) =>
      i === idx ? { ...e, [field]: value } : e,
    );
    setInputs((prev) => ({ ...prev, flourEntries: updated }));
    setFlourSum(updated.reduce((a, e) => a + (Number(e.percentage) || 0), 0));
    setSelectedFramework(null);
  }

  function addFlourEntry() {
    const usedIds = inputs.flourEntries.map(e => e.flourId);
    const available = FLOUR_DATABASE.find(f => !usedIds.includes(f.id));
    const newEntry: FlourEntry = { flourId: available?.id || FLOUR_DATABASE[0].id, percentage: 0 };
    setInputs((prev) => ({ ...prev, flourEntries: [...prev.flourEntries, newEntry] }));
    setSelectedFramework(null);
  }

  function removeFlourEntry(idx: number) {
    const updated = inputs.flourEntries.filter((_, i) => i !== idx);
    setInputs((prev) => ({ ...prev, flourEntries: updated }));
    setFlourSum(updated.reduce((a, e) => a + e.percentage, 0));
    setSelectedFramework(null);
  }

  const num = (v: string) => parseFloat(v) || 0;

  return (
    <div className="space-y-2">
      {/* Framework Quick-Select */}
      <div className="card">
        <div className="section-title">Quick-Start Framework</div>
        <p className="text-xs text-stone-400 mb-3">
          Apply a pre-built flour framework based on your available flours and process goal.
        </p>
        <div className="grid grid-cols-1 gap-2">
          {CANOTTO_FRAMEWORKS.map((fw) => {
            const isActive = selectedFramework === fw.id;
            return (
              <button
                key={fw.id}
                onClick={() => applyFramework(fw.id)}
                className={`text-left p-3 rounded-lg border transition-all group ${
                  isActive
                    ? 'border-amber-500/60 bg-amber-950/25'
                    : 'border-stone-700/60 hover:border-amber-500/50 hover:bg-stone-800'
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <div className={`text-sm font-medium ${isActive ? 'text-amber-300' : 'text-stone-200 group-hover:text-amber-300'}`}>
                    {fw.name}
                  </div>
                  {isActive && (
                    <span className="text-xs text-amber-400 shrink-0">✓ Applied</span>
                  )}
                </div>
                <div className="text-xs text-stone-500 mt-0.5">{fw.description}</div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Environment */}
      <div className="card">
        <SectionHeading>Environment & Temperatures</SectionHeading>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <FieldRow label="Unit">
            <select className="select-field" value={inputs.tempUnit}
              onChange={e => set('tempUnit', e.target.value as TempUnit)}>
              <option value="C">°C</option>
              <option value="F">°F</option>
            </select>
          </FieldRow>
          <FieldRow label={`Ambient Temp (°${inputs.tempUnit})`} hint="Room temp where dough sits">
            <input type="number" className="input-field" value={inputs.ambientTemp}
              onChange={e => set('ambientTemp', num(e.target.value))} />
          </FieldRow>
          <FieldRow label={`Flour Temp (°${inputs.tempUnit})`} hint="Temp of flour bag">
            <input type="number" className="input-field" value={inputs.flourTemp}
              onChange={e => set('flourTemp', num(e.target.value))} />
          </FieldRow>
          <FieldRow label={`Fridge Temp (°${inputs.tempUnit})`} hint="Target: 4°C / 39°F">
            <input type="number" className="input-field" value={inputs.fridgeTemp}
              onChange={e => set('fridgeTemp', num(e.target.value))} />
          </FieldRow>
        </div>
      </div>

      {/* Flour Blend */}
      <div className="card">
        <SectionHeading>Flour Blend</SectionHeading>
        {selectedFramework && (
          <p className="text-xs text-amber-500/60 -mt-2 mb-3">
            Framework {selectedFramework} applied — edit freely below
          </p>
        )}
        <div className="space-y-3">
          {inputs.flourEntries.map((entry, idx) => (
            <div key={idx} className="flex gap-3 items-end">
              <div className="flex-1">
                <label className="label">Flour {idx + 1}</label>
                <select className="select-field" value={entry.flourId}
                  onChange={e => updateFlourEntry(idx, 'flourId', e.target.value)}>
                  {FLOUR_DATABASE.map(f => (
                    <option key={f.id} value={f.id}>{f.name}</option>
                  ))}
                </select>
              </div>
              <div className="w-24">
                <label className="label">%</label>
                <input type="number" min={0} max={100} className="input-field"
                  value={entry.percentage}
                  onChange={e => updateFlourEntry(idx, 'percentage', num(e.target.value))} />
              </div>
              {inputs.flourEntries.length > 1 && (
                <button onClick={() => removeFlourEntry(idx)}
                  className="mb-0.5 text-stone-500 hover:text-red-400 text-lg leading-none transition-colors">
                  ×
                </button>
              )}
            </div>
          ))}
          <div className="flex items-center justify-between">
            <button onClick={addFlourEntry}
              className="text-xs text-amber-400 hover:text-amber-300 transition-colors">
              + Add flour
            </button>
            <span className={`text-xs font-mono ${Math.abs(flourSum - 100) > 0.5 ? 'text-red-400' : 'text-emerald-400'}`}>
              Total: {flourSum}%
            </span>
          </div>
          {Math.abs(flourSum - 100) > 0.5 && (
            <p className="text-xs text-red-400">Flour percentages must sum to 100%</p>
          )}
        </div>

        {/* Flour reference */}
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="text-stone-500">
                <th className="text-left py-1 pr-3">Flour</th>
                <th className="text-center py-1 px-2">W</th>
                <th className="text-center py-1 px-2">P/L</th>
                <th className="text-center py-1 px-2">FN</th>
                <th className="text-center py-1 px-2">Type</th>
                <th className="text-left py-1 pl-2">Role</th>
              </tr>
            </thead>
            <tbody>
              {FLOUR_DATABASE.map(f => (
                <tr key={f.id} className="border-t border-stone-800">
                  <td className="py-1.5 pr-3 text-stone-300 font-medium whitespace-nowrap">{f.name}</td>
                  <td className="text-center py-1.5 px-2 font-mono text-stone-300">{f.w}</td>
                  <td className="text-center py-1.5 px-2 font-mono text-stone-300">{f.pl.toFixed(2)}</td>
                  <td className="text-center py-1.5 px-2 font-mono text-stone-300">{f.fn}</td>
                  <td className="text-center py-1.5 px-2 text-stone-400">{f.type}</td>
                  <td className="py-1.5 pl-2 text-stone-500">
                    {!f.canUseInBiga && f.canUseInRefresh ? 'Refresh only' :
                     f.canUseInBiga && f.canUseInRefresh ? 'Biga or refresh' : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Process Architecture */}
      <div className="card">
        <SectionHeading>Process Architecture</SectionHeading>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <FieldRow label="Number of Pizzas">
            <input type="number" min={1} max={50} className="input-field" value={inputs.numPizzas}
              onChange={e => set('numPizzas', num(e.target.value))} />
          </FieldRow>
          <FieldRow label="Ball Weight (g)" hint="Default: 270g">
            <input type="number" min={200} max={400} className="input-field" value={inputs.ballWeight}
              onChange={e => set('ballWeight', num(e.target.value))} />
          </FieldRow>
          <FieldRow label="Process Timeline">
            <select className="select-field" value={inputs.timeline}
              onChange={e => set('timeline', num(e.target.value) as Timeline)}>
              <option value={24}>24h</option>
              <option value={48}>48h</option>
              <option value={72}>72h</option>
            </select>
          </FieldRow>
          <FieldRow label="Biga %" hint="% of total flour in biga">
            <input type="number" min={10} max={100} className="input-field" value={inputs.bigaPct}
              onChange={e => set('bigaPct', num(e.target.value))} />
          </FieldRow>
          <FieldRow label="Biga Hydration %" hint="44–50% typical for biga">
            <input type="number" min={40} max={60} className="input-field" value={inputs.bigaHydration}
              onChange={e => set('bigaHydration', num(e.target.value))} />
          </FieldRow>
          <FieldRow label="Total Hydration %" hint="68–80%, target 72%">
            <input type="number" min={60} max={90} className="input-field" value={inputs.totalHydration}
              onChange={e => set('totalHydration', num(e.target.value))} />
          </FieldRow>
          <FieldRow label="Puntata (Bulk)" hint="Room temp bulk rest">
            <select className="select-field" value={inputs.puntata}
              onChange={e => set('puntata', e.target.value as PuntataType)}>
              <option value="short">Short (45–60 min)</option>
              <option value="standard">Standard (60–90 min)</option>
              <option value="long">Long (90–120 min)</option>
            </select>
          </FieldRow>
          <FieldRow label="Appretto (Final Proof)" hint="Ball room temp proof">
            <select className="select-field" value={inputs.appretto}
              onChange={e => set('appretto', e.target.value as AprettoType)}>
              <option value="short">Short (1.5–2h)</option>
              <option value="standard">Standard (2–3h)</option>
              <option value="long">Long (3–4h)</option>
            </select>
          </FieldRow>
        </div>
      </div>

      {/* Yeast */}
      <div className="card">
        <SectionHeading>Yeast</SectionHeading>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <FieldRow label="Yeast Type">
            <select className="select-field" value={inputs.yeastType}
              onChange={e => set('yeastType', e.target.value as YeastType)}>
              <option value="idy">Instant Dry Yeast (IDY)</option>
              <option value="fresh">Fresh Yeast</option>
              <option value="ady">Active Dry Yeast (ADY)</option>
            </select>
          </FieldRow>
          <div className="flex items-end">
            <p className="text-xs text-stone-500 leading-relaxed">
              Conversion: 1g Fresh = 0.33g IDY = 0.40g ADY.<br />
              <span className="text-amber-500/80">In practice, 1g IDY often behaves closer to 2g Fresh in warm environments.</span>
            </p>
          </div>
        </div>
      </div>

      {/* Optional Additions */}
      <div className="card">
        <SectionHeading>Salt, Oil & Malt</SectionHeading>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <FieldRow label="Salt %" hint="Default 2.5%, range 2.0–3.0%">
            <input type="number" min={1.5} max={3.5} step={0.1} className="input-field"
              value={inputs.saltPct}
              onChange={e => set('saltPct', num(e.target.value))} />
          </FieldRow>
          <FieldRow label="Oil">
            <div className="flex gap-2 items-center">
              <input type="checkbox" className="w-4 h-4 accent-amber-500"
                checked={inputs.oilEnabled}
                onChange={e => set('oilEnabled', e.target.checked)} />
              <input type="number" min={0} max={3} step={0.5} className="input-field"
                disabled={!inputs.oilEnabled} value={inputs.oilPct}
                onChange={e => set('oilPct', num(e.target.value))} />
              <span className="text-stone-400 text-sm">%</span>
            </div>
          </FieldRow>
          <FieldRow label="Diastatic Malt" hint="Only if FN>350 + oven <300°C">
            <div className="flex gap-2 items-center">
              <input type="checkbox" className="w-4 h-4 accent-amber-500"
                checked={inputs.maltEnabled}
                onChange={e => set('maltEnabled', e.target.checked)} />
              <input type="number" min={0} max={0.5} step={0.05} className="input-field"
                disabled={!inputs.maltEnabled} value={inputs.maltPct}
                onChange={e => set('maltPct', num(e.target.value))} />
              <span className="text-stone-400 text-sm">%</span>
            </div>
          </FieldRow>
        </div>
      </div>

      {/* Equipment & Baking */}
      <div className="card">
        <SectionHeading>Equipment & Baking</SectionHeading>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <FieldRow label="Mixer Type" hint="Affects DDT friction factor">
            <select className="select-field" value={inputs.mixerType}
              onChange={e => set('mixerType', e.target.value as MixerType)}>
              <option value="hand">Hand / gentle folds (+3°C)</option>
              <option value="fork">Fork mixer (+4°C)</option>
              <option value="planetary">Planetary / KitchenAid (+6°C)</option>
              <option value="planetary_long">Planetary — long biga mix (+10°C)</option>
              <option value="spiral">Spiral mixer (+10°C)</option>
            </select>
          </FieldRow>
          <FieldRow label="Oven Type">
            <select className="select-field" value={inputs.ovenType}
              onChange={e => set('ovenType', e.target.value as OvenType)}>
              <option value="gas_pizza">Gas pizza oven (Gozney Arc XL etc.)</option>
              <option value="wood">Wood-fired pizza oven</option>
              <option value="home_steel">Home oven with baking steel or stone</option>
              <option value="home_no_steel">Home oven (no steel/stone)</option>
            </select>
          </FieldRow>
          <FieldRow label={`Floor Temp (°${inputs.tempUnit})`} hint="Target 400–420°C for canotto crunch">
            <input type="number" className="input-field" value={inputs.floorTemp}
              onChange={e => set('floorTemp', num(e.target.value))} />
          </FieldRow>
          <FieldRow label={`Dome Temp (°${inputs.tempUnit})`} hint="Target 450–480°C">
            <input type="number" className="input-field" value={inputs.domeTemp}
              onChange={e => set('domeTemp', num(e.target.value))} />
          </FieldRow>
        </div>
      </div>

      <div className="flex justify-center pt-2 pb-4">
        <button
          className="btn-primary text-base px-12 py-4"
          disabled={Math.abs(flourSum - 100) > 0.5}
          onClick={() => onCalculate(inputs)}
        >
          Calculate Recipe
        </button>
      </div>
    </div>
  );
}
