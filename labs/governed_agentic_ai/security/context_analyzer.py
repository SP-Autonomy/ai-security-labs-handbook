"""
Context-aware security analysis for agentic AI systems.
Goes beyond static allowlists to understand intent and risk.
"""
import re
from typing import Dict, Any, List
from shared.evidence.logger import append_evidence

class RiskScore:
    """Risk scoring for tool calls"""
    LOW = "low"        # 0-30: Safe operations
    MEDIUM = "medium"  # 31-69: Potentially risky, log and monitor
    HIGH = "high"      # 70-100: Dangerous, should block

class ContextAnalyzer:
    """Analyzes tool calls in context to assess risk"""
    
    def __init__(self):
        self.call_history: Dict[str, List[Dict]] = {}  # run_id -> list of calls
        
        # Suspicious patterns (more nuanced than simple blocking)
        self.suspicious_patterns = {
            # Exfiltration indicators
            "exfiltrat": 40,
            "send.*to.*@": 35,
            "leak": 30,
            "steal": 35,
            "transfer.*external": 40,
            
            # Path traversal indicators
            r"\.\./": 45,
            "/etc/": 50,
            "/root/": 50,
            
            # Code injection indicators
            "eval\(": 50,
            "exec\(": 50,
            "__import__": 45,
            
            # Credential patterns
            "password": 25,
            "api[_-]?key": 30,
            "secret": 25,
            "token": 20,
        }
        
        # Unusual sequences (behavioral anomaly detection)
        self.unusual_sequences = [
            (["search_docs", "search_docs", "search_docs"], 20),  # Repeated searches
            (["read_file", "read_file", "read_file"], 25),        # Mass file reading
            (["write_to_file", "write_to_file"], 30),             # Multiple writes
        ]
    
    def analyze_tool_call(
        self,
        agent_id: str,
        tool_name: str,
        payload: Dict[str, Any],
        run_id: str,
        opa_allowed: bool
    ) -> Dict[str, Any]:
        """
        Analyze a tool call in context and return risk assessment.
        
        Returns:
            {
                "risk_level": "low" | "medium" | "high",
                "risk_score": 0-100,
                "reasons": ["reason1", "reason2"],
                "action": "allow" | "log_and_allow" | "block"
            }
        """
        risk_score = 0
        reasons = []
        
        # Factor 1: OPA basic allowlist
        if not opa_allowed:
            risk_score += 100  # Immediate block
            reasons.append("not_in_agent_allowlist")
            return self._build_result(risk_score, reasons, run_id, agent_id, tool_name)
        
        # Factor 2: Pattern analysis in payload
        payload_str = str(payload).lower()
        for pattern, score in self.suspicious_patterns.items():
            if re.search(pattern, payload_str):
                risk_score += score
                reasons.append(f"suspicious_pattern:{pattern}")
        
        # Factor 3: Call history / behavioral analysis
        self.call_history.setdefault(run_id, [])
        self.call_history[run_id].append({"agent": agent_id, "tool": tool_name})
        
        recent_calls = [c["tool"] for c in self.call_history[run_id][-5:]]  # Last 5 calls
        
        for sequence, score in self.unusual_sequences:
            if self._matches_sequence(recent_calls, sequence):
                risk_score += score
                reasons.append(f"unusual_sequence:{'>'.join(sequence)}")
        
        # Factor 4: Tool-specific risk (side effects)
        if tool_name in ["send_email", "write_to_file", "delete_file"]:
            risk_score += 15  # Side-effect tools inherently riskier
            reasons.append("side_effect_tool")
        
        # Factor 5: Payload size anomaly
        if len(payload_str) > 5000:
            risk_score += 20
            reasons.append("large_payload")
        
        return self._build_result(risk_score, reasons, run_id, agent_id, tool_name)
    
    def _matches_sequence(self, recent_calls: List[str], sequence: List[str]) -> bool:
        """Check if recent calls match a suspicious sequence"""
        if len(recent_calls) < len(sequence):
            return False
        
        for i in range(len(recent_calls) - len(sequence) + 1):
            if recent_calls[i:i+len(sequence)] == sequence:
                return True
        return False
    
    def _build_result(
        self,
        risk_score: int,
        reasons: List[str],
        run_id: str,
        agent_id: str,
        tool_name: str
    ) -> Dict[str, Any]:
        """Build risk assessment result"""
        
        # Determine risk level and action
        if risk_score >= 70:
            risk_level = RiskScore.HIGH
            action = "block"
        elif risk_score >= 31:
            risk_level = RiskScore.MEDIUM
            action = "log_and_allow"
        else:
            risk_level = RiskScore.LOW
            action = "allow"
        
        result = {
            "risk_level": risk_level,
            "risk_score": min(risk_score, 100),  # Cap at 100
            "reasons": reasons,
            "action": action
        }
        
        # Log to evidence
        append_evidence({
            "type": "risk_assessment",
            "run_id": run_id,
            "agent": agent_id,
            "tool": tool_name,
            **result
        })
        
        return result

# Global instance
context_analyzer = ContextAnalyzer()