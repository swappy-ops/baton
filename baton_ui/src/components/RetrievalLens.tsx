import React from 'react';
import { motion } from 'framer-motion';
import { Database, Search, Target } from 'lucide-react';

export const RetrievalLens: React.FC = () => {
  const hits = [
    { id: '1', score: 0.94, content: "Neural Observatory is the primary semantic recall interface...", source: "TERMINOLOGY.md" },
    { id: '2', score: 0.88, content: "Spectral Fingerprint allows for forensic audio matching...", source: "SPECTRAL_ENGINE.md" },
  ];

  return (
    <div className="glass-panel h-full flex flex-col p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xs font-bold uppercase tracking-widest text-accent/80">Retrieval Lens</h3>
        <Database size={14} className="text-accent/40" />
      </div>
      <div className="space-y-4 overflow-y-auto pr-2 custom-scrollbar">
        {hits.map((hit) => (
          <div key={hit.id} className="space-y-1">
            <div className="flex justify-between items-center">
              <span className="text-[9px] font-mono text-accent bg-accent/10 px-1.5 py-0.5 rounded border border-accent/20">
                SCORE: {hit.score}
              </span>
              <span className="text-[9px] text-white/30 truncate max-w-[100px]">{hit.source}</span>
            </div>
            <p className="text-[10px] text-white/60 leading-tight italic">"{hit.content}"</p>
            <div className="h-0.5 w-full bg-white/5 rounded-full overflow-hidden">
                <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${hit.score * 100}%` }}
                    className="h-full bg-accent/40"
                />
            </div>
          </div>
        ))}
      </div>
      <div className="mt-auto pt-4 border-t border-white/5">
         <div className="flex items-center gap-2 text-white/20">
            <Search size={12} />
            <span className="text-[10px] font-mono">LATENT SPACE IDLE</span>
         </div>
      </div>
    </div>
  );
};
