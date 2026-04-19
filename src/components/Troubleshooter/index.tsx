import { useState } from 'react';
import { TROUBLESHOOT_DATA } from '../../data/troubleshooter';

export function Troubleshooter() {
  const [selected, setSelected] = useState<string | null>(null);

  const entry = TROUBLESHOOT_DATA.find(e => e.id === selected);

  return (
    <div>
      <div className="card mb-4">
        <div className="section-title">Symptom Lookup</div>
        <p className="text-sm text-stone-400 mb-4">
          Select the symptom you're experiencing to get targeted diagnosis and fixes.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {TROUBLESHOOT_DATA.map((item) => (
            <button
              key={item.id}
              onClick={() => setSelected(item.id === selected ? null : item.id)}
              className={`text-left p-3 rounded-lg border transition-all ${
                selected === item.id
                  ? 'border-amber-500 bg-amber-950/30 text-amber-200'
                  : 'border-stone-700/60 text-stone-300 hover:border-stone-600 hover:bg-stone-800'
              }`}
            >
              <div className="text-sm font-medium">{item.symptom}</div>
              <div className="text-xs text-stone-500 mt-0.5">{item.section}</div>
            </button>
          ))}
        </div>
      </div>

      {entry && (
        <div className="card border-amber-600/20">
          <div className="section-title text-amber-300">{entry.symptom}</div>

          <div className="mb-4">
            <div className="text-xs font-bold text-stone-400 uppercase tracking-wider mb-2">
              Likely Causes
            </div>
            <div className="space-y-1">
              {entry.causes.map((c, i) => (
                <div key={i} className="flex gap-2 text-sm text-stone-300">
                  <span className="text-red-400 mt-0.5 flex-shrink-0">◆</span>
                  <span>{c}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <div className="text-xs font-bold text-stone-400 uppercase tracking-wider mb-2">
              Fixes & Next Steps
            </div>
            <div className="space-y-1.5">
              {entry.fixes.map((f, i) => (
                <div key={i} className="flex gap-2 text-sm text-stone-200">
                  <span className="text-emerald-400 mt-0.5 flex-shrink-0">→</span>
                  <span>{f}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {!selected && (
        <div className="card border-stone-700/30">
          <div className="section-title">Enzyme Management Quick Reference</div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="text-stone-500 border-b border-stone-700">
                  <th className="text-left py-2 pr-4">State</th>
                  <th className="text-left py-2 pr-4">Windowpane</th>
                  <th className="text-left py-2 pr-4">Stretch</th>
                  <th className="text-left py-2 pr-4">Smell</th>
                  <th className="text-left py-2">Poke Test</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-stone-800">
                  <td className="py-2 pr-4 font-medium text-blue-300">Under-fermented</td>
                  <td className="py-2 pr-4 text-stone-400">Tears thick, no translucency</td>
                  <td className="py-2 pr-4 text-stone-400">Snaps back hard</td>
                  <td className="py-2 pr-4 text-stone-400">Raw flour only</td>
                  <td className="py-2 text-stone-400">Bounces back fast</td>
                </tr>
                <tr className="border-b border-stone-800 bg-emerald-950/10">
                  <td className="py-2 pr-4 font-medium text-emerald-300">Optimal (canotto)</td>
                  <td className="py-2 pr-4 text-stone-300">Translucent, tears with slight puncture</td>
                  <td className="py-2 pr-4 text-stone-300">Extends and holds, slow memory</td>
                  <td className="py-2 pr-4 text-stone-300">Bread, slight alcohol, faint sweet</td>
                  <td className="py-2 text-stone-300">Slow recovery 3-5s</td>
                </tr>
                <tr>
                  <td className="py-2 pr-4 font-medium text-red-300">Over-fermented</td>
                  <td className="py-2 pr-4 text-stone-400">Falls apart, liquid edges</td>
                  <td className="py-2 pr-4 text-stone-400">Extends indefinitely OR tears brittle</td>
                  <td className="py-2 pr-4 text-stone-400">Acetone, sharp vinegar, ammoniacal</td>
                  <td className="py-2 text-stone-400">Stays dented or collapses</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="card mt-4 border-stone-700/30">
        <div className="section-title">pH Quick Reference</div>
        <div className="space-y-0">
          {[
            { ph: '~6.0', label: 'Fresh biga mix', color: 'text-stone-400', note: 'Under-matured — poor opening' },
            { ph: '5.5–5.8', label: 'Young biga', color: 'text-blue-300', note: 'Snappy, tight, not ready' },
            { ph: '5.0–5.3', label: 'Ripe biga (canotto target)', color: 'text-emerald-300', note: 'Extensible with memory — open cleanly' },
            { ph: '4.8–5.0', label: 'Over-ripe biga', color: 'text-amber-300', note: 'Inspect closely — some protease damage' },
            { ph: '<4.8', label: 'Over-fermented — irreversible', color: 'text-red-300', note: 'Protease damage — expect weak dough, no oven spring' },
          ].map((row, i) => (
            <div key={i} className="result-row">
              <div className="flex items-baseline gap-3">
                <span className={`font-mono text-sm ${row.color}`}>{row.ph}</span>
                <span className="text-stone-300 text-sm">{row.label}</span>
              </div>
              <span className="text-stone-500 text-xs">{row.note}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
