# Monitoring Guide

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Not Production Ready

**Last Updated:** March 17, 2026  
**Version:** v2.0.0-dev

## Overview

This guide covers operational monitoring for Zero-Shield CLI, including session file management, Knowledge Graph maintenance, performance metrics, and log analysis.

---

## Session File Management

### Session State Files

Zero-Shield maintains two encrypted session files:

1. **session_state.json** - Volatile session metadata
   - Active resource IDs
   - Quota maps
   - Cooldown timers
   - Last action timestamps

2. **session_kg.json** - Persistent Knowledge Graph
   - Audited resource cache
   - Security group rules
   - VPC subnet mappings
   - IAM policy summaries

### File Locations

**CloudShell:**
```bash
/home/cloudshell-user/zero-shield-cli/session_state.json
/home/cloudshell-user/zero-shield-cli/session_kg.json
```

**Local/EC2:**
```bash
./session_state.json
./session_kg.json
```

### Monitoring Session Files

```bash
# Check file existence and permissions
ls -la session_*.json

# Expected output:
# -rw------- 1 user user 1234 Mar 15 10:30 session_state.json
# -rw------- 1 user user 5678 Mar 15 10:30 session_kg.json

# Check file sizes
du -h session_*.json

# Monitor file growth over time
watch -n 60 'ls -lh session_*.json'
```

### File Size Thresholds

| File | Normal Size | Warning Threshold | Action Required |
|------|-------------|-------------------|-----------------|
| session_state.json | < 10 KB | > 50 KB | Review and prune |
| session_kg.json | < 100 KB | > 1 MB | Knowledge Graph cleanup |

---

## Knowledge Graph Maintenance

### KG Health Checks

```bash
# Check KG file integrity
python3 -c "
import json
with open('session_kg.json', 'r') as f:
    kg = json.load(f)
    print(f'KG entries: {len(kg)}')
    print(f'KG size: {len(json.dumps(kg))} bytes')
"
```

### KG Pruning Strategy

**When to Prune:**
- KG file exceeds 1 MB
- Contains > 1000 cached resources
- Performance degradation observed

**How to Prune:**
```bash
# Backup current KG
cp session_kg.json session_kg.json.backup

# Delete KG (will rebuild on next run)
rm session_kg.json

# Restart Zero-Shield
python3 zero_shield_cli.py
```

### KG Performance Metrics

Monitor these indicators:
- **Lookup time:** Should be < 10ms per query
- **Cache hit rate:** Should be > 80%
- **Memory usage:** Should be < 50 MB

---

## Performance Metrics

### Response Time Monitoring

**Expected Response Times:**
| Operation | Target | Warning | Critical |
|-----------|--------|---------|----------|
| List instances | < 2s | > 5s | > 10s |
| Describe SG | < 1s | > 3s | > 5s |
| Quarantine action | < 3s | > 10s | > 20s |
| LLM inference | < 5s | > 15s | > 30s |

### Monitoring Script

```bash
#!/bin/bash
# monitor_performance.sh

LOG_FILE="zero_shield_performance.log"

while true; do
    START=$(date +%s%N)
    
    # Simulate Zero-Shield operation
    timeout 30 python3 -c "
import boto3
ec2 = boto3.client('ec2')
ec2.describe_instances(MaxResults=10)
" 2>&1
    
    END=$(date +%s%N)
    DURATION=$(( (END - START) / 1000000 ))  # Convert to ms
    
    echo "$(date): AWS API call took ${DURATION}ms" >> $LOG_FILE
    
    if [ $DURATION -gt 5000 ]; then
        echo "WARNING: Slow response detected (${DURATION}ms)" | tee -a $LOG_FILE
    fi
    
    sleep 60
done
```

---

## Log Analysis

### Application Logs

Zero-Shield outputs to stdout. Capture logs for analysis:

```bash
# Run with logging
python3 zero_shield_cli.py 2>&1 | tee zero_shield.log

# Or use systemd journal (if running as service)
journalctl -u zero-shield -f
```

### Log Patterns to Monitor

**Normal Operations:**
```
[*] Session state saved (encrypted) → session_state.json
[*] Knowledge Graph updated → session_kg.json
[ORIENT] Analyzing user intent...
[DECIDE] Executing tool: list_instances
[ACT] Completed successfully
```

**Warning Signs:**
```
[!] Rate limit approaching (80% quota used)
[!] Session file corruption detected
[!] AWS API throttling detected
[!] LLM API error (retrying...)
```

**Critical Issues:**
```
[ERROR] Failed to save session state
[ERROR] AWS credentials invalid
[ERROR] GITHUB_TOKEN expired
[ERROR] Unhandled exception
```

### Log Analysis Commands

```bash
# Count errors in last hour
grep -c "\[ERROR\]" zero_shield.log

# Find slow operations
grep "took.*ms" zero_shield.log | awk '{print $NF}' | sort -n | tail -10

# Monitor rate limiting
grep -i "rate limit" zero_shield.log

# Track session file operations
grep "Session state saved" zero_shield.log | wc -l
```

---

## AWS CloudWatch Integration

### Custom Metrics

```python
# Add to zero_shield_cli.py for CloudWatch metrics
import boto3
cloudwatch = boto3.client('cloudwatch')

def publish_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='ZeroShield',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': unit
        }]
    )

# Example usage
publish_metric('ActionsExecuted', 1)
publish_metric('ResponseTime', response_time_ms, 'Milliseconds')
```

### CloudWatch Alarms

```bash
# Create alarm for high error rate
aws cloudwatch put-metric-alarm \
    --alarm-name zero-shield-high-errors \
    --alarm-description "Zero-Shield error rate > 10/hour" \
    --metric-name Errors \
    --namespace ZeroShield \
    --statistic Sum \
    --period 3600 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold
```

---

## Health Check Endpoints

### Manual Health Check

```bash
# Test AWS connectivity
aws sts get-caller-identity

# Test GitHub Models API
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     https://models.inference.ai.azure.com/models

# Test Zero-Shield startup
timeout 10 python3 -c "
import zero_shield_cli
print('Health check: OK')
"
```

### Automated Health Monitoring

```bash
#!/bin/bash
# health_check.sh

# Check session files exist
if [ ! -f session_state.json ]; then
    echo "CRITICAL: session_state.json missing"
    exit 1
fi

# Check file permissions
PERMS=$(stat -c %a session_state.json)
if [ "$PERMS" != "600" ]; then
    echo "WARNING: Incorrect file permissions ($PERMS)"
fi

# Check AWS credentials
if ! aws sts get-caller-identity &>/dev/null; then
    echo "CRITICAL: AWS credentials invalid"
    exit 1
fi

echo "Health check: PASS"
exit 0
```

---

## Alerting Strategy

### Alert Levels

**INFO:** Routine operations, no action required
**WARNING:** Potential issues, monitor closely
**ERROR:** Action required within 1 hour
**CRITICAL:** Immediate action required

### Alert Channels

1. **CloudWatch Alarms** → SNS → Email/SMS
2. **Log-based alerts** → CloudWatch Logs Insights
3. **Custom scripts** → PagerDuty/Slack webhooks

### Sample Alert Rules

```bash
# Alert on session file corruption
if ! python3 -c "import json; json.load(open('session_state.json'))" 2>/dev/null; then
    echo "CRITICAL: Session file corrupted" | mail -s "Zero-Shield Alert" admin@example.com
fi

# Alert on high memory usage
MEM_USAGE=$(ps aux | grep zero_shield_cli.py | awk '{print $4}')
if (( $(echo "$MEM_USAGE > 50" | bc -l) )); then
    echo "WARNING: High memory usage ($MEM_USAGE%)"
fi
```

---

## Dashboard Recommendations

### Key Metrics to Display

1. **Operations per hour**
2. **Average response time**
3. **Error rate**
4. **Session file size**
5. **KG cache hit rate**
6. **AWS API quota usage**

### Sample CloudWatch Dashboard

```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["ZeroShield", "ActionsExecuted"]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "Actions per 5 minutes"
      }
    }
  ]
}
```

---

## Troubleshooting Performance Issues

See `docs/admin-guide/TROUBLESHOOTING.md` for detailed troubleshooting steps.

---

## Next Steps

- Review security monitoring: `docs/admin-guide/SECURITY.md`
- Setup maintenance procedures: `docs/admin-guide/MAINTENANCE.md`
- Configure backup/recovery: `docs/admin-guide/BACKUP_RECOVERY.md`
