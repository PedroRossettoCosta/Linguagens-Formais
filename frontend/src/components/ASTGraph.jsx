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
  BINOP: '#c084fc',
  FUNC_CALL: '#32ff7e',
  PIN_MODE: '#32ff7e',      // Habitus
  DIGITAL_WRITE: '#32ff7e', // Incantare
  DIGITAL_READ: '#32ff7e',  // Sentire
  ANALOG_WRITE: '#32ff7e',  // Fluxus
  ANALOG_READ: '#32ff7e',   // Percipere
  DELAY: '#32ff7e',         // Mora
  PRINT: '#a78bfa',         // NOVO: Revelare (Roxo Místico)
  RETURN: '#f472b6',        // Redditum
  INT_LIT: '#94a3b8',
  FLOAT_LIT: '#94a3b8',
  STRING_LIT: '#94a3b8',    // NOVO: Textos entre aspas
  VAR: '#e0e0e0',
  CONST_STATE: '#fbbf24',   // Ignis / Tenebrae
  CONDITION: '#ffd700',
};

function getNodeColor(type) {
  return nodeColors[type] || '#e0e0e0';
}

// Mapeamento reverso: nomes genéricos/C++ → nomes da linguagem infernal
const typeToInfernal = {
  int: 'Sanguis',
  float: 'Sanguis_Fluens',
  HIGH: 'Ignis',
  LOW: 'Tenebrae',
};

function getLabel(node) {
  if (!Array.isArray(node)) return String(node);
  const type = node[0];
  switch (type) {
    case 'PROGRAM':
      return 'Ritual';
    case 'SETUP_BLOCK':
      return 'Exordium()';
    case 'LOOP_BLOCK':
      return 'Inferna()';
    case 'VAR_DECL': {
      const tipoInfernal = typeToInfernal[node[1]] || node[1];
      return `${tipoInfernal}\n${node[2]}`;
    }
    case 'ASSIGN':
      return `${node[1]} =`;
    case 'IF_STMT':
      return 'Si';
    case 'WHILE_STMT':
      return 'Tormentum';
    case 'BINOP':
      return `( ${node[1]} )`;
    case 'FUNC_CALL':
      return `${node[1]}`;
    case 'PIN_MODE':
      return 'Habitus';
    case 'DIGITAL_WRITE':
      return 'Incantare';
    case 'DIGITAL_READ':
      return 'Sentire';
    case 'ANALOG_WRITE':
      return 'Fluxus';
    case 'ANALOG_READ':
      return 'Percipere';
    case 'DELAY':
      return 'Mora';
    case 'PRINT':
      return 'Revelare';
    case 'RETURN':
      return 'Redditum';
    case 'INT_LIT':
      return `${node[1]}`;
    case 'FLOAT_LIT':
      return `${node[1]}`;
    case 'STRING_LIT':
      return `"${node[1]}"`;
    case 'VAR':
      return `${node[1]}`;
    case 'CONST_STATE': {
      const valInfernal = typeToInfernal[node[1]] || node[1];
      return valInfernal;
    }
    case 'CONDITION':
      return `( ${node[1]} )`;
    default:
      return type;
  }
}

function getChildren(node) {
  if (!Array.isArray(node)) return [];
  const type = node[0];
  switch (type) {
    case 'PROGRAM':
      return Array.isArray(node[1]) ? node[1] : [];
    case 'SETUP_BLOCK':
    case 'LOOP_BLOCK':
      return Array.isArray(node[1]) ? node[1] : [];
    case 'VAR_DECL':
      return node[3] ? [node[3]] : [];
    case 'ASSIGN':
      return node[2] ? [node[2]] : [];
    case 'IF_STMT':
      return [node[1], ...(Array.isArray(node[2]) ? node[2] : [])];
    case 'WHILE_STMT':
      return [node[1], ...(Array.isArray(node[2]) ? node[2] : [])];
    case 'BINOP':
    case 'CONDITION':
      return [node[2], node[3]].filter(Boolean);
    case 'FUNC_CALL':
      return Array.isArray(node[2]) ? node[2] : [];
    case 'PIN_MODE':
    case 'DIGITAL_WRITE':
    case 'ANALOG_WRITE':
      return [node[1], node[2]].filter(Boolean);
    case 'DIGITAL_READ':
    case 'ANALOG_READ':
      return node[1] ? [node[1]] : [];
    case 'DELAY':
    case 'PRINT':
    case 'RETURN':
      return node[1] ? [node[1]] : [];
    default:
      return node.slice(1).filter((c) => Array.isArray(c));
  }
}

function buildGraph(ast) {
  const nodes = [];
  const edges = [];
  let id = 0;

  function walk(node, parentId) {
    if (node == null) return;
    const currentId = `node-${id++}`;
    const type = Array.isArray(node) ? node[0] : null;
    const label = getLabel(node);
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

    const children = getChildren(node);
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