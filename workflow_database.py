"""
Comprehensive Workflow Database System

This module provides a complete database of all system workflows, agent capabilities,
file relationships, and session continuity for the Autonomous UI Engine.

Features:
- Complete system component catalog
- Agent workflow mapping
- File dependency tracking
- Session continuity framework
- Knowledge graph integration
- Multi-session memory persistence
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import pickle


@dataclass
class FileMetadata:
    """Metadata for a file in the system"""
    path: str
    file_type: str
    purpose: str
    dependencies: List[str] = field(default_factory=list)
    related_agents: List[str] = field(default_factory=list)
    last_modified: str = ""
    size_bytes: int = 0
    checksum: str = ""
    

@dataclass
class AgentCapability:
    """Capability definition for an agent"""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    required_context: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowDefinition:
    """Definition of a workflow in the system"""
    workflow_id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    required_agents: List[str]
    input_requirements: Dict[str, Any]
    output_format: Dict[str, Any]
    estimated_time: float = 0.0
    success_rate: float = 0.0


@dataclass
class SessionMemory:
    """Memory structure for session continuity"""
    session_id: str
    timestamp: str
    context_snapshot: Dict[str, Any]
    agent_states: Dict[str, Any]
    workflow_progress: Dict[str, float]
    learned_patterns: List[str] = field(default_factory=list)


class WorkflowDatabase:
    """
    Comprehensive database for system workflows, agents, and files.
    
    This class maintains a complete catalog of all system components
    and their relationships, enabling intelligent workflow planning,
    session continuity, and knowledge preservation.
    """
    
    def __init__(self, base_path: str = None):
        """Initialize the workflow database"""
        self.base_path = base_path or os.getcwd()
        self.files: Dict[str, FileMetadata] = {}
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.sessions: Dict[str, SessionMemory] = {}
        self.knowledge_graph: Dict[str, Set[str]] = {}
        
        # System component catalog
        self.component_catalog = {
            'context_engine': {
                'modules': [
                    'context_engine.py', 'node.py', 'edge.py', 'vector_space.py',
                    'network_engine.py', 'embedding_generator.py', 'advanced_cache.py',
                    'performance_monitor.py', 'advanced_search.py', 'advanced_reasoning.py',
                    'memory_consolidation.py'
                ],
                'purpose': 'Graph-based context management with vector embeddings',
                'capabilities': ['semantic_search', 'clustering', 'caching', 'reasoning']
            },
            'agents': {
                'modules': [
                    'base_agent.py', 'concrete_agents.py', 'enhanced_agents.py',
                    'enhanced_concrete_agents.py', 'self_enhancing_agent.py',
                    'self_enhancing_concrete_agents.py'
                ],
                'purpose': 'AI agent system with self-enhancement capabilities',
                'capabilities': ['code_generation', 'ui_design', 'reasoning', 'self_learning']
            },
            'integrations': {
                'modules': [
                    'databases.py', 'message_queues.py', 'cloud_platforms.py',
                    'web_frameworks.py'
                ],
                'purpose': 'External system integrations',
                'capabilities': ['database_ops', 'messaging', 'cloud_deployment', 'web_frameworks']
            },
            'nlp_system': {
                'modules': ['nlp_ui_interpreter.py'],
                'purpose': 'Natural language UI interpretation',
                'capabilities': ['ui_parsing', 'component_detection', 'layout_analysis', 'llm_integration']
            }
        }
        
        print(f"✓ Workflow Database initialized at {self.base_path}")
    
    def scan_repository(self) -> Dict[str, Any]:
        """
        Scan the entire repository and catalog all files.
        
        Returns:
            Dictionary with scan results and statistics
        """
        print("\n📂 Scanning repository...")
        
        stats = {
            'total_files': 0,
            'python_files': 0,
            'markdown_files': 0,
            'config_files': 0,
            'agent_files': 0,
            'total_size': 0
        }
        
        # Scan all files
        for root, dirs, files in os.walk(self.base_path):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.base_path)
                
                # Get file info
                try:
                    file_stat = os.stat(file_path)
                    file_size = file_stat.st_size
                    file_mtime = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                    
                    # Calculate checksum for content tracking
                    checksum = self._calculate_checksum(file_path)
                    
                    # Determine file type and purpose
                    file_type, purpose = self._classify_file(rel_path, file)
                    
                    # Create file metadata
                    metadata = FileMetadata(
                        path=rel_path,
                        file_type=file_type,
                        purpose=purpose,
                        last_modified=file_mtime,
                        size_bytes=file_size,
                        checksum=checksum
                    )
                    
                    self.files[rel_path] = metadata
                    
                    # Update statistics
                    stats['total_files'] += 1
                    stats['total_size'] += file_size
                    
                    if file.endswith('.py'):
                        stats['python_files'] += 1
                        if 'agent' in file.lower():
                            stats['agent_files'] += 1
                    elif file.endswith('.md'):
                        stats['markdown_files'] += 1
                    elif file.endswith(('.json', '.yaml', '.yml', '.toml', '.ini')):
                        stats['config_files'] += 1
                        
                except Exception as e:
                    print(f"  ⚠ Error scanning {rel_path}: {e}")
        
        print(f"✓ Repository scan complete!")
        print(f"  Total files: {stats['total_files']}")
        print(f"  Python files: {stats['python_files']}")
        print(f"  Markdown docs: {stats['markdown_files']}")
        print(f"  Agent files: {stats['agent_files']}")
        print(f"  Total size: {stats['total_size'] / (1024*1024):.2f} MB")
        
        return stats
    
    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA-256 checksum for a file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()[:16]
        except:
            return ""
    
    def _classify_file(self, rel_path: str, filename: str) -> Tuple[str, str]:
        """Classify file type and determine its purpose"""
        path_lower = rel_path.lower()
        file_lower = filename.lower()
        
        # Python files
        if filename.endswith('.py'):
            if 'agent' in file_lower:
                if 'self_enhancing' in file_lower:
                    return 'agent', 'Self-enhancing agent with learning capabilities'
                elif 'enhanced' in file_lower:
                    return 'agent', 'Enhanced agent with network features'
                elif 'base' in file_lower:
                    return 'agent', 'Base agent class/interface'
                else:
                    return 'agent', 'Agent implementation'
            elif 'context' in path_lower or 'context' in file_lower:
                return 'context_engine', 'Context management component'
            elif 'nlp' in file_lower or 'interpret' in file_lower:
                return 'nlp', 'Natural language processing component'
            elif 'test' in file_lower:
                return 'test', 'Test suite'
            elif 'demo' in file_lower or 'example' in file_lower:
                return 'demo', 'Example/demo script'
            elif 'integration' in path_lower:
                return 'integration', 'External system integration'
            else:
                return 'python', 'Python module'
        
        # Markdown files
        elif filename.endswith('.md'):
            if 'readme' in file_lower:
                return 'documentation', 'Project documentation (README)'
            elif 'architecture' in file_lower:
                return 'documentation', 'Architecture documentation'
            elif 'guide' in file_lower or 'tutorial' in file_lower:
                return 'documentation', 'User guide/tutorial'
            elif 'summary' in file_lower or 'status' in file_lower:
                return 'documentation', 'Project summary/status'
            elif '.github/agents' in path_lower:
                return 'agent_config', 'Agent configuration/instructions'
            else:
                return 'documentation', 'Documentation file'
        
        # Configuration files
        elif filename.endswith(('.json', '.yaml', '.yml', '.toml', '.ini')):
            if 'agent' in file_lower:
                return 'agent_config', 'Agent configuration'
            else:
                return 'config', 'Configuration file'
        
        # Requirements/dependencies
        elif filename in ['requirements.txt', 'setup.py', 'pyproject.toml']:
            return 'dependency', 'Dependency specification'
        
        # Other
        else:
            return 'other', 'Other file type'
    
    def register_agent(self, agent_name: str, agent_info: Dict[str, Any]):
        """Register an agent and its capabilities"""
        self.agents[agent_name] = agent_info
        print(f"✓ Registered agent: {agent_name}")
    
    def define_workflow(self, workflow: WorkflowDefinition):
        """Define a new workflow"""
        self.workflows[workflow.workflow_id] = workflow
        print(f"✓ Defined workflow: {workflow.name}")
    
    def save_session(self, session: SessionMemory):
        """Save session memory for continuity"""
        self.sessions[session.session_id] = session
        print(f"✓ Saved session: {session.session_id}")
    
    def restore_session(self, session_id: str) -> Optional[SessionMemory]:
        """Restore a previous session"""
        return self.sessions.get(session_id)
    
    def build_knowledge_graph(self):
        """Build knowledge graph of system relationships"""
        print("\n🔗 Building knowledge graph...")
        
        # Connect files to components
        for file_path, metadata in self.files.items():
            if metadata.file_type in ['agent', 'context_engine', 'integration', 'nlp']:
                component_type = metadata.file_type
                if component_type not in self.knowledge_graph:
                    self.knowledge_graph[component_type] = set()
                self.knowledge_graph[component_type].add(file_path)
        
        # Connect agents to workflows
        for workflow_id, workflow in self.workflows.items():
            for agent_name in workflow.required_agents:
                edge_key = f"workflow:{workflow_id}->agent:{agent_name}"
                if 'workflow_dependencies' not in self.knowledge_graph:
                    self.knowledge_graph['workflow_dependencies'] = set()
                self.knowledge_graph['workflow_dependencies'].add(edge_key)
        
        print(f"✓ Knowledge graph built with {len(self.knowledge_graph)} node types")
    
    def get_agent_workflows(self, agent_name: str) -> List[WorkflowDefinition]:
        """Get all workflows that use a specific agent"""
        workflows = []
        for workflow in self.workflows.values():
            if agent_name in workflow.required_agents:
                workflows.append(workflow)
        return workflows
    
    def get_related_files(self, file_path: str, max_depth: int = 2) -> List[str]:
        """Get files related to a given file through the knowledge graph"""
        if file_path not in self.files:
            return []
        
        metadata = self.files[file_path]
        related = set()
        
        # Add direct dependencies
        related.update(metadata.dependencies)
        
        # Add files of same type
        for path, meta in self.files.items():
            if meta.file_type == metadata.file_type and path != file_path:
                related.add(path)
        
        return list(related)
    
    def export_database(self, output_path: str = "workflow_database.json"):
        """Export database to JSON file"""
        data = {
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'base_path': self.base_path,
                'version': '1.0.0'
            },
            'files': {path: asdict(meta) for path, meta in self.files.items()},
            'agents': self.agents,
            'workflows': {wid: asdict(wf) for wid, wf in self.workflows.items()},
            'component_catalog': self.component_catalog,
            'knowledge_graph': {k: list(v) for k, v in self.knowledge_graph.items()}
        }
        
        output_file = os.path.join(self.base_path, output_path)
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Database exported to {output_path}")
        print(f"  Size: {os.path.getsize(output_file) / 1024:.2f} KB")
        return output_file
    
    def import_database(self, input_path: str):
        """Import database from JSON file"""
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        # Restore files
        self.files = {
            path: FileMetadata(**meta) 
            for path, meta in data.get('files', {}).items()
        }
        
        # Restore agents
        self.agents = data.get('agents', {})
        
        # Restore workflows
        self.workflows = {
            wid: WorkflowDefinition(**wf)
            for wid, wf in data.get('workflows', {}).items()
        }
        
        # Restore component catalog
        self.component_catalog = data.get('component_catalog', {})
        
        # Restore knowledge graph
        self.knowledge_graph = {
            k: set(v) for k, v in data.get('knowledge_graph', {}).items()
        }
        
        print(f"✓ Database imported from {input_path}")
    
    def generate_report(self) -> str:
        """Generate a comprehensive report of the system"""
        report = []
        report.append("=" * 80)
        report.append("AUTONOMOUS UI ENGINE - WORKFLOW DATABASE REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Base Path: {self.base_path}\n")
        
        # Files summary
        report.append("\n📂 FILES SUMMARY")
        report.append("-" * 80)
        report.append(f"Total Files: {len(self.files)}")
        
        file_types = {}
        for meta in self.files.values():
            file_types[meta.file_type] = file_types.get(meta.file_type, 0) + 1
        
        for ftype, count in sorted(file_types.items(), key=lambda x: -x[1]):
            report.append(f"  {ftype:20s}: {count:4d} files")
        
        # Agents summary
        report.append("\n🤖 AGENTS SUMMARY")
        report.append("-" * 80)
        report.append(f"Total Agents: {len(self.agents)}")
        for agent_name, agent_info in self.agents.items():
            report.append(f"  {agent_name}: {agent_info.get('description', 'No description')}")
        
        # Workflows summary
        report.append("\n⚙️  WORKFLOWS SUMMARY")
        report.append("-" * 80)
        report.append(f"Total Workflows: {len(self.workflows)}")
        for workflow in self.workflows.values():
            report.append(f"  {workflow.name}")
            report.append(f"    - Steps: {len(workflow.steps)}")
            report.append(f"    - Agents: {', '.join(workflow.required_agents)}")
        
        # Components summary
        report.append("\n📦 COMPONENTS SUMMARY")
        report.append("-" * 80)
        for comp_name, comp_info in self.component_catalog.items():
            report.append(f"  {comp_name}:")
            report.append(f"    Purpose: {comp_info['purpose']}")
            report.append(f"    Modules: {len(comp_info['modules'])}")
            report.append(f"    Capabilities: {', '.join(comp_info['capabilities'])}")
        
        # Knowledge graph summary
        report.append("\n🔗 KNOWLEDGE GRAPH SUMMARY")
        report.append("-" * 80)
        for node_type, nodes in self.knowledge_graph.items():
            report.append(f"  {node_type}: {len(nodes)} connections")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)


# Initialize default workflows
def initialize_default_workflows(db: WorkflowDatabase):
    """Initialize default workflows for the system"""
    
    # Workflow 1: UI Generation from Natural Language
    ui_generation_workflow = WorkflowDefinition(
        workflow_id="ui_generation",
        name="UI Generation from Natural Language",
        description="Convert natural language descriptions to complete UI implementations",
        steps=[
            {'step': 1, 'action': 'Parse NLP input', 'agent': 'nlp_interpreter'},
            {'step': 2, 'action': 'Design UI structure', 'agent': 'ui_designer'},
            {'step': 3, 'action': 'Generate code', 'agent': 'codex'},
            {'step': 4, 'action': 'Validate & enhance', 'agent': 'reasoning'}
        ],
        required_agents=['nlp_interpreter', 'ui_designer', 'codex', 'reasoning'],
        input_requirements={'text_description': 'string', 'preferences': 'dict'},
        output_format={'html': 'string', 'css': 'string', 'js': 'string'},
        estimated_time=30.0,
        success_rate=0.92
    )
    db.define_workflow(ui_generation_workflow)
    
    # Workflow 2: Code Enhancement
    code_enhancement_workflow = WorkflowDefinition(
        workflow_id="code_enhancement",
        name="Code Enhancement & Optimization",
        description="Analyze and enhance existing code with best practices",
        steps=[
            {'step': 1, 'action': 'Analyze code', 'agent': 'codex'},
            {'step': 2, 'action': 'Identify improvements', 'agent': 'reasoning'},
            {'step': 3, 'action': 'Apply enhancements', 'agent': 'codex'},
            {'step': 4, 'action': 'Validate changes', 'agent': 'reasoning'}
        ],
        required_agents=['codex', 'reasoning'],
        input_requirements={'code': 'string', 'language': 'string'},
        output_format={'enhanced_code': 'string', 'changes': 'list'},
        estimated_time=20.0,
        success_rate=0.88
    )
    db.define_workflow(code_enhancement_workflow)
    
    # Workflow 3: Multi-Agent Collaboration
    collaboration_workflow = WorkflowDefinition(
        workflow_id="multi_agent_collaboration",
        name="Multi-Agent Problem Solving",
        description="Coordinate multiple agents to solve complex problems",
        steps=[
            {'step': 1, 'action': 'Decompose problem', 'agent': 'reasoning'},
            {'step': 2, 'action': 'Assign subtasks', 'agent': 'reasoning'},
            {'step': 3, 'action': 'Execute in parallel', 'agent': 'all'},
            {'step': 4, 'action': 'Integrate results', 'agent': 'reasoning'}
        ],
        required_agents=['codex', 'ui_designer', 'reasoning'],
        input_requirements={'problem_description': 'string'},
        output_format={'solution': 'dict', 'metadata': 'dict'},
        estimated_time=45.0,
        success_rate=0.85
    )
    db.define_workflow(collaboration_workflow)


# Demo usage
if __name__ == "__main__":
    print("🚀 Initializing Workflow Database System\n")
    
    # Create database
    db = WorkflowDatabase()
    
    # Scan repository
    stats = db.scan_repository()
    
    # Register agents
    db.register_agent('codex', {
        'description': 'Code generation and analysis agent',
        'capabilities': ['code_generation', 'code_review', 'refactoring']
    })
    
    db.register_agent('ui_designer', {
        'description': 'UI design and generation agent',
        'capabilities': ['ui_design', 'component_generation', 'styling']
    })
    
    db.register_agent('reasoning', {
        'description': 'Logical reasoning and planning agent',
        'capabilities': ['problem_decomposition', 'planning', 'decision_making']
    })
    
    # Initialize default workflows
    initialize_default_workflows(db)
    
    # Build knowledge graph
    db.build_knowledge_graph()
    
    # Generate and display report
    report = db.generate_report()
    print("\n" + report)
    
    # Export database
    db.export_database()
    
    print("\n✅ Workflow Database System initialized successfully!")
