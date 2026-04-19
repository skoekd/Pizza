import type React from 'react';

interface Props {
  label: string;
  hint?: string;
  children: React.ReactNode;
  className?: string;
}

export function FieldRow({ label, hint, children, className = '' }: Props) {
  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      <label className="label">{label}</label>
      {children}
      {hint && <p className="text-xs text-stone-500 leading-tight">{hint}</p>}
    </div>
  );
}

export function SectionHeading({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-3 mb-4 mt-6 first:mt-0">
      <div className="h-px flex-1 bg-stone-700/60" />
      <span className="text-xs font-bold text-amber-400 uppercase tracking-widest whitespace-nowrap">
        {children}
      </span>
      <div className="h-px flex-1 bg-stone-700/60" />
    </div>
  );
}
