from .security import calculate_sha256
from .security import calculate_file_hash
from .security import check_ip_reputation
from .security import resolve_domain
from .security import analyze_pcap
from .security import search_mitre_technique

TOOLS = {
    "calculate_sha256": {
        "function": calculate_sha256,
        "description": "Calculate the SHA-256 hash of a text.",
    },
    "calculate_file_hash": {
        "function": calculate_file_hash
    },

    "check_ip_reputation": {
        "function": check_ip_reputation
    },

    "resolve_domain": {
        "function": resolve_domain
    },

    "analyze_pcap": {
        "function": analyze_pcap
    },

    "search_mitre_technique": {
        "function": search_mitre_technique
    }
}
