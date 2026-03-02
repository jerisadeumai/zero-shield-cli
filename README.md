### Zero-Shield CLI: Agentic Security Copilot

**Zero-Shield** is an AI-native security orchestrator designed for rapid cloud threat remediation. Built on the **OODA loop** (Observe-Orient-Decide-Act) framework, it utilizes **GitHub Models (GPT-4o)** and **AWS Boto3** to translate natural language into immediate infrastructure action.

## Key Features

* **Conversational REPL:** Manage cloud security via a simple terminal interface.
* **Agentic Reasoning:** Automatically extracts Instance IDs and Regions from natural language.
* **Instant Remediation:** One-command isolation of compromised EC2 instances.
* **Context-Aware:** Remembers previous commands to maintain an investigation flow.
* **Hardened Defaults:** Built-in safeguards against LLM hallucinations regarding AWS regions.

---

## Installation & Setup

### 1. Prerequisites

* Python 3.9+
* AWS CLI configured with appropriate permissions (`ec2:ModifyInstanceAttribute`, `ec2:DescribeInstances`).
* A GitHub Personal Access Token for GitHub Models.

### 2. Clone and Install

```bash
git clone https://github.com/jerisadeumai/zero-shield-cli
cd zero-shield-cli
pip install boto3 openai python-dotenv

```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```text
GITHUB_TOKEN=your_github_model_token_here

```

---

## How to Use (Prompts to Try)

Run the agent:

```bash
python3 zero_shield_cli_v2.0.0.py

```

### Step 1: Observe (Discovery)

Scan your environment to see what's running.

> **User:** "What instances are currently running in the us-east-1 region?"

### Step 2: Orient (Investigation)

Get security context on a specific target.

> **User:** "Inspect the security groups and state for instance i-02c35a50d214cf886."

### Step 3: Act (Remediation)

Execute the "Nuclear Option" to secure your perimeter.

> **User:** "This instance looks like it has been compromised by an SSH brute-force attack. Isolate it immediately."

---

## Architecture

Zero-Shield acts as the "Brain" between the Security Analyst and the Cloud Infrastructure.

1. **Observe:** Uses Boto3 to pull real-time data from AWS EC2.
2. **Orient:** GPT-4o analyzes the metadata and user intent.
3. **Decide:** The agent selects the correct tool (LIST, INSPECT, or QUARANTINE).
4. **Act:** Executes the API call to move the instance into a restricted Security Group.

---

## Roadmap

* [ ] **Multi-Cloud Support:** Integration with Azure and GCP security sets.
* [ ] **Automated Rollback:** One-click restoration after a "Clear" status is achieved.
* [ ] **Slack/Teams Bot:** Move the REPL from the terminal to enterprise chat apps.
* [ ] **IAM Analysis:** Agentic auditing of user permissions and roles.
