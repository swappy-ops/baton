import React from 'react';
import Editor from '@monaco-editor/react';

export const WorkspaceSurface: React.FC = () => {
  return (
    <div className="glass-panel h-full relative overflow-hidden flex flex-col">
      <div className="flex items-center gap-2 px-4 py-2 bg-black/20 border-b border-white/5">
        <div className="flex gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-red-500/50" />
          <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/50" />
          <div className="w-2.5 h-2.5 rounded-full bg-green-500/50" />
        </div>
        <span className="text-[10px] font-mono text-white/40 ml-4">d:/AIWORKFLOW/projskep/graphs/router_graph.py</span>
      </div>
      
      <div className="flex-grow relative">
        <Editor
          height="100%"
          defaultLanguage="python"
          theme="vs-dark"
          value={`# ProjSkep Orchestration Graph
import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: List[str]
    task_type: str
    
def build_router_graph():
    workflow = StateGraph(AgentState)
    # ... logic continues
`}
          options={{
            minimap: { enabled: false },
            fontSize: 12,
            backgroundColor: 'transparent',
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            readOnly: true,
            padding: { top: 20 }
          }}
        />
        
        {/* Orchestration Overlays */}
        <div className="absolute top-4 right-4 z-10 flex flex-col gap-2">
            <div className="bg-accent/10 border border-accent/40 backdrop-blur-md p-2 rounded flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-accent animate-ping" />
                <span className="text-[10px] font-bold text-accent uppercase font-mono">Trace Active</span>
            </div>
            <div className="bg-warning/10 border border-warning/40 backdrop-blur-md p-2 rounded flex flex-col gap-1">
                <span className="text-[9px] font-bold text-warning uppercase">Forensic Hint</span>
                <span className="text-[10px] text-white/80">Potential Terminology Drift: 'Neural Observatory'</span>
            </div>
        </div>
      </div>
      
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-10 flex gap-4">
          <div className="px-3 py-1.5 bg-black/80 border border-white/10 rounded-full flex items-center gap-2 shadow-2xl">
              <div className="w-1.5 h-1.5 rounded-full bg-accent" />
              <span className="text-[10px] text-white/60 font-mono">router_node -> retrieval_node</span>
          </div>
      </div>
    </div>
  );
};
