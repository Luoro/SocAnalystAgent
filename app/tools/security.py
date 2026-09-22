import hashlib


def calculate_sha256(text: str) -> str:
    """
    Calculate the SHA-256 hash of a text.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

import os
import ipaddress

import requests


VIRUSTOTAL_URL = (
    "https://www.virustotal.com/api/v3/ip_addresses"
)

ABUSEIPDB_URL = (
    "https://api.abuseipdb.com/api/v2/check"
)


def check_ip_reputation(
    ip: str
) -> dict:

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise ValueError(
            f"Invalid IP address: {ip}"
        )

    result = {
        "ip": ip,
        "virustotal": None,
        "abuseipdb": None
    }

    # -------------------------
    # VIRUSTOTAL
    # -------------------------

    vt_key = os.getenv(
        "VIRUSTOTAL_API_KEY"
    )

    if vt_key:

        response = requests.get(
            f"{VIRUSTOTAL_URL}/{ip}",
            headers={
                "x-apikey": vt_key
            },
            timeout=10
        )

        if response.ok:

            data = response.json()

            attributes = (
                data
                .get("data", {})
                .get("attributes", {})
            )

            result["virustotal"] = {
                "reputation": attributes.get(
                    "reputation"
                ),
                "country": attributes.get(
                    "country"
                ),
                "asn": attributes.get(
                    "asn"
                ),
                "as_owner": attributes.get(
                    "as_owner"
                ),
                "network": attributes.get(
                    "network"
                ),
                "last_analysis_stats": attributes.get(
                    "last_analysis_stats"
                )
            }

    # -------------------------
    # ABUSEIPDB
    # -------------------------

    abuse_key = os.getenv(
        "ABUSEIPDB_API_KEY"
    )

    if abuse_key:

        response = requests.get(
            ABUSEIPDB_URL,
            headers={
                "Accept": "application/json",
                "Key": abuse_key
            },
            params={
                "ipAddress": ip,
                "maxAgeInDays": 90
            },
            timeout=10
        )

        if response.ok:

            data = response.json()

            result["abuseipdb"] = (
                data.get("data")
            )

    return result

import requests


GOOGLE_DNS_URL = (
    "https://dns.google/resolve"
)


def resolve_domain(
    domain: str
) -> dict:

    result = {
        "domain": domain,
        "a": [],
        "aaaa": [],
        "cname": []
    }

    for record_type in [
        "A",
        "AAAA",
        "CNAME"
    ]:

        response = requests.get(
            GOOGLE_DNS_URL,
            params={
                "name": domain,
                "type": record_type
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        answers = data.get(
            "Answer",
            []
        )

        for answer in answers:

            result[
                record_type.lower()
            ].append(
                answer.get("data")
            )

    return result

import hashlib
import os
from pathlib import Path

import requests


def calculate_file_hash(
    file_path: str,
    algorithm: str = "sha256"
) -> dict:

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    hash_function = hashlib.new(
        algorithm
    )

    with path.open("rb") as file:

        for chunk in iter(
            lambda: file.read(8192),
            b""
        ):
            hash_function.update(chunk)

    file_hash = hash_function.hexdigest()

    result = {
        "file": file_path,
        "algorithm": algorithm,
        "hash": file_hash,
        "virustotal": None
    }

    # -------------------------
    # VIRUSTOTAL LOOKUP
    # -------------------------

    vt_key = os.getenv(
        "VIRUSTOTAL_API_KEY"
    )

    if vt_key:

        response = requests.get(
            f"https://www.virustotal.com/api/v3/files/{file_hash}",
            headers={
                "x-apikey": vt_key
            },
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            attributes = (
                data
                .get("data", {})
                .get("attributes", {})
            )

            result["virustotal"] = {
                "meaningful_name": attributes.get(
                    "meaningful_name"
                ),
                "type_description": attributes.get(
                    "type_description"
                ),
                "last_analysis_stats": attributes.get(
                    "last_analysis_stats"
                ),
                "reputation": attributes.get(
                    "reputation"
                )
            }

        elif response.status_code == 404:

            result["virustotal"] = {
                "found": False
            }

    return result

import os

import requests


MITRE_URL = os.getenv(
    "MITRE_ATTACK_URL",
    "https://raw.githubusercontent.com/"
    "mitre-attack/attack-stix-data/master/"
    "enterprise-attack/"
    "enterprise-attack.json"
)


def search_mitre_technique(
    technique: str
) -> dict:

    response = requests.get(
        MITRE_URL,
        timeout=30
    )

    response.raise_for_status()

    bundle = response.json()

    search = technique.lower()

    results = []

    for obj in bundle.get(
        "objects",
        []
    ):

        if obj.get("type") != "attack-pattern":
            continue

        technique_id = ""

        for ref in obj.get(
            "external_references",
            []
        ):

            if (
                ref.get("source_name")
                == "mitre-attack"
            ):

                technique_id = ref.get(
                    "external_id",
                    ""
                )

        name = obj.get(
            "name",
            ""
        )

        description = obj.get(
            "description",
            ""
        )

        if (
            search in technique_id.lower()
            or search in name.lower()
        ):

            results.append(
                {
                    "technique_id": technique_id,
                    "name": name,
                    "description": description
                }
            )

    return {
        "query": technique,
        "count": len(results),
        "results": results[:10]
    }

from collections import Counter

from scapy.all import rdpcap


def analyze_pcap(
    file_path: str
) -> dict:

    packets = rdpcap(file_path)

    protocols = Counter()
    source_ips = Counter()
    destination_ips = Counter()

    for packet in packets:

        if packet.haslayer("IP"):

            source = packet["IP"].src
            destination = packet["IP"].dst

            source_ips[source] += 1
            destination_ips[destination] += 1

        if packet.haslayer("TCP"):
            protocols["TCP"] += 1

        elif packet.haslayer("UDP"):
            protocols["UDP"] += 1

        elif packet.haslayer("ICMP"):
            protocols["ICMP"] += 1

        else:
            protocols["OTHER"] += 1

    return {
        "packet_count": len(packets),
        "protocols": dict(protocols),
        "top_source_ips": dict(
            source_ips.most_common(10)
        ),
        "top_destination_ips": dict(
            destination_ips.most_common(10)
        )
    }

"""

def search_logs()
def search_splunk()
"""
