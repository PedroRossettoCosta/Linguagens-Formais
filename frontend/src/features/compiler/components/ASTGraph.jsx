import { useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
} from '@xyflow/react';
import dagre from 'dagre';
import '@xyflow/react/dist/style.css';

const NODE_WIDTH = 150;
const NODE_HEIGHT = 40;

const nodeColors = {
  PROGRAM: '#ff3c00',       // Ritual
  SETUP_BLOCK: '#ff5e00',   // Exordium
  LOOP_BLOCK: '#ff5e00',    // Inferna
  VAR_DECL: '#7efff5',      // Sanguis / Sanguis_Fluens
  ASSIGN: '#7efff5',
  IF_STMT: '#ffd700',       // Si
  WHILE_STMT: '#ffd700',    // Tormentum
  FOR_STMT: '#ffd700',      // Iterum
  BINOP: '#c084fc',
  LOGOP: '#c084fc',
  FUNC_CALL: '#32ff7e',
  PIN_MODE: '#32ff7e',      // Habitus
  DIGITAL_WRITE: '#32ff7e', // Incantare
  DIGITAL_READ: '#32ff7e',  // Sentire
  ANALOG_READ: '#32ff7e',   // Anima
  DELAY: '#32ff7e',         // Mora
  PRINT: '#a78bfa',         // Revelare (Roxo Místico)
  RETURN: '#f472b6',        // Redditum
  INT_LIT: '#94a3b8',
  FLOAT_LIT: '#94a3b8',
  STRING_LIT: '#94a3b8',    // Textos entre aspas
  VAR: '#e0e0e0',
  CONST_STATE: '#fbbf24',   // Ignis / Tenebrae
  CONDITION: '#ffd700',
  TEMPERARE_CRONOS: '#32ff7e',
  SIGNARE_CAOS: '#32ff7e',
  SACRATUM: '#32ff7e',
  INANIS: '#32ff7e',
  AEVUM: '#32ff7e',
  VERBUM_AEVUM: '#32ff7e',
};

function getNodeColor(type) {
  return nodeColors[type] || '#e0e0e0';
}

function buildGraph(ast) {
  const nodes = [];
  const edges = [];
  let id = 0;

  function walk(node, parentId) {
    if (!node) return;
    const currentId = `node-${id++}`;
    const type = node.type || 'LITERAL';
    const label = node.label || '';
    const color = getNodeColor(type);

    nodes.push({
      id: currentId,
      data: { label },
      style: {
        background: '#1e1e1e',
        color: color,
        border: `2px solid ${color}`,
        borderRadius: '8px',
        padding: '8px 12px',
        fontSize: '12px',
        fontFamily: "'Fira Code', monospace",
        fontWeight: 600,
        textAlign: 'center',
        whiteSpace: 'pre-line',
        minWidth: '80px',
      },
      position: { x: 0, y: 0 },
    });

    if (parentId != null) {
      edges.push({
        id: `edge-${parentId}-${currentId}`,
        source: parentId,
        target: currentId,
        style: { stroke: '#555', strokeWidth: 2 },
        type: 'smoothstep',
      });
    }

    const children = node.children || [];
    children.forEach((child) => walk(child, currentId));
  }

  walk(ast, null);
  return { nodes, edges };
}

function layoutGraph(nodes, edges) {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: 'TB', nodesep: 50, ranksep: 70 });

  nodes.forEach((node) => {
    g.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  return nodes.map((node) => {
    const pos = g.node(node.id);
    return {
      ...node,
      position: {
        x: pos.x - NODE_WIDTH / 2,
        y: pos.y - NODE_HEIGHT / 2,
      },
    };
  });
}

export default function ASTGraph({ ast }) {
  const { nodes, edges } = useMemo(() => {
    if (!ast) return { nodes: [], edges: [] };

    let parsed = ast;
    if (typeof ast === 'string') {
      try {
        parsed = JSON.parse(ast);
      } catch {
        return { nodes: [], edges: [] };
      }
    }

    const graph = buildGraph(parsed);
    const laidOut = layoutGraph(graph.nodes, graph.edges);
    return { nodes: laidOut, edges: graph.edges };
  }, [ast]);

  if (!ast) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500 text-sm">
        Compile o ritual para visualizar a AST
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: '100%', minHeight: '400px' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        proOptions={{ hideAttribution: true }}
        style={{ background: '#161616' }}
        panActivationKeyCode={null}
        deleteKeyCode={null}
        selectionKeyCode={null}
        multiSelectionKeyCode={null}
        zoomActivationKeyCode={null}
      >
        <Background color="#333" gap={20} size={1} />
        <Controls
          style={{
            button: { backgroundColor: '#1e1e1e', color: '#e0e0e0', border: '1px solid #555' },
          }}
        />
      </ReactFlow>
    </div>
  );
}
