import { useState } from 'react';
import type { UserInputs, RecipeResult } from '../../types';
import { calcBlendStats, calcWeights, calcTemperatures, ballToDisc, detectFramework } from '../../lib/calculations';
import { buildWarnings } from '../../lib/validation';
import { buildSchedule } from '../../lib/schedule';
import { InputForm } from './InputForm';
import { RecipeOutput } from './RecipeOutput';

export function RecipeGenerator() {
  const [result, setResult] = useState<RecipeResult | null>(null);
  const [view, setView] = useState<'form' | 'recipe'>('form');

  function handleCalculate(inputs: UserInputs) {
    const blend = calcBlendStats(inputs.flourEntries);
    const weights = calcWeights(inputs);
    const temps = calcTemperatures(inputs, weights);
    const warnings = buildWarnings(inputs, blend);
    const schedule = buildSchedule(inputs);
    const discDiameter = ballToDisc(inputs.ballWeight);
    const framework = detectFramework(inputs.flourEntries, inputs.bigaPct);

    setResult({ inputs, blend, weights, temps, warnings, schedule, discDiameter, framework });
    setView('recipe');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  return (
    <div>
      {result && (
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => setView('form')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${view === 'form' ? 'bg-amber-500 text-stone-950' : 'bg-stone-800 text-stone-400 hover:text-stone-200'}`}
          >
            Edit Inputs
          </button>
          <button
            onClick={() => setView('recipe')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${view === 'recipe' ? 'bg-amber-500 text-stone-950' : 'bg-stone-800 text-stone-400 hover:text-stone-200'}`}
          >
            Recipe Output
            {result.warnings.filter(w => w.severity !== 'note').length > 0 && (
              <span className="ml-2 bg-amber-600 text-white text-xs px-1.5 py-0.5 rounded-full">
                {result.warnings.filter(w => w.severity !== 'note').length}
              </span>
            )}
          </button>
        </div>
      )}
      {view === 'form' ? (
        <InputForm onCalculate={handleCalculate} />
      ) : (
        result && <RecipeOutput result={result} />
      )}
    </div>
  );
}
