import React, { useState } from 'react';
import { motion } from 'framer-motion';

export const ReplayPanel: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [currentTime, setCurrentTime] = useState(422); // Seconds

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${h}:${m}:${s}:04`;
  };
  
  return (
    <div className="glass-panel p-6 flex flex-col h-full bg-black/60 border-t-2 border-t-warning/20 relative overflow-hidden group">
      {/* Decorative scanline */}
      <div className="absolute inset-0 bg-gradient-to-b from-white/[0.02] to-transparent pointer-events-none h-1" />

      <div className="flex justify-between items-start mb-4 relative z-10">
        <div>
           <h3 className="cinematic-heading text-xs !text-warning/80">Forensic Replay</h3>
           <span className="telemetry-text !text-warning/30">Cognition Black Box Recorder</span>
        </div>
        <div className="flex gap-4 items-center">
           <div className="flex flex-col items-end">
              <span className="telemetry-text !text-white/20">Archive Hash</span>
              <span className="text-[9px] font-mono text-white/40">0x7F2A...9C1D</span>
           </div>
           <div className={`px-3 py-1 rounded border transition-all duration-500 ${
             isPlaying ? 'bg-warning/20 border-warning/40 text-warning shadow-[0_0_15px_rgba(255,170,0,0.2)]' : 'bg-white/5 border-white/10 text-white/30'
           }`}>
             <span className="text-[10px] font-bold uppercase tracking-[0.2em]">{isPlaying ? 'REPLAY ACTIVE' : 'SYSTEM STANDBY'}</span>
           </div>
        </div>
      </div>

      <div className="flex-grow flex items-center gap-8 relative z-10 px-4">
         {/* Controls */}
         <div className="flex items-center gap-4">
            <button className="button-forensic p-2 rounded-full !bg-transparent border-none text-white/20 hover:text-warning hover:scale-110">
               <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6L18 18V6z"/></svg>
            </button>
            <button 
              onClick={() => setIsPlaying(!isPlaying)}
              className="w-14 h-14 rounded-full border-2 border-warning/30 flex items-center justify-center text-warning hover:bg-warning/10 hover:border-warning/60 transition-all duration-500 shadow-[0_0_20px_rgba(255,170,0,0.1)] group/play"
            >
              {isPlaying ? (
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
              ) : (
                <svg className="w-8 h-8 translate-x-1" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              )}
            </button>
            <button className="button-forensic p-2 rounded-full !bg-transparent border-none text-white/20 hover:text-warning hover:scale-110">
               <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg>
            </button>
         </div>

         {/* Timeline */}
         <div className="flex-grow flex flex-col gap-2">
            <div className="flex justify-between items-center mb-1">
               <div className="flex gap-6">
                  {[0.5, 1, 2, 4].map(s => (
                    <span 
                      key={s}
                      onClick={() => setPlaybackSpeed(s)}
                      className={`text-[10px] font-mono cursor-pointer transition-colors ${playbackSpeed === s ? 'text-warning' : 'text-white/20 hover:text-white/40'}`}
                    >
                      {s.toFixed(1)}X
                    </span>
                  ))}
               </div>
               <span className="text-xl font-mono text-warning/90 tracking-tighter">{formatTime(currentTime)}</span>
            </div>
            
            <div className="h-10 bg-white/5 rounded relative overflow-hidden group/timeline cursor-pointer border border-white/5 hover:border-white/10 transition-colors">
               <div className="absolute inset-0 flex items-end px-1 gap-[2px]">
                  {[...Array(80)].map((_, i) => (
                     <div 
                       key={i} 
                       className={`w-1 rounded-t transition-all duration-500 ${i % 10 === 0 ? 'bg-warning/40 h-2/3' : 'bg-warning/10 h-1/3'} group-hover/timeline:opacity-60`}
                       style={{ height: `${Math.random() * 40 + 20}%` }}
                     />
                  ))}
               </div>
               <motion.div 
                 className="absolute inset-y-0 left-0 bg-warning/20 border-r-2 border-warning shadow-[0_0_15px_rgba(255,170,0,0.5)] z-10" 
                 animate={{ width: isPlaying ? '100%' : '35%' }}
                 transition={{ duration: isPlaying ? 60 / playbackSpeed : 0, ease: "linear" }}
               />
               
               {/* Bookmark Indicators */}
               <div className="absolute top-0 left-1/4 w-px h-full bg-error/40 shadow-[0_0_5px_rgba(255,68,68,0.5)]" />
               <div className="absolute top-0 left-2/3 w-px h-full bg-accent/40 shadow-[0_0_5px_rgba(0,210,255,0.5)]" />
            </div>
         </div>
      </div>

      <div className="mt-4 flex justify-between items-center px-4 opacity-40">
         <span className="text-[8px] font-mono uppercase tracking-[0.4em]">Historical State Reconstruction</span>
         <div className="flex gap-2">
            <div className="w-1 h-1 bg-warning rounded-full animate-pulse" />
            <div className="w-1 h-1 bg-warning rounded-full animate-pulse" style={{ animationDelay: '0.5s' }} />
         </div>
      </div>
    </div>
  );
};
