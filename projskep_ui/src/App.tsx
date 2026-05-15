import React, { useEffect } from 'react';
import { useStore } from './stores/useStore';
import { useWebSocket } from './hooks/useWebSocket';
import { IntentBar } from './components/IntentBar';
import { TopologyMap } from './components/TopologyMap';
import { TraceFeed } from './components/TraceFeed';
import { ContextBudgetMeter } from './components/ContextBudgetMeter';
import { StatusPanel } from './components/StatusPanel';
import { ReplayPanel } from './components/ReplayPanel';
import { SuggestionsQueue } from './components/SuggestionsQueue';
import { WorkflowStream } from './components/WorkflowStream';
import { motion, AnimatePresence } from 'framer-motion';

const App: React.FC = () => {
  const { setIntent, reportFriction } = useStore();
  const { isConnected } = useWebSocket('ws://localhost:8000/ws');

  // Hotkey System
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        // Intent Bar logic handled inside component via state if needed, 
        // but global listener can trigger it here.
      }
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'F') {
        e.preventDefault();
        const msg = prompt("Report Friction Point:");
        if (msg) reportFriction("User Feedback", msg);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [reportFriction]);

  return (
    <div className="flex h-screen w-screen bg-obsidian text-white overflow-hidden font-sans selection:bg-accent/30 relative">
      {/* Dynamic Background Pulse */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(0,210,255,0.02)_0%,transparent_70%)] pointer-events-none" />

      {/* Left Column: Intelligence & Strategy */}
      <motion.div 
        initial={{ x: -400 }}
        animate={{ x: 0 }}
        className="w-[400px] flex flex-col border-r border-white/5 bg-black/40 backdrop-blur-3xl z-20"
      >
        <div className="h-[280px]">
          <ContextBudgetMeter />
        </div>
        <div className="flex-grow overflow-hidden">
          <TraceFeed />
        </div>
        <div className="h-[240px]">
          <SuggestionsQueue />
        </div>
      </motion.div>

      {/* Center Column: Observation & Work */}
      <div className="flex-grow flex flex-col relative z-10">
        {/* Intent Bar (Command Center) */}
        <div className="absolute top-10 left-1/2 -translate-x-1/2 z-50">
          <IntentBar />
        </div>

        {/* Dynamic Canvas */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
          className="flex-grow relative"
        >
          <TopologyMap />
        </motion.div>

        {/* Workflow Stream (Floating) */}
        <div className="absolute bottom-52 right-8 w-80 z-40">
           <WorkflowStream />
        </div>

        {/* Forensic Replay (Bottom) */}
        <motion.div 
          initial={{ y: 200 }}
          animate={{ y: 0 }}
          className="h-56"
        >
          <ReplayPanel />
        </motion.div>
      </div>

      {/* Right Column: Operational Integrity */}
      <motion.div 
        initial={{ x: 300 }}
        animate={{ x: 0 }}
        className="w-[300px] flex flex-col border-l border-white/5 bg-black/30 backdrop-blur-2xl z-20"
      >
        <div className="flex-grow">
          <StatusPanel />
        </div>
        
        {/* Active Investigation Brief */}
        <div className="p-6 bg-black/60 border-t border-white/5 group">
           <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center">
                 <span className="telemetry-text !text-white/20">Active Investigation</span>
                 <div className="flex gap-1">
                    <div className="w-1 h-1 rounded-full bg-accent animate-pulse" />
                    <div className="w-1 h-1 rounded-full bg-accent/20" />
                 </div>
              </div>
              <span className="text-sm font-bold text-white group-hover:text-accent transition-colors truncate">vst3_bridge_synchronization</span>
              <div className="flex items-center gap-3 mt-1">
                 <div className="px-2 py-0.5 rounded-sm bg-accent/10 text-accent text-[9px] font-mono border border-accent/20">OPERATIONAL</div>
                 <span className="text-[10px] font-mono text-white/30 tracking-widest uppercase">04:42:11</span>
              </div>
           </div>
        </div>
      </motion.div>

      {/* Global Connection Status Overlay */}
      <AnimatePresence>
        {!isConnected && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black/90 backdrop-blur-md flex items-center justify-center"
          >
            <div className="flex flex-col items-center gap-6">
               <div className="w-16 h-16 rounded-full border-2 border-error border-t-transparent animate-spin" />
               <div className="flex flex-col items-center gap-2">
                  <span className="text-lg font-bold text-error uppercase tracking-[0.4em] animate-pulse">Connection Interrupted</span>
                  <span className="telemetry-text text-white/40">Re-establishing Neural Observatory Link...</span>
               </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default App;
