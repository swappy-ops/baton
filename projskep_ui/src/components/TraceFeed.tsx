import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore } from '../stores/useStore';

const TraceCard = ({ trace }: { trace: any }) => {
  const isCritical = trace.category === 'FAILURES' || trace.is_pinned;
  const isWarning = trace.category === 'AUDITS' || trace.severity === 'warning';

  return (
    <motion.div 
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: 20, opacity: 0 }}
      className={`p-4 glass-panel mb-2 border-l-2 transition-all duration-300 relative group overflow-hidden ${
        isCritical ? 'border-l-error bg-error/5 shadow-[0_0_15px_rgba(255,68,68,0.05)]' : 
        isWarning ? 'border-l-warning bg-warning/5' : 
        'border-l-accent bg-accent/5'
      }`}
    >
      <div className="flex justify-between items-start mb-1">
        <span className={`telemetry-text tracking-[0.2em] font-bold ${
           isCritical ? 'text-error' : isWarning ? 'text-warning' : 'text-accent'
        }`}>
           {trace.category}
        </span>
        <span className="telemetry-text !text-white/20">{new Date(trace.timestamp * 1000).toLocaleTimeString()}</span>
      </div>
      <p className="text-[11px] text-white/80 font-mono leading-relaxed group-hover:text-white transition-colors">
        {trace.message}
      </p>
      
      {/* Subtle Scanner Glow */}
      <div className={`absolute top-0 right-0 w-16 h-16 bg-gradient-to-br from-transparent to-white/5 opacity-20 transform rotate-45 translate-x-8 -translate-y-8 group-hover:translate-x-4 group-hover:-translate-y-4 transition-transform duration-700`} />
    </motion.div>
  );
};

export const TraceFeed: React.FC = () => {
  const { traces } = useStore();

  return (
    <div className="flex flex-col h-full bg-black/20 p-4 border-b border-white/5">
      <div className="flex justify-between items-center mb-6">
        <div>
           <h3 className="cinematic-heading text-xs">Forensic Trace Feed</h3>
           <span className="telemetry-text">Execution Telemetry</span>
        </div>
        <div className="flex gap-2">
           <div className="w-2 h-2 rounded-full bg-accent animate-pulse shadow-[0_0_8px_#00d2ff]" />
        </div>
      </div>
      
      <div className="flex-grow overflow-y-auto pr-2 custom-scrollbar">
        <AnimatePresence initial={false}>
          {traces.length > 0 ? (
            traces.map((trace, idx) => (
              <TraceCard key={trace.id || idx} trace={trace} />
            ))
          ) : (
            <div className="h-full flex flex-col items-center justify-center opacity-20">
               <svg className="w-8 h-8 mb-2 animate-pulse-soft" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
               </svg>
               <span className="telemetry-text">Awaiting Telemetry...</span>
            </div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
