import { useState, useEffect } from 'react';
import type { BakeLogEntry } from '../../types';
import { FieldRow, SectionHeading } from '../shared/FieldRow';

const STORAGE_KEY = 'canotto_bake_logs';

const EMPTY_LOG: Omit<BakeLogEntry, 'id' | 'date'> = {
  protocolNumber: '',
  method: '48h Biga',
  fermentationTime: '',
  flours: '',
  yeastAmountType: '',
  hydration: 72,
  salt: 2.5,
  goal: 'Maximum canotto rim, crunchy crust like Daniel Gigì',
  roomTempMix: 22,
  flourTempMix: 20,
  waterTempCalc: 0,
  waterTempActual: 0,
  prefermentTemp: 19,
  fdt: 24,
  mixingMinutes: 12,
  bulkRoomHours: 1,
  bulkFridgeHours: 0,
  ballRoomHours: 0,
  ballFridgeHours: 22,
  ballWeightUsed: 270,
  finalProofTime: 2.5,
  finalProofTemp: 22,
  ovenType: 'Gas pizza oven',
  bakingTemp: 410,
  bakingMinutes: 2,
  specialNotes: '',
  scoreCornicione: 0,
  scoreCrumb: 0,
  scoreFlavor: 0,
  scoreHandling: 0,
  scoreOvenSpring: 0,
  scoreOverall: 0,
  nextNotes: '',
};

function ScoreInput({ label, value, onChange }: { label: string; value: number; onChange: (v: number) => void }) {
  return (
    <div className="flex flex-col gap-1">
      <span className="label">{label}</span>
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => (
          <button
            key={n}
            onClick={() => onChange(n)}
            className={`w-7 h-7 rounded text-xs font-bold transition-colors ${
              value === n
                ? 'bg-amber-500 text-stone-950'
                : value >= n
                ? 'bg-amber-800/60 text-amber-300'
                : 'bg-stone-700 text-stone-500 hover:bg-stone-600'
            }`}
          >
            {n}
          </button>
        ))}
      </div>
    </div>
  );
}

function LogCard({ log, onDelete }: { log: BakeLogEntry; onDelete: () => void }) {
  const [expanded, setExpanded] = useState(false);
  const avgScore = log.scoreOverall || Math.round(
    (log.scoreCornicione + log.scoreCrumb + log.scoreFlavor + log.scoreHandling + log.scoreOvenSpring) / 5
  );

  return (
    <div className="card border-stone-700/40">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-stone-200 font-medium text-sm">
              {log.date} {log.protocolNumber ? `· #${log.protocolNumber}` : ''}
            </span>
            {avgScore > 0 && (
              <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                avgScore >= 8 ? 'bg-emerald-900/50 text-emerald-300' :
                avgScore >= 6 ? 'bg-amber-900/50 text-amber-300' :
                'bg-red-900/50 text-red-300'
              }`}>
                {avgScore}/10
              </span>
            )}
          </div>
          <div className="text-xs text-stone-500 mt-0.5">{log.method} · {log.flours}</div>
        </div>
        <div className="flex gap-2">
          <button onClick={() => setExpanded(!expanded)} className="text-xs text-stone-400 hover:text-stone-200 transition-colors">
            {expanded ? 'Collapse' : 'Expand'}
          </button>
          <button onClick={onDelete} className="text-xs text-stone-600 hover:text-red-400 transition-colors">
            Delete
          </button>
        </div>
      </div>

      {expanded && (
        <div className="mt-4 space-y-3 text-xs text-stone-300">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div><span className="text-stone-500">Hydration:</span> {log.hydration}%</div>
            <div><span className="text-stone-500">Salt:</span> {log.salt}%</div>
            <div><span className="text-stone-500">Ball weight:</span> {log.ballWeightUsed}g</div>
            <div><span className="text-stone-500">FDT:</span> {log.fdt}°C</div>
            <div><span className="text-stone-500">Room temp:</span> {log.roomTempMix}°C</div>
            <div><span className="text-stone-500">Water (calc):</span> {log.waterTempCalc}°C</div>
            <div><span className="text-stone-500">Water (actual):</span> {log.waterTempActual}°C</div>
            <div><span className="text-stone-500">Bake temp:</span> {log.bakingTemp}°C</div>
          </div>
          <div><span className="text-stone-500">Goal:</span> {log.goal}</div>
          {log.specialNotes && <div><span className="text-stone-500">Notes:</span> {log.specialNotes}</div>}
          <div className="grid grid-cols-3 sm:grid-cols-6 gap-2 pt-1">
            {[
              ['Cornicione', log.scoreCornicione],
              ['Crumb', log.scoreCrumb],
              ['Flavor', log.scoreFlavor],
              ['Handling', log.scoreHandling],
              ['Oven Spring', log.scoreOvenSpring],
              ['Overall', log.scoreOverall],
            ].map(([label, score]) => (
              <div key={label as string} className="text-center">
                <div className="text-stone-500 text-xs">{label}</div>
                <div className={`text-lg font-bold ${Number(score) >= 8 ? 'text-emerald-300' : Number(score) >= 6 ? 'text-amber-300' : 'text-stone-400'}`}>
                  {score || '—'}
                </div>
              </div>
            ))}
          </div>
          {log.nextNotes && (
            <div className="bg-stone-800/50 rounded p-2">
              <span className="text-amber-400 font-medium">Next session:</span> {log.nextNotes}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export function BakeLog() {
  const [logs, setLogs] = useState<BakeLogEntry[]>([]);
  const [form, setForm] = useState<Omit<BakeLogEntry, 'id' | 'date'>>(EMPTY_LOG);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) setLogs(JSON.parse(stored));
  }, []);

  function saveLogs(updated: BakeLogEntry[]) {
    setLogs(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  }

  function handleSubmit() {
    const newLog: BakeLogEntry = {
      ...form,
      id: Date.now().toString(),
      date: new Date().toLocaleDateString('en-GB', { year: 'numeric', month: 'short', day: 'numeric' }),
    };
    saveLogs([newLog, ...logs]);
    setForm(EMPTY_LOG);
    setShowForm(false);
  }

  function deleteLog(id: string) {
    saveLogs(logs.filter(l => l.id !== id));
  }

  const num = (v: string) => parseFloat(v) || 0;

  const set = <K extends keyof typeof form>(key: K, value: typeof form[K]) =>
    setForm(prev => ({ ...prev, [key]: value }));

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-base font-bold text-stone-200">Bake Log</h2>
          <p className="text-xs text-stone-500 mt-0.5">{logs.length} session{logs.length !== 1 ? 's' : ''} recorded</p>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Session'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-4 border-amber-600/20">
          <div className="section-title">New Bake Session</div>

          <SectionHeading>Protocol Info</SectionHeading>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <FieldRow label="Protocol #">
              <input className="input-field" value={form.protocolNumber}
                onChange={e => set('protocolNumber', e.target.value)} placeholder="e.g. 12" />
            </FieldRow>
            <FieldRow label="Method">
              <input className="input-field" value={form.method}
                onChange={e => set('method', e.target.value)} placeholder="48h Biga" />
            </FieldRow>
            <FieldRow label="Fermentation Time">
              <input className="input-field" value={form.fermentationTime}
                onChange={e => set('fermentationTime', e.target.value)} placeholder="48h total" />
            </FieldRow>
            <FieldRow label="Flours Used" className="sm:col-span-2">
              <input className="input-field" value={form.flours}
                onChange={e => set('flours', e.target.value)} placeholder="50% La 8 Plus + 50% Caputo Blue" />
            </FieldRow>
            <FieldRow label="Yeast (amount + type)">
              <input className="input-field" value={form.yeastAmountType}
                onChange={e => set('yeastAmountType', e.target.value)} placeholder="0.5g IDY biga" />
            </FieldRow>
            <FieldRow label="Hydration %">
              <input type="number" className="input-field" value={form.hydration}
                onChange={e => set('hydration', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Salt %">
              <input type="number" className="input-field" value={form.salt}
                onChange={e => set('salt', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Goal" className="sm:col-span-3">
              <input className="input-field" value={form.goal}
                onChange={e => set('goal', e.target.value)} />
            </FieldRow>
          </div>

          <SectionHeading>Mixing Log</SectionHeading>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <FieldRow label="Room Temp (°C)">
              <input type="number" className="input-field" value={form.roomTempMix}
                onChange={e => set('roomTempMix', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Flour Temp (°C)">
              <input type="number" className="input-field" value={form.flourTempMix}
                onChange={e => set('flourTempMix', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Water Temp Calc (°C)">
              <input type="number" className="input-field" value={form.waterTempCalc}
                onChange={e => set('waterTempCalc', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Water Temp Actual (°C)">
              <input type="number" className="input-field" value={form.waterTempActual}
                onChange={e => set('waterTempActual', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Preferment Temp (°C)">
              <input type="number" className="input-field" value={form.prefermentTemp}
                onChange={e => set('prefermentTemp', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="FDT Measured (°C)">
              <input type="number" className="input-field" value={form.fdt}
                onChange={e => set('fdt', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Mix Time (min)">
              <input type="number" className="input-field" value={form.mixingMinutes}
                onChange={e => set('mixingMinutes', num(e.target.value))} />
            </FieldRow>
          </div>

          <SectionHeading>Fermentation Log</SectionHeading>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <FieldRow label="Bulk Room (h)">
              <input type="number" className="input-field" value={form.bulkRoomHours}
                onChange={e => set('bulkRoomHours', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Bulk Fridge (h)">
              <input type="number" className="input-field" value={form.bulkFridgeHours}
                onChange={e => set('bulkFridgeHours', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Ball Room (h)">
              <input type="number" className="input-field" value={form.ballRoomHours}
                onChange={e => set('ballRoomHours', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Ball Fridge (h)">
              <input type="number" className="input-field" value={form.ballFridgeHours}
                onChange={e => set('ballFridgeHours', num(e.target.value))} />
            </FieldRow>
          </div>

          <SectionHeading>Baking Log</SectionHeading>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <FieldRow label="Ball Weight (g)">
              <input type="number" className="input-field" value={form.ballWeightUsed}
                onChange={e => set('ballWeightUsed', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Final Proof Time (h)">
              <input type="number" className="input-field" value={form.finalProofTime}
                onChange={e => set('finalProofTime', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Final Proof Temp (°C)">
              <input type="number" className="input-field" value={form.finalProofTemp}
                onChange={e => set('finalProofTemp', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Oven Type">
              <input className="input-field" value={form.ovenType}
                onChange={e => set('ovenType', e.target.value)} />
            </FieldRow>
            <FieldRow label="Baking Temp (°C)">
              <input type="number" className="input-field" value={form.bakingTemp}
                onChange={e => set('bakingTemp', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Baking Time (min)">
              <input type="number" className="input-field" value={form.bakingMinutes}
                onChange={e => set('bakingMinutes', num(e.target.value))} />
            </FieldRow>
            <FieldRow label="Special Notes" className="sm:col-span-2">
              <input className="input-field" value={form.specialNotes}
                onChange={e => set('specialNotes', e.target.value)} placeholder="Observations..." />
            </FieldRow>
          </div>

          <SectionHeading>Result Scoring (1–10)</SectionHeading>
          <div className="space-y-3">
            <ScoreInput label="Cornicione Rise" value={form.scoreCornicione} onChange={v => set('scoreCornicione', v)} />
            <ScoreInput label="Crumb Openness" value={form.scoreCrumb} onChange={v => set('scoreCrumb', v)} />
            <ScoreInput label="Flavor Profile" value={form.scoreFlavor} onChange={v => set('scoreFlavor', v)} />
            <ScoreInput label="Dough Handling" value={form.scoreHandling} onChange={v => set('scoreHandling', v)} />
            <ScoreInput label="Oven Spring" value={form.scoreOvenSpring} onChange={v => set('scoreOvenSpring', v)} />
            <ScoreInput label="Overall" value={form.scoreOverall} onChange={v => set('scoreOverall', v)} />
          </div>

          <SectionHeading>Notes for Next Session</SectionHeading>
          <textarea
            className="input-field min-h-20 resize-y"
            value={form.nextNotes}
            onChange={e => set('nextNotes', e.target.value)}
            placeholder="What to adjust next time..."
          />

          <div className="flex justify-end gap-3 mt-4">
            <button className="btn-secondary" onClick={() => setShowForm(false)}>Cancel</button>
            <button className="btn-primary" onClick={handleSubmit}>Save Session</button>
          </div>
        </div>
      )}

      {logs.length === 0 && !showForm && (
        <div className="card text-center py-12 border-stone-700/30">
          <div className="text-stone-500 mb-2">No bake sessions logged yet.</div>
          <p className="text-xs text-stone-600 max-w-sm mx-auto">
            After each bake, fill in your session log. Over multiple bakes the system identifies patterns — consistently low oven spring, check FDT data across logs.
          </p>
        </div>
      )}

      <div className="space-y-3">
        {logs.map(log => (
          <LogCard key={log.id} log={log} onDelete={() => deleteLog(log.id)} />
        ))}
      </div>
    </div>
  );
}
