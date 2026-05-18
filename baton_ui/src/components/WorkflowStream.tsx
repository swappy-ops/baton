import React from 'react';
import { motion } from 'framer-motion';
import { Activity, Disc, Fingerprint, Shield } from 'lucide-react';

const workflows = [
  { id: '1', name: 'stability_audit', status: 'RUNNING', icon: Shield, color: 'text-accent' },
  { id: '2', name: 'continuity_check', status: 'IDLE', icon: Fingerprint, color: 'text-warning' },
  { id: '3', name: 'spectral_mapping', status: 'PENDING', icon: Disc, color: 'text-purple-400' },
];

export const WorkflowStream: React.FC = () => {
  return (
    <div className="glass-panel h-full flex flex-col p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xs font-bold uppercase tracking-widest text-white/40">Workflow Stream</h3>
        <Activity size={14} className="text-accent animate-pulse" />
      </div>
      <div className="space-y-3">
        {workflows.map((wf) => (
          <div key={wf.id} className="flex items-center gap-3 p-2 bg-white/5 rounded border border-white/5 group hover:border-white/10 transition-colors">
            <div className={`p-1.5 rounded bg-black/40 ${wf.color}`}>
              <wf.icon size={16} />
            </div>
            <div className="flex flex-col flex-grow">
              <span className="text-[10px] font-bold text-white/80">{wf.name}</span>
              <span className="text-[9px] text-white/30 uppercase font-mono">{wf.status}</span>
            </div>
            {wf.status === 'RUNNING' && (
              <div className="flex gap-0.5">
                {[1, 2, 3].map(i => (
                  <motion.div
                    key={i}
                    animate={{ height: [4, 12, 4] }}
                    transition={{ repeat: Infinity, duration: 1, delay: i * 0.2 }}
                    className="w-0.5 bg-accent/60"
                  />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
