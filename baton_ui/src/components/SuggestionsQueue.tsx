import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, X, AlertTriangle, Zap } from 'lucide-react';
import { useStore } from '../stores/useStore';

export const SuggestionsQueue: React.FC = () => {
  const { suggestions } = useStore();

  return (
    <div className="glass-panel h-full flex flex-col p-4">
      <h3 className="text-xs font-bold uppercase tracking-widest text-warning/80 mb-4">Suggestions Queue</h3>
      <div className="flex-grow overflow-y-auto space-y-3 pr-2 custom-scrollbar">
        <AnimatePresence>
          {suggestions.length === 0 ? (
             <div className="text-white/10 h-full flex flex-col items-center justify-center italic gap-2">
                <Zap size={24} className="opacity-10" />
                <span>No pending proposals</span>
             </div>
          ) : (
            suggestions.map((s, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, x: 50 }}
                className="bg-black/40 border border-white/5 p-3 rounded-lg space-y-2 relative overflow-hidden group"
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-2">
                    <AlertTriangle size={14} className="text-warning" />
                    <span className="text-[10px] font-bold text-warning uppercase">{s.type}</span>
                  </div>
                  <span className="text-[9px] text-white/30 font-mono">2m ago</span>
                </div>
                <p className="text-xs text-white/80 leading-relaxed">{s.message}</p>
                <div className="flex gap-2 pt-1">
                  <button className="flex-grow flex items-center justify-center gap-1 py-1.5 bg-accent/20 text-accent rounded border border-accent/30 text-[10px] font-bold hover:bg-accent/30 transition-colors">
                    <Check size={12} /> ACCEPT
                  </button>
                  <button className="flex items-center justify-center w-8 bg-white/5 text-white/40 rounded border border-white/10 hover:bg-risk/20 hover:text-risk transition-colors">
                    <X size={12} />
                  </button>
                </div>
                <div className="absolute top-0 left-0 w-1 h-full bg-warning/50" />
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
