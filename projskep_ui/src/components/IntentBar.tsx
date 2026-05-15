import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore, IntentMode } from '../stores/useStore';

export const IntentBar: React.FC = () => {
  const { intent, setIntent } = useStore();
  const [isOpen, setIsOpen] = useState(false);

  const modes: IntentMode[] = ['DEBUG', 'RESEARCH', 'BUILD', 'DESIGN', 'FORENSIC', 'DEEP_WORK'];

  return (
    <div className="relative group flex flex-col items-center">
      {/* Primary Command Core */}
      <motion.div 
        onClick={() => setIsOpen(!isOpen)}
        className="glass-panel px-8 py-3 rounded-full flex items-center gap-6 cursor-pointer hover:bg-black/60 transition-all duration-500 border-accent/20 shadow-[0_0_40px_rgba(0,0,0,0.5)] group-hover:border-accent/40"
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <div className="flex flex-col">
           <span className="telemetry-text tracking-[0.4em] !text-accent shadow-[0_0_10px_rgba(0,210,255,0.3)]">Active Intent</span>
           <div className="flex items-center gap-3">
              <span className="text-xl font-bold tracking-tight text-white/90">{intent.mode}</span>
              <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
           </div>
        </div>
        
        <div className="w-px h-10 bg-white/10" />

        <div className="flex flex-col items-end">
           <span className="telemetry-text">Orchestration</span>
           <span className="text-[10px] font-mono text-white/40 uppercase tracking-widest">{intent.depth === 'high' ? 'High Entropy' : 'Low Latency'}</span>
        </div>
      </motion.div>

      {/* Mode Selection Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            className="absolute top-full mt-4 glass-panel p-2 rounded-2xl grid grid-cols-3 gap-1 z-[100] w-[450px]"
          >
            {modes.map((mode) => (
              <button
                key={mode}
                onClick={() => {
                  setIntent({ mode });
                  setIsOpen(false);
                }}
                className={`px-4 py-3 rounded-xl transition-all duration-300 font-mono text-[10px] uppercase tracking-widest text-left relative overflow-hidden group/btn ${
                  intent.mode === mode ? 'bg-accent/20 text-accent border border-accent/30' : 'bg-transparent text-white/40 hover:bg-white/5 border border-transparent'
                }`}
              >
                <span className="relative z-10">{mode}</span>
                {intent.mode === mode && (
                  <motion.div 
                    layoutId="active-bg"
                    className="absolute inset-0 bg-accent/10 pointer-events-none"
                  />
                )}
                <div className="absolute inset-0 bg-gradient-to-r from-accent/0 via-accent/5 to-accent/0 opacity-0 group-hover/btn:opacity-100 transition-opacity translate-x-[-100%] group-hover/btn:translate-x-[100%] duration-1000" />
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Subtle Bottom Pulse */}
      <motion.div 
        className="w-1/2 h-0.5 bg-gradient-to-r from-transparent via-accent/30 to-transparent blur-sm mt-1"
        animate={{ opacity: [0.2, 0.5, 0.2] }}
        transition={{ duration: 3, repeat: Infinity }}
      />
    </div>
  );
};
