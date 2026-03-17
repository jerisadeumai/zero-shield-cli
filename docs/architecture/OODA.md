# Zero-Shield: OODA Reasoning Framework (v2.0.0-dev)

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Last Updated: March 17, 2026  
> **This branch contains features not yet in the main branch.**

**Last Updated:** March 17, 2026  
**Copyright © 2026 Jeri L3D | JeriSadeuM | All Rights Reserved**
**License:** MIT License
**Repository:** https://github.com/jerisadeumai/zero-shield-cli  
**Specification:** [Comprehensive Spec](.kiro/specs/zero-shield-cli-comprehensive-spec/)

---

Zero-Shield operates on a clinical **Observe-Orient-Decide-Act** loop. This document details the reasoning chains and the security gates that prevent cognitive collapse.

**Formal Specification:** The OODA loop implementation is formally specified in [Requirement 2](.kiro/specs/zero-shield-cli-comprehensive-spec/requirements.md) with 10 acceptance criteria and validated by [Property 7](.kiro/specs/zero-shield-cli-comprehensive-spec/design.md) (OODA Loop Formatting Enforcement) using property-based testing.

## 1. The OODA Sequence

1. **OBSERVE**: The Python backend fetches live AWS data and injects it into the system prompt.
2. **ORIENT**: The AI analyzes the data to identify security deltas or threats.
3. **DECIDE**: The AI selects the appropriate tool or identifies if a target must be set.
4. **ACT**: The AI executes a strictly formatted `[ACTION:TAG]`.

## 2. v2.0.1-Beta Security Gates

To prevent the "Infinite Loop Trap" and "Hallucination Bleed" identified in the Stress Testing (Edge Case Matrix), the following gates are now enforced:

### Gate A: The Format Enforcer (REPL-Layer)
- **Logic**: Every AI response must contain `[ORIENT]`, `[DECIDE]`, and `[ACT]`.
- **Constraint**: If tags are missing, the system intercepts, issues a `[SYSTEM ERROR]` user-correction, and increments a strike counter.
- **Kill-Switch**: At 3 consecutive strikes, the session is severed to prevent invisible token-burning loops.

### Gate B: Target Validation (Hallucination Prevention) (Target-Layer)
- **Logic**: Explicit targeting is mandatory.
- **Constraint**: If `last_id` is None, a crimson `[ACTIVE TARGET: NONE]` alert is injected into the prompt.
- **Constraint**: Rule #8 forbids the AI from assuming targets based on background training data or resource names.

### Gate C: Input Sanitization (Data-Plane Defanger) (Ingestion-Layer)
- **Logic**: All environment metadata is considered hostile until sanitized.
- **Shield**: The `_sanitize_aws_tag` function strips structural characters (`[`, `]`, `` ` ``, `<`, `>`, `ACTION:`) from AWS resource tags during the **OBSERVE** phase, neutralizing code-injection or XML-wrapping attacks.

### Gate D: Buffer Management (Paste Guard) (I/O Layer)
- **Logic**: Multi-line bursts indicate manual terminal spills, not clinical interaction.
- **Shield**: Uses non-blocking I/O polling to detect rapid buffer fills. If triggered, `universal_flush` is called to physically discard the runaway stdin data before it reaches the AI.

---
Principal Architect: Jeri L3D | JeriSadeuM | Version: v2.0.0-dev | Specification: [Comprehensive Spec](.kiro/specs/zero-shield-cli-comprehensive-spec/)
