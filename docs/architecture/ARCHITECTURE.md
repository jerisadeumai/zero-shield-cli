# Zero-Shield CLI: Technical Architecture Manifesto (v2.0.0-dev)

**Last Updated:** March 16, 2026  
**Copyright © 2026 Jeri L3D | JeriSadeuM | All Rights Reserved**
**License:** MIT License
**Repository:** https://github.com/jerisadeumai/zero-shield-cli  
**Specification:** [Comprehensive Spec](.kiro/specs/zero-shield-cli-comprehensive-spec/)

---

This document details the advanced engineering philosophy, memory management, and API resilience mechanisms that power the Zero-Shield Agentic Engine.

**Formal Specification:** This architecture is backed by a comprehensive formal specification with 50 validated requirements, 30 correctness properties, and 131 tests (100% pass rate). See [specification documentation](.kiro/specs/zero-shield-cli-comprehensive-spec/) for complete requirements, design properties, and property-based testing implementation.

---

## 1. The OODA Cognitive Engine

Zero-Shield abandons simple "If/Then" logic. Every terminal turn is a multi-stage cognitive cycle based on military strategy:

* **Observe**: The script injects live AWS snapshot data and Knowledge Graph (KG) context into the prompt prefix before the user's input is processed.
* **Orient**: The LLM analyzes the delta between the user's intent and the current environment state, factoring in previous constraints.
* **Decide**: The LLM determines if a Boto3 tool call is required, or if the answer already exists in the local KG.
* **Act**: The LLM triggers a strictly formatted [ACTION:TAG] which the Python backend parses and executes, feeding the result back into the observation loop.

---

## 2. Skeptical Architecture (API Resilience)

Zero-Shield operates on the "Skeptical Architecture" principle -- it assumes API provider headers (like Retry-After: 0) are actively misleading during saturation.

* **Adaptive Triage**: Most free-tier APIs use a 1-minute sliding window. If a 429 occurs, Zero-Shield enforces a mandatory 60-second safety floor, allowing the backend sliding window to physically drain.
* **Escalation**: On Strike 2+, the floor autonomously escalates to 120 seconds, recognizing severe "Window Contamination."
* **Agnostic Exponential Backoff**: Uses a deterministic ladder: 2s -> 4s -> 8s -> 16s -> 32s (Hard Cap).

---

## 3. Memory Segregation: State vs. Graph

Memory is split into a dual-layer persistence system:

1. **Session State (session_state.json)**: Volatile metadata tracking active IDs, quota maps, and cooldown timers.
2. **Knowledge Graph (session_kg.json)**: A persistent lookup cache for audited resources (SG rules, VPC subnets, IAM). This creates a RAG framework that survives reboots.
3. **Atomic Integrity**: To prevent corruption during power loss, Zero-Shield uses an atomic write pattern (tempfile + `os.replace`). Data is never left in a partial state.

---

## 4. Prompt Resilience: Replay & Cleanse

* **Prompt Replay**: If a model times out, the user can swap the backend (e.g., DeepSeek -> GPT-4o). The user's input is cached and re-sent to the new model family.
* **Context Cleanse (The Air-Gap)**: Before replay, conversation history is rolled back. This strips corrupted or hallucinated messages, ensuring the new model receives a mathematically clean context.

---

## 5. Triple-Hardening (Physics & Cognitive)

The agent-v2 release utilizes "Triple-Lock" hardening to ensure 100% compliance in production environments:

* **Entropy-Aware Redaction**: The redaction engine utilizes a range-based (16-40 char) entropy scanner. This prevents "Base64 Cleverness" where the AI outputs shorter high-entropy strings to bypass fixed-length filters.
* **MedGemma Strict Compliance**: To prevent "Helpfulness Bias" from violating negative constraints (e.g., "Do not use IDs"), a `[STRICT_COMPLIANCE_PROTOCOL]` is anchored at the terminal segment of the system prompt. This creates a high "Recency Bias" anchor, forcing the model to prioritize user-imposed restrictions over task completion.
* **Cross-Platform Buffer Management**: To prevent terminal spills, the Buffer Management (Paste Guard) uses OS-aware flushing (POSIX `select` vs. Windows `msvcrt`). A mandatory `0.2s` physical buffer drain is enforced to mitigate stdin race conditions during high-volume pastes.
* **Input Sanitization (Data-Plane Defanger)**: The `_sanitize_aws_tag` layer programmatically strips structural characters and markdown/XML escapes from AWS environment metadata. This prevents "Environment Poisoning" where an attacker injects prompt instructions via an EC2 Name tag or S3 bucket name.
* **Non-Blocking Buffer Management (Paste Guard 2.0)**: The REPL utilizes strictly non-blocking I/O (`select.select(0.0)`) to poll the terminal buffer. If a multi-line burst is detected, a `universal_flush` is triggered to physically drain the OS input queue, neutralizing token-burning loops.
* **Format Strike System**: To prevent "Infinite API Traps," the execution engine implements a 3-strike kill-switch. If the model fails the OODA formatting mandate 3 times consecutively, the execution loop is severed, returning control to the user.
* **Target Validation (Hallucination Prevention)**: The REPL prompt forcefully injects `[ACTIVE TARGET: NONE]` when the context is empty. This prevents the LLM from assuming a target from background training data, enforcing a "Target-First" operational doctrine.
* **Private CIDR (RFC 1918) Awareness**: The SG audit engine factors in 10.x, 172.x, and 192.x address spaces. It programmatically distinguishes between "VPC-Open" and "Internet-Open," eliminating noise in isolated subnets.
* **Inference Repointing**: Supports the `GITHUB_MODELS_URL` env var. This allows the CLI to be repointed to local Ollama or private Azure OpenAI instances without code changes.

---
Principal Architect: Jeri L3D | JeriSadeuM | Version: v2.0.0-dev | Repository: [zero-shield-cli](https://github.com/jerisadeumai/zero-shield-cli) | Specification: [Comprehensive Spec](.kiro/specs/zero-shield-cli-comprehensive-spec/)
