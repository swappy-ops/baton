import React from 'react';
import { useStore } from '../stores/useStore';
import { motion } from 'framer-motion';

const StatusIndicator = ({ label, status, value }: { label: string; status: 'online' | 'offline' | 'degraded'; value?: string }) => (
  <div className="flex flex-col py-2 border-b border-white/5 last:border-0 group">
    <div className="flex items-center justify-between mb-1">
      <div className="flex items-center gap-2">
        <div className={`w-1 h-1 rounded-full ${
          status === 'online' ? 'bg-accent shadow-[0_0_8px_#00d2ff]' : 
          status === 'degraded' ? 'bg-warning shadow-[0_0_8px_#ffaa00]' : 
          'bg-error shadow-[0_0_8px_#ff4444]'
        }`} />
        <span className="telemetry-text tracking-[0.2em] group-hover:text-white/60 transition-colors">{label}</span>
      </div>
      <span className="text-[10px] font-mono text-white/90 group-hover:text-accent transition-colors">{value || status.toUpperCase()}</span>
    </div>
    <div className="h-[2px] bg-white/5 rounded-full overflow-hidden">
       <motion.div 
         className={`h-full ${status === 'online' ? 'bg-accent' : 'bg-warning'}`}
         initial={{ width: 0 }}
         animate={{ width: status === 'online' ? '100%' : '50%' }}
         transition={{ duration: 1, ease: "easeOut" }}
       />
    </div>
  </div>
);

export const StatusPanel: React.FC = () => {
  const { metrics } = useStore();
  
  return (
    <div className="glass-panel p-6 flex flex-col h-full border-l-2 border-l-accent/20 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute bottom-0 right-0 p-2 opacity-5 pointer-events-none">
         <svg className="w-24 h-24" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" strokeWidth="2" strokeDasharray="10 5" />
         </svg>
      </div>

      <div className="flex justify-between items-start mb-8 relative z-10">
        <div>
           <h3 className="cinematic-heading text-xs">System Integrity</h3>
           <span className="telemetry-text">Mission Control Status</span>
        </div>
        <div className="w-1.5 h-1.5 rounded-full bg-accent animate-ping" />
      </div>
      
      <div className="flex flex-col gap-2 relative z-10">
        <StatusIndicator label="Backend" status="online" value="v1.4.2" />
        <StatusIndicator label="WebSocket" status="online" value="RX: 14kb/s" />
        <StatusIndicator label="Watchdog" status="online" value="ACTIVE" />
        <StatusIndicator label="Retrieval" status="online" value="CHROMA" />
        <StatusIndicator label="SQLite" status="online" value="PERSISTENT" />
        <StatusIndicator label="Topology" status="online" value="STABLE" />
      </div>

      <div className="mt-auto pt-8 relative z-10">
        <div className="flex justify-between mb-2">
           <span className="telemetry-text !text-white/20">Compute Pressure</span>
           <span className="text-[10px] text-accent font-mono">12%</span>
        </div>
        <div className="h-1 bg-white/5 rounded-full overflow-hidden">
           <motion.div 
             className="h-full bg-gradient-to-r from-accent/40 to-accent shadow-[0_0_10px_#00d2ff]" 
             animate={{ width: ['12%', '15%', '12%'] }}
             transition={{ duration: 5, repeat: Infinity }}
           />
        </div>
        <div className="mt-4 flex justify-between items-center opacity-30 group">
           <span className="text-[8px] font-mono uppercase tracking-[0.3em]">Neural Link</span>
           <div className="flex gap-1">
              {[...Array(4)].map((_, i) => (
                 <div key={i} className="w-1 h-1 bg-accent rounded-full animate-pulse-soft" style={{ animationDelay: `${i * 0.2}s` }} />
              ))}
           </div>
        </div>
      </div>
    </div>
  );
};
