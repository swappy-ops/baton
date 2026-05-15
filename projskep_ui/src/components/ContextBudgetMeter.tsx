import React from 'react';
import { motion } from 'framer-motion';
import { useStore } from '../stores/useStore';

interface GaugeProps {
  label: string;
  value: number;
  color?: string;
}

const RadialGauge: React.FC<GaugeProps> = ({ label, value, color = "#00d2ff" }) => {
  const radius = 35;
  const circumference = Math.PI * radius;
  const offset = circumference - (Math.min(value, 100) / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center group">
      <div className="relative w-24 h-16 overflow-hidden">
        <svg className="w-full h-full transform -rotate-180">
          <circle
            cx="48"
            cy="48"
            r={radius}
            stroke="currentColor"
            strokeWidth="4"
            fill="transparent"
            strokeDasharray={`${circumference} ${circumference}`}
            className="text-white/5"
          />
          <motion.circle
            cx="48"
            cy="48"
            r={radius}
            stroke={color}
            strokeWidth="4"
            fill="transparent"
            strokeDasharray={`${circumference} ${circumference}`}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 2, ease: "circOut" }}
            strokeLinecap="butt"
          />
        </svg>
        <div className="absolute bottom-0 inset-x-0 flex flex-col items-center justify-end pb-0.5">
          <motion.span 
            className="text-[10px] font-mono font-bold text-white/90 group-hover:text-accent transition-colors"
            animate={{ opacity: [0.7, 1, 0.7] }}
            transition={{ duration: 3, repeat: Infinity }}
          >
            {value.toFixed(1)}%
          </motion.span>
          <span className="text-[7px] uppercase tracking-[0.2em] text-white/20 font-bold">{label}</span>
        </div>
      </div>
      
      {/* Decorative Glow Line */}
      <div className={`h-px w-8 transition-all duration-500 mt-1 ${value > 80 ? 'bg-error shadow-[0_0_5px_#ff4444]' : 'bg-white/5'}`} />
    </div>
  );
};

export const ContextBudgetMeter: React.FC = () => {
  const { metrics } = useStore();
  
  return (
    <div className="glass-panel p-6 flex flex-col h-full relative overflow-hidden group">
      {/* Ambient Lighting Overlay */}
      <div className="absolute -top-10 -right-10 w-32 h-32 bg-accent/5 rounded-full blur-3xl" />
      
      <div className="flex justify-between items-start mb-6 relative z-10">
        <div>
           <h3 className="cinematic-heading text-xs">Context Budget</h3>
           <span className="telemetry-text">Token Economics</span>
        </div>
        <div className="flex flex-col items-end">
           <span className="text-[10px] font-mono text-accent animate-pulse-soft">NOMINAL</span>
           <span className="text-[7px] text-white/20 uppercase tracking-widest">Efficiency</span>
        </div>
      </div>

      <div className="grid grid-cols-5 gap-0 flex-grow items-end pb-4 relative z-10">
        <RadialGauge label="Prompt" value={metrics.promptOverhead} />
        <RadialGauge label="Memory" value={metrics.memoryInjection} />
        <RadialGauge label="Retr" value={metrics.retrievalDuplication} />
        <RadialGauge label="Chat" value={metrics.agentChatter} />
        <RadialGauge label="Sem" value={metrics.semanticRedundancy} />
      </div>

      <div className="mt-auto border-t border-white/5 pt-4 flex justify-between items-center relative z-10">
          <span className="telemetry-text !text-white/20">Entropy Index</span>
          <div className="flex gap-1">
             {[...Array(5)].map((_, i) => (
                <div key={i} className={`w-3 h-0.5 rounded-full ${i < 3 ? 'bg-accent/40' : 'bg-white/5'}`} />
             ))}
          </div>
      </div>
    </div>
  );
};
