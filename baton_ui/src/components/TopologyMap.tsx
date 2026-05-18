import React, { useMemo } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  Handle, 
  Position,
  Edge,
  Node,
  BackgroundVariant
} from 'reactflow';
import 'reactflow/dist/style.css';
import { motion } from 'framer-motion';

const CustomNode = ({ data }: any) => (
  <motion.div 
    initial={{ scale: 0.9, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    className={`px-6 py-3 rounded border backdrop-blur-xl transition-all duration-700 relative overflow-hidden group ${
    data.active ? 'bg-accent/10 border-accent/50 shadow-[0_0_30px_rgba(0,210,255,0.1)]' : 'bg-black/60 border-white/5 opacity-50'
  }`}>
    {/* Active Scanner Line */}
    {data.active && (
      <motion.div 
        className="absolute inset-0 bg-gradient-to-r from-transparent via-accent/5 to-transparent w-full h-full"
        animate={{ x: ['-100%', '100%'] }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
      />
    )}
    
    <Handle type="target" position={Position.Left} className="!w-1.5 !h-1.5 !bg-accent !border-none !rounded-full shadow-[0_0_5px_#00d2ff]" />
    
    <div className="flex flex-col gap-1 relative z-10">
      <div className="flex items-center gap-2">
         <div className={`w-1 h-1 rounded-full ${
           data.type === 'audit' ? 'bg-warning shadow-[0_0_5px_#ffaa00]' : 
           data.type === 'orchestrator' ? 'bg-accent shadow-[0_0_5px_#00d2ff]' : 'bg-white/20'
         }`} />
         <span className="telemetry-text tracking-[0.2em]">{data.type}</span>
      </div>
      <span className="text-sm font-bold text-white/90 tracking-tight group-hover:text-accent transition-colors duration-300">{data.label}</span>
      
      {data.active && (
         <div className="flex gap-1 mt-1">
            <div className="w-12 h-0.5 bg-accent/20 rounded-full overflow-hidden">
               <motion.div 
                 className="h-full bg-accent"
                 animate={{ width: ['0%', '100%'] }}
                 transition={{ duration: 1.5, repeat: Infinity }}
               />
            </div>
         </div>
      )}
    </div>
    
    <Handle type="source" position={Position.Right} className="!w-1.5 !h-1.5 !bg-accent !border-none !rounded-full shadow-[0_0_5px_#00d2ff]" />
  </motion.div>
);

const nodeTypes = {
  custom: CustomNode,
};

export const TopologyMap: React.FC = () => {
  const initialNodes: Node[] = [
    { id: 'on_change', type: 'custom', position: { x: 0, y: 150 }, data: { label: 'on_change', type: 'event', active: true } },
    { id: 'router', type: 'custom', position: { x: 250, y: 50 }, data: { label: 'router_graph.py', type: 'orchestrator', active: true } },
    { id: 'orchestrator', type: 'custom', position: { x: 250, y: 250 }, data: { label: 'event_orchestrator.py', type: 'service', active: true } },
    { id: 'stability', type: 'custom', position: { x: 550, y: 0 }, data: { label: 'vst3_stability_audit', type: 'audit', active: true } },
    { id: 'pipeline', type: 'custom', position: { x: 550, y: 150 }, data: { label: 'pipeline.py', type: 'retrieval', active: false } },
    { id: 'continuity', type: 'custom', position: { x: 550, y: 300 }, data: { label: 'validate_continuity.py', type: 'audit', active: false } },
    { id: 'query', type: 'custom', position: { x: 850, y: 150 }, data: { label: 'retrieval_query', type: 'task', active: false } },
    { id: 'suggestion', type: 'custom', position: { x: 1150, y: 150 }, data: { label: 'suggestion_delta', type: 'proposal', active: false } },
  ];

  const initialEdges: Edge[] = [
    { id: 'e1', source: 'on_change', target: 'router', animated: true, style: { stroke: '#00d2ff', strokeWidth: 2 } },
    { id: 'e2', source: 'on_change', target: 'orchestrator', animated: true, style: { stroke: '#00d2ff', strokeWidth: 2 } },
    { id: 'e3', source: 'router', target: 'stability', animated: true, style: { stroke: '#ffaa00', strokeWidth: 2 } },
    { id: 'e4', source: 'router', target: 'pipeline', animated: false, style: { stroke: 'rgba(255,255,255,0.05)', strokeWidth: 1 } },
    { id: 'e5', source: 'orchestrator', target: 'pipeline', animated: false, style: { stroke: 'rgba(255,255,255,0.05)', strokeWidth: 1 } },
    { id: 'e6', source: 'orchestrator', target: 'continuity', animated: false, style: { stroke: 'rgba(255,255,255,0.05)', strokeWidth: 1 } },
    { id: 'e7', source: 'pipeline', target: 'query', animated: false, style: { stroke: 'rgba(255,255,255,0.05)', strokeWidth: 1 } },
    { id: 'e8', source: 'query', target: 'suggestion', animated: false, style: { stroke: 'rgba(255,255,255,0.05)', strokeWidth: 1 } },
  ];

  return (
    <div className="w-full h-full bg-obsidian overflow-hidden relative">
      <div className="absolute top-8 left-8 z-10 flex flex-col gap-1 pointer-events-none">
        <h3 className="cinematic-heading text-lg">Topology Map</h3>
        <span className="telemetry-text">Realtime Propagation Substrate</span>
      </div>
      
      <ReactFlow
        nodes={initialNodes}
        edges={initialEdges}
        nodeTypes={nodeTypes}
        fitView
        className="bg-transparent"
        minZoom={0.2}
        maxZoom={1.5}
      >
        <Background variant={BackgroundVariant.Dots} color="rgba(255,255,255,0.03)" gap={40} size={1} />
        <Controls />
      </ReactFlow>

      {/* Cinematic Overlays */}
      <div className="absolute inset-0 pointer-events-none border-[20px] border-obsidian/50 shadow-[inset_0_0_100px_rgba(0,0,0,0.8)]" />
      <div className="absolute bottom-8 left-8 z-10 flex items-center gap-4">
         <div className="flex flex-col">
            <span className="telemetry-text">Active Clusters</span>
            <span className="text-xl font-mono font-bold text-accent">04</span>
         </div>
         <div className="w-px h-8 bg-white/10" />
         <div className="flex flex-col">
            <span className="telemetry-text">Edge Density</span>
            <span className="text-xl font-mono font-bold text-accent">LOW</span>
         </div>
      </div>
    </div>
  );
};
