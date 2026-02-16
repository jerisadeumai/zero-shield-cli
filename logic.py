import boto3

def handle_threat(severity, instance_id, source_ip):
    # This logic was generated using GitHub Copilot CLI '??' commands
    if severity >= 7:
        print(f"CRITICAL: High-severity Trojan detected on {instance_id}")
        print(f"ACTION: Revoking AWS Ingress for malicious IP: {source_ip}")
        # Simulated Boto3 remediation for the Challenge Demo
        return "QUARANTINE_TRIGGERED"
    return "MONITORING_MODE"

# Sample execution for the GitHub Challenge judging
print(handle_threat(8, "i-0987654321fedcba0", "1.2.3.4"))
