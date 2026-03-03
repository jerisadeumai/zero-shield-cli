# Zero-Shield CLI: Agentic Security Copilot

**Zero-Shield** is an AI-native security orchestrator designed for rapid cloud threat remediation. Built on the deterministic OODA loop (Observe-Orient-Decide-Act) framework, it utilizes GitHub Models (GPT-4o) and AWS Boto3 to translate natural language into immediate infrastructure action.

## Key Features

* **Conversational REPL:** Manage cloud security via a simple terminal interface.
* **Agentic Reasoning:** Automatically extracts Instance IDs and Regions from natural language.
* **Instant Remediation:** One-command isolation of compromised EC2 instances.
* **Context-Aware:** Remembers previous commands to maintain an investigation flow.
* **Hardened Defaults:** Built-in safeguards against LLM hallucinations regarding AWS regions.

## System Architecture

Zero-Shield acts as the autonomous reasoning engine between the Security Analyst and the Cloud Infrastructure.

* **Observe:** Uses Boto3 to pull real-time telemetry and state data from AWS EC2.
* **Orient:** GPT-4o analyzes the metadata, extracting instance IDs and inferring user intent.
* **Decide:** The agent mathematically maps the intent to the correct execution tool (LIST, INSPECT, or QUARANTINE).
* **Act:** Executes the API call to move the compromised instance into an isolated, restricted Security Group (`sg-0123456789abcdef0`).

## Installation and Setup

### 1. Prerequisites
* Python 3.9+
* A GitHub Personal Access Token (PAT) for the reasoning engine.
* AWS IAM user credentials with `ec2:ModifyInstanceAttribute` and `ec2:DescribeInstances` permissions.

### 2. Clone and Install
```bash
git clone https://github.com/jerisadeumai/zero-shield-cli.git
cd zero-shield-cli
pip install -r requirements.txt
```

### 3. Environment & Authentication

Zero-Shield utilizes the Boto3 Default Credential Provider Chain. By using a `.env` file, credentials are injected into the process environment variables, allowing Boto3 to automatically authenticate without hardcoded keys in the source code.

Copy the template file to create your local environment:
```bash
cp .env.example .env
```

Open `.env` and insert your secure values:
```env
GITHUB_TOKEN=your_github_personal_access_token_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=us-east-1
```
*(Note: If running inside a pre-authenticated environment such as AWS CloudShell, the AWS keys in `.env` may be left blank as the SDK will inherit the active session's IAM role).*

## Execution (REPL)

Launch the conversational terminal:
```bash
python3 zero_shield_cli.py
```

## Tactical Prompts

* **Observe (Discovery):** "What instances are currently running in the us-east-1 region?"
* **Orient (Investigation):** "Inspect the security groups and state for instance i-0123456789abcdef0."
* **Act (Remediation):** "This instance looks like it has been compromised by an SSH brute-force attack. Isolate it immediately."

## Roadmap

* **Multi-Cloud Support:** Integration with Azure and GCP security sets.
* **Automated Rollback:** One-click restoration after a "Clear" status is achieved.
* **Slack/Teams Bot:** Move the REPL from the terminal to enterprise chat apps.
* **IAM Analysis:** Agentic auditing of user permissions and roles.

---
Copyright (c) 2026 JeriSadeuM AI | Licensed under the MIT License.
