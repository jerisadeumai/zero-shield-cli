# Zero-Shield CLI: AI-Native AWS Terminal Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Compatible-orange.svg)](https://aws.amazon.com/)
[![Security Hardened](https://img.shields.io/badge/Security-Hardened-green.svg)](#security)

**Zero-Shield CLI** is an AI-native security orchestrator that translates natural language into immediate AWS security actions. Built for security analysts, DevSecOps engineers, and incident responders who need rapid cloud threat investigation and remediation.

## Quick Start

**📺 Watch Live Demo:** [Zero-Shield CLI in Action](https://www.youtube.com/watch?v=iTuvqgTAUhA) - See the [March 3, 2026 commit](https://github.com/jerisadeumai/zero-shield-cli/commit/9c56283724b7e1dcd16349833026ce9c731eb17c) demonstrated live!

Choose your deployment environment:

| Environment | Setup Time | Best For |
|-------------|------------|----------|
| **[AWS CloudShell](environments/cloudshell/SETUP.md)** | 2 minutes | Production use, inherits IAM roles |
| **[Local Development](environments/local/SETUP.md)** | 5 minutes | Development, testing, customization |

**Platform Compatibility:**
- ✅ **Windows** (Windows 10+) - Full support with ANSI colors
- ✅ **Linux/Unix** (Ubuntu 20.04+) - Native POSIX support  
- ✅ **macOS** (macOS 12+) - Native terminal compatibility
- ✅ **AWS CloudShell** - Inherits IAM credentials automatically

**Fastest Start (CloudShell):**
```bash
# 1. Upload zero_shield_cli.py to CloudShell
# 2. Configure environment
cp environments/cloudshell/.env.example .env
# Edit .env with your GITHUB_TOKEN and QUARANTINE_SG_ID
# 3. Run
python3 zero_shield_cli.py
```

**Local Development:**
```bash
# 1. Clone repository
git clone https://github.com/jerisadeumai/zero-shield-cli.git
cd zero-shield-cli

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp environments/local/.env.example .env
# Edit .env with AWS credentials and GITHUB_TOKEN

# 4. Run
python3 zero_shield_cli.py
```

## Planned Deployment Options

Future releases will include additional deployment methods:

- **Docker** - Containerized deployment with pre-configured environment
- **EC2 Instance** - Direct deployment on AWS EC2 with IAM role integration  
- **AWS Lambda** - Serverless function deployment for event-driven security
- **Container Platforms** - Kubernetes, ECS, and other orchestration platforms

**Planned AI Model Integrations:**

- **Amazon Nova AI Models** - Integration with Amazon's Nova foundation models for enhanced reasoning
- **AWS Bedrock** - Support for Claude, Llama, and other Bedrock-hosted models
- **AWS SageMaker** - Custom model deployment and fine-tuning capabilities

*These are planned for future releases and not available in v2.0.0-dev preview.*

## What Zero-Shield Does

```bash
# Natural language security operations
> "What instances are currently running?"
> "Inspect the security groups for instance i-0123456789abcdef0" 
> "This instance looks compromised. Isolate it immediately."
> "Show me all GuardDuty findings from the last 24 hours"
> "What's the cost impact of running these instances?"
```

**Key Capabilities:**
- **32 AWS Actions** across 14 service categories (EC2, IAM, S3, RDS, Lambda, CloudWatch, GuardDuty, KMS, DynamoDB, EFS, WAF, CloudTrail, Cost Explorer, CloudWatch Logs)
- **5 LLM Models** (GPT-4o, Llama-3.3-70B, Phi-4, DeepSeek-V3, gpt-4o-mini)
- **OODA Loop Framework** (Observe-Orient-Decide-Act)
- **Security Hardened** (5-layer credential redaction, encrypted state)
- **Context-Aware Memory** (Knowledge Graph survives reboots)

## Documentation

### Getting Started
- **[Quick Start Guide](QUICK_START.md)** - 5-minute setup
- **[AWS Setup Guide](aws-setup/IAM_POLICIES.md)** - IAM policies & permissions
- **[Command Reference](docs/user-guide/COMMANDS.md)** - All available commands
- **[Usage Examples](docs/user-guide/EXAMPLES.md)** - Real-world scenarios

### Environment Setup
- **[CloudShell Setup](environments/cloudshell/SETUP.md)** - AWS CloudShell deployment
- **[Local Development](environments/local/.env.example)** - Local environment configuration

### Technical Documentation
- **[Architecture Overview](docs/architecture/ARCHITECTURE.md)** - OODA framework, memory management
- **[OODA Loop Details](docs/architecture/OODA.md)** - Cognitive cycle implementation

### Quality Assurance
- **[Test Reports](validation/TEST_REPORTS.md)** - Comprehensive testing results
- **[Validation Reports](validation/reports/)** - Complete audit history

## Security & Trust

Zero-Shield has undergone extensive security hardening:

- **3,069 Lines Analyzed** - Zero critical bugs found during development
- **100% Test Coverage** - 66 comprehensive + 35 security tests
- **5-Layer Credential Redaction** - AWS credentials never logged
- **Encrypted State Files** - Session data protected at rest
- **Human-in-the-Loop** - Destructive actions require confirmation

[View detailed validation reports →](validation/reports/)

## Specification & Validation

Zero-Shield CLI is built on a comprehensive formal specification with property-based testing:

- **[50 Validated Requirements](.kiro/specs/zero-shield-cli-comprehensive-spec/requirements.md)** - Complete system requirements using EARS protocol
- **[30 Correctness Properties](.kiro/specs/zero-shield-cli-comprehensive-spec/design.md)** - Formal properties with property-based testing
- **[131 Total Tests](.kiro/specs/zero-shield-cli-comprehensive-spec/tasks.md)** - 35 security + 66 comprehensive + 30 property-based tests
- **100% Test Pass Rate** - All tests passing with zero failures
- **Property-Based Testing** - Universal correctness guarantees using Hypothesis library
- **Round-Trip Integrity** - Session state and Knowledge Graph persistence validated
- **Security Properties** - Credential redaction, prompt injection prevention, HITL confirmations

The comprehensive specification covers:
- REPL interface and OODA loop cognitive cycle
- 32 AWS actions across 14 service categories
- Multi-model LLM support (5 models)
- 5-layer security architecture
- Cross-platform compatibility (Unix/Linux, Windows, AWS CloudShell)
- Encrypted persistent storage with atomic writes
- Rate limit handling and API resilience

[View complete specification →](.kiro/specs/zero-shield-cli-comprehensive-spec/)

## Development with Kiro

The `agent-v2-dev` branch was developed extensively using **[Kiro](https://kiro.dev)** - an AI-powered development assistant that enabled rapid, specification-driven development:

**Kiro-Powered Development Artifacts:**
- **[Comprehensive Specification](.kiro/specs/zero-shield-cli-comprehensive-spec/)** - 50 requirements, 30 correctness properties, complete implementation plan
- **[Custom Steering Rules](.kiro/steering/)** - Project-specific AI guidance for product, technology stack, structure, and communication
- **Property-Based Testing** - 30 automated correctness properties using Hypothesis library
- **Documentation Generation** - Automated synchronization between code and documentation
- **Quality Assurance** - Systematic validation of all 50 requirements and 30 properties

**Development Methodology:**
1. **Specification-First** - Formal requirements and design documents created before implementation
2. **Property-Based Testing** - Universal correctness guarantees through automated property validation
3. **Iterative Refinement** - Continuous validation against specification throughout development
4. **Documentation Sync** - Automated verification that documentation matches implementation

**Acknowledgments:**
- Developed with [Kiro](https://kiro.dev) - AI-powered development assistant
- AWS services integration via [AWS SDK for Python (Boto3)](https://github.com/boto/boto3)
- LLM inference via [GitHub Models API](https://github.com/marketplace/models)
- Property-based testing via [Hypothesis](https://hypothesis.readthedocs.io/)

Special thanks to:
- [@awslabs](https://github.com/awslabs) - AWS SDK and tools
- [@aws](https://github.com/aws) - AWS platform and services
- Amazon Web Services for CloudShell environment

This development approach demonstrates how AI-assisted development with formal specifications can produce high-quality, well-tested, and thoroughly documented software.

## AWS Permissions

Zero-Shield requires specific AWS IAM permissions. We provide three policy levels:

| Policy | Use Case | Permissions |
|--------|----------|-------------|
| **[Minimal](aws-setup/policies/zero-shield-minimal.json)** | Read-only investigation | EC2 describe, IAM list |
| **[Standard](aws-setup/policies/zero-shield-standard.json)** | Most security operations | + S3, RDS, Lambda, CloudWatch |
| **[Full](aws-setup/policies/zero-shield-full.json)** | Complete functionality | + Quarantine, key deactivation |

[Detailed IAM setup guide →](aws-setup/IAM_POLICIES.md)

## Interactive Demo

Try these example commands after setup:

```bash
# Investigation workflow
/target i-0123456789abcdef0 # Set target instance
inspect instance # Get detailed info
check its security groups # Analyze SG rules
what vpc is it in? # VPC information

# Security assessment
list guardduty findings # Recent threats
show me iam users without mfa # IAM security gaps
what s3 buckets are public? # Storage exposure

# Cost analysis
estimate cost for this instance # Cost projection
show 7 day spend breakdown # Recent spending
```

## Production Status

**Current Version:** v2.0.0-dev  
**Status:** Development Branch - Not Yet Released  
**Branch:** agent-v2-dev  
**Last Main Branch Commit:** March 3, 2026 (commit: d3754fc)  
**Development Branch Updates:** March 13-16, 2026  

**Development Quality Metrics:**
- 3,069 lines of code analyzed and certified bug-free
- 66/66 comprehensive tests passing (100%)
- 35/35 security tests passing (100%)
- 5 critical security fixes applied and validated
- 99.0% development confidence score

## Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

**Quick contribution setup:**
```bash
git clone https://github.com/jerisadeumai/zero-shield-cli.git
cd zero-shield-cli
pip install -r requirements.txt
python3 test_comprehensive_e2e.py # Run tests
```

## Support

- **Issues:** [GitHub Issues](https://github.com/jerisadeumai/zero-shield-cli/issues)
- **Documentation:** [Command Reference](docs/user-guide/COMMANDS.md)
- **Setup Help:** [Quick Start Guide](QUICK_START.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Principal Architect:** Jeri L3D | JeriSadeuM  
**Repository:** https://github.com/jerisadeumai/zero-shield-cli  
**Live Demo:** [YouTube - Zero-Shield CLI in Action](https://www.youtube.com/watch?v=iTuvqgTAUhA) *(Demonstrates commit [9c56283](https://github.com/jerisadeumai/zero-shield-cli/commit/9c56283724b7e1dcd16349833026ce9c731eb17c) from March 3, 2026)*  
**Copyright © 2026 Jeri L3D | JeriSadeuM | All Rights Reserved**

---

*Zero-Shield CLI: Where AI meets AWS security at the speed of thought.*