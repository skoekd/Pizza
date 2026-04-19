import { useState } from 'react';
import './index.css';
import { RecipeGenerator } from './components/RecipeGenerator';
import { Troubleshooter } from './components/Troubleshooter';
import { BakeLog } from './components/BakeLog';

type Mode = 'recipe' | 'troubleshoot' | 'log';

export default function App() {
  const [mode, setMode] = useState<Mode>('recipe');

  const tabs: Array<{ id: Mode; label: string; sub: string }> = [
    { id: 'recipe', label: 'Recipe Generator', sub: 'Calculate your dough' },
    { id: 'troubleshoot', label: 'Troubleshooter', sub: 'Diagnose problems' },
    { id: 'log', label: 'Bake Log', sub: 'Track sessions' },
  ];

  return (
    <div className="min-h-screen bg-[#0f0e0c]">
      {/* Header */}
      <header className="border-b border-stone-800/80 bg-stone-950/80 sticky top-0 z-50 backdrop-blur-sm">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
          <div className="flex items-baseline gap-2">
            <span className="text-lg font-bold text-amber-400 tracking-tight">Canotto</span>
            <span className="text-stone-500 text-sm hidden sm:block">Dough Protocol Builder</span>
          </div>
          <div className="flex gap-1">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setMode(tab.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  mode === tab.id
                    ? 'bg-amber-500 text-stone-950'
                    : 'text-stone-400 hover:text-stone-200 hover:bg-stone-800'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Tagline */}
      {mode === 'recipe' && (
        <div className="bg-gradient-to-b from-stone-950 to-[#0f0e0c] border-b border-stone-800/40">
          <div className="max-w-3xl mx-auto px-4 py-5">
            <h1 className="text-2xl sm:text-3xl font-bold text-stone-100 leading-tight">
              Canotto Pizza Dough Calculator
            </h1>
            <p className="text-stone-400 text-sm mt-1.5 leading-relaxed max-w-xl">
              Designed for the large, airy, crunchy cornicione in the canotto / Romano-contemporanea style.
              All calculations from Schmitz <em>Control Your Dough</em> and Miele <em>Logic of Pizza Dough</em>.
            </p>
            <div className="flex flex-wrap gap-2 mt-3">
              {['BIGA pre-ferment', 'DDT water temps', 'Enzyme load', 'Fermentation schedule', 'pH guidance'].map(tag => (
                <span key={tag} className="text-xs px-2.5 py-1 rounded-full bg-stone-800 text-stone-400 border border-stone-700/50">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Main */}
      <main className="max-w-3xl mx-auto px-4 py-6">
        {mode === 'recipe' && <RecipeGenerator />}
        {mode === 'troubleshoot' && (
          <div>
            <div className="mb-5">
              <h2 className="text-xl font-bold text-stone-100">Troubleshooter</h2>
              <p className="text-stone-400 text-sm mt-1">
                Select a symptom for targeted diagnosis based on Schmitz and Miele protocols.
              </p>
            </div>
            <Troubleshooter />
          </div>
        )}
        {mode === 'log' && (
          <div>
            <div className="mb-5">
              <h2 className="text-xl font-bold text-stone-100">Bake Log</h2>
              <p className="text-stone-400 text-sm mt-1">
                Track each session. Over multiple bakes, patterns emerge — inconsistency becomes predictable.
              </p>
            </div>
            <BakeLog />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-stone-800/40 mt-8">
        <div className="max-w-3xl mx-auto px-4 py-4 text-xs text-stone-600 flex flex-wrap gap-4 justify-between">
          <span>Canotto Dough Protocol Builder v1.0</span>
          <span>Sources: Schmitz · Miele · PizzaBlab · Stadler Made</span>
        </div>
      </footer>
    </div>
  );
}
