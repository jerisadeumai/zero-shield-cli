# Requirements Document: Zero-Shield CLI

## Introduction

Zero-Shield CLI is an AI-native security orchestrator for rapid cloud threat remediation. It functions as an agentic AWS security copilot that translates natural language commands into immediate infrastructure actions through a conversational REPL interface. The system implements a deterministic OODA loop (Observe-Orient-Decide-Act) cognitive cycle, integrates with 14 AWS service categories providing 32 distinct actions, supports 5 LLM models via GitHub Models API, and enforces enterprise-grade security through 5-layer credential redaction, prompt injection prevention, XOR encryption, and Human-in-the-Loop confirmations for destructive operations.

## Glossary

- **Zero_Shield_CLI**: The main command-line interface application that orchestrates AWS security operations
- **REPL**: Read-Eval-Print Loop - the interactive terminal interface for user commands
- **OODA_Loop**: Observe-Orient-Decide-Act cognitive cycle that structures all system reasoning
- **LLM**: Large Language Model - AI inference engine for natural language processing
- **GitHub_Models_API**: External API service providing LLM inference capabilities
- **Knowledge_Graph**: Persistent cache of audited AWS resources stored in session_kg.json
- **Session_State**: Volatile metadata tracking active resources, quotas, and cooldowns in session_state.json
- **HITL**: Human-in-the-Loop - mandatory confirmation mechanism for destructive actions
- **Credential_Redaction_Engine**: 5-layer security system that removes sensitive data from outputs
- **Sanitization_Layer**: Security boundary that prevents prompt injection via AWS resource metadata
- **XOR_Encryption**: Symmetric encryption using GITHUB_TOKEN as key for session files
- **Quarantine_Security_Group**: AWS security group that blocks all network traffic for compromised instances
- **Atomic_Write_Pattern**: File write mechanism using tempfile + os.replace to prevent corruption
- **Lazy_Client_Factory**: AWS client caching mechanism to avoid recreation overhead
- **Paste_Guard**: Non-blocking I/O system that prevents terminal buffer overflow attacks
- **Format_Strike_System**: 3-strike enforcement mechanism for OODA formatting compliance
- **Skeptical_Architecture**: API resilience pattern assuming provider headers are misleading during saturation
- **Adaptive_Triage**: Rate limit handling with 60-second safety floor and escalation to 120 seconds
- **Target_Context**: Active AWS resource ID maintained in session state for context-aware operations
- **Boto3**: AWS SDK for Python used for all AWS API interactions
- **CloudShell**: AWS CloudShell environment for serverless deployment
- **IAM_Policy**: AWS Identity and Access Management policy defining permitted actions

---

## Requirements

### Requirement 1: REPL Interface and User Interaction

**User Story:** As a security analyst, I want a conversational command-line interface, so that I can investigate and remediate AWS security incidents using natural language.

#### Acceptance Criteria

1. WHEN the application starts, THE REPL SHALL display a welcome banner with version information and system status
2. WHEN the user enters a command, THE REPL SHALL accept natural language input without requiring specific syntax
3. WHILE the REPL is active, THE REPL SHALL maintain an interactive prompt for continuous user input
4. WHEN the user types "exit" or presses Ctrl+C, THE REPL SHALL gracefully terminate and save session state
5. THE REPL SHALL support system commands prefixed with "/" for meta-operations
6. WHEN the user enters "/help", THE REPL SHALL display available commands and usage guidance
7. WHEN the user enters "/status", THE REPL SHALL display current system state including active target, model, quotas, and cooldowns
8. WHEN the user enters "/clear", THE REPL SHALL reset conversation history while preserving session state
9. THE REPL SHALL provide color-coded output with success (green), error (red), warning (yellow), and info (cyan) messages
10. WHEN the REPL displays output, THE REPL SHALL apply credential redaction to all text before rendering

### Requirement 2: OODA Loop Cognitive Cycle

**User Story:** As a system architect, I want all operations to follow the OODA loop pattern, so that the system maintains deterministic reasoning and auditability.

#### Acceptance Criteria

1. WHEN processing any user command, THE OODA_Loop SHALL execute the Observe phase by injecting live AWS snapshot data
2. WHEN the Observe phase completes, THE OODA_Loop SHALL execute the Orient phase to analyze deltas between user intent and environment state
3. WHEN the Orient phase completes, THE OODA_Loop SHALL execute the Decide phase to determine required actions
4. WHEN the Decide phase completes, THE OODA_Loop SHALL execute the Act phase by triggering formatted [ACTION:TAG] commands
5. THE OODA_Loop SHALL format all LLM responses with explicit [ORIENT], [DECIDE], and [ACT] section markers
6. IF an LLM response lacks required OODA formatting, THEN THE Format_Strike_System SHALL increment the strike counter
7. WHEN the Format_Strike_System reaches 3 consecutive strikes, THE OODA_Loop SHALL terminate execution and return control to the user
8. THE OODA_Loop SHALL inject Knowledge_Graph context during the Observe phase for persistent resource awareness
9. THE OODA_Loop SHALL feed action execution results back into the observation loop for iterative refinement
10. THE OODA_Loop SHALL maintain conversation history across multiple turns within a session

### Requirement 3: AWS Service Integration - EC2 and Networking

**User Story:** As a security analyst, I want to investigate and remediate EC2 instances and network configurations, so that I can respond to compute-related security incidents.

#### Acceptance Criteria

1. WHEN the user requests instance listing, THE Zero_Shield_CLI SHALL execute [ACTION:LIST] to retrieve all EC2 instances with ID, name, state, type, and IP addresses
2. WHEN the user requests instance inspection, THE Zero_Shield_CLI SHALL execute [ACTION:INSPECT:instance_id] to retrieve complete instance metadata including VPC, subnet, security groups, and IAM role
3. WHEN the user requests security group analysis, THE Zero_Shield_CLI SHALL execute [ACTION:SG_RULES:sg_id] to retrieve inbound and outbound rules with risk assessment
4. WHEN analyzing security group rules, THE Zero_Shield_CLI SHALL distinguish between RFC 1918 private CIDR blocks and public internet exposure
5. WHEN the user requests VPC information, THE Zero_Shield_CLI SHALL execute [ACTION:VPC_INFO:vpc_id] to retrieve CIDR blocks, subnets, route tables, and internet gateway status
6. WHEN the user requests EBS volume listing, THE Zero_Shield_CLI SHALL execute [ACTION:EC2_VOLUMES] to retrieve volume IDs, sizes, encryption status, and attachments
7. WHEN the user requests SSH key pair listing, THE Zero_Shield_CLI SHALL execute [ACTION:EC2_KEYPAIRS] to retrieve key names, fingerprints, and creation dates
8. WHEN the user requests network ACL information, THE Zero_Shield_CLI SHALL execute [ACTION:NETWORK_ACLS] to retrieve NACL rules and subnet associations
9. WHEN the user requests instance quarantine, THE Zero_Shield_CLI SHALL execute [ACTION:QUARANTINE:instance_id] after HITL confirmation to move the instance to the quarantine security group

10. WHEN the user requests security group modification, THE Zero_Shield_CLI SHALL execute [ACTION:MODIFY_SG:instance_id:sg_id] after HITL confirmation to change instance security groups

### Requirement 4: AWS Service Integration - IAM

**User Story:** As a security analyst, I want to audit and remediate IAM configurations, so that I can manage identity and access security incidents.

#### Acceptance Criteria

1. WHEN the user requests IAM user listing, THE Zero_Shield_CLI SHALL execute [ACTION:IAM_USERS] to retrieve usernames, MFA status, last activity, and access key ages
2. WHEN the user requests IAM role listing, THE Zero_Shield_CLI SHALL execute [ACTION:IAM_ROLES] to retrieve role names, trust relationships, and attached policies
3. WHEN the user requests access key audit, THE Zero_Shield_CLI SHALL execute [ACTION:IAM_ACCESS_KEYS] to retrieve key IDs, ages, last used dates, and rotation recommendations
4. WHEN the user requests instance IAM profile analysis, THE Zero_Shield_CLI SHALL execute [ACTION:IAM_CHECK:instance_id] to retrieve attached IAM role and effective permissions
5. WHEN the user requests access key deactivation, THE Zero_Shield_CLI SHALL execute [ACTION:DEACTIVATE_ACCESS_KEY:key_id] after HITL confirmation to set key status to inactive
6. WHEN displaying IAM user information, THE Zero_Shield_CLI SHALL highlight users without MFA enabled as security risks
7. WHEN displaying access key information, THE Zero_Shield_CLI SHALL flag keys older than 90 days for rotation

### Requirement 5: AWS Service Integration - Storage and Databases

**User Story:** As a security analyst, I want to audit storage and database configurations, so that I can identify data exposure risks.

#### Acceptance Criteria

1. WHEN the user requests S3 bucket listing, THE Zero_Shield_CLI SHALL execute [ACTION:S3_BUCKETS] to retrieve bucket names, public access status, encryption, and versioning
2. WHEN the user requests S3 bucket policy analysis, THE Zero_Shield_CLI SHALL execute [ACTION:S3_BUCKET_POLICY:bucket_name] to retrieve policy JSON, ACL settings, and public access analysis
3. WHEN the user requests RDS instance listing, THE Zero_Shield_CLI SHALL execute [ACTION:RDS_INSTANCES] to retrieve database identifiers, engine types, sizes, and public accessibility
4. WHEN the user requests DynamoDB table listing, THE Zero_Shield_CLI SHALL execute [ACTION:DYNAMODB_TABLES] to retrieve table names, item counts, capacity, and encryption status
5. WHEN the user requests EFS filesystem listing, THE Zero_Shield_CLI SHALL execute [ACTION:EFS_FILESYSTEMS] to retrieve filesystem IDs, sizes, mount targets, and encryption status
6. WHEN displaying S3 bucket information, THE Zero_Shield_CLI SHALL highlight buckets with public read or write access as security risks
7. WHEN displaying RDS instance information, THE Zero_Shield_CLI SHALL highlight publicly accessible databases as security risks

### Requirement 6: AWS Service Integration - Security Services

**User Story:** As a security analyst, I want to access security service findings, so that I can investigate detected threats and vulnerabilities.

#### Acceptance Criteria

1. WHEN the user requests GuardDuty findings, THE Zero_Shield_CLI SHALL execute [ACTION:GUARDDUTY_FINDINGS] to retrieve finding types, severity levels, affected resources, and timestamps
2. WHEN the user requests KMS key listing, THE Zero_Shield_CLI SHALL execute [ACTION:KMS_KEYS] to retrieve key IDs, aliases, rotation status, and usage information
3. WHEN the user requests WAF WebACL listing, THE Zero_Shield_CLI SHALL execute [ACTION:WAF_WEBACLS] to retrieve WebACL names, associated resources, and rule counts
4. WHEN displaying GuardDuty findings, THE Zero_Shield_CLI SHALL prioritize HIGH and MEDIUM severity findings
5. WHEN displaying KMS key information, THE Zero_Shield_CLI SHALL highlight keys without automatic rotation enabled

### Requirement 7: AWS Service Integration - Monitoring and Logging

**User Story:** As a security analyst, I want to access monitoring and logging data, so that I can investigate system behavior and anomalies.

#### Acceptance Criteria

1. WHEN the user requests CloudWatch logs, THE Zero_Shield_CLI SHALL execute [ACTION:CLOUDWATCH_LOGS:log_group] to retrieve recent log events with timestamps
2. WHEN the user requests CloudWatch alarms, THE Zero_Shield_CLI SHALL execute [ACTION:CLOUDWATCH_ALARMS] to retrieve alarm names, states, metrics, and thresholds
3. WHEN the user requests EC2 metrics, THE Zero_Shield_CLI SHALL execute [ACTION:EC2_METRICS:instance_id] to retrieve CPU utilization, network traffic, and disk I/O
4. WHEN displaying CloudWatch logs, THE Zero_Shield_CLI SHALL apply credential redaction to log content before display
5. THE Zero_Shield_CLI SHALL sanitize all log output through the _sanitize_logs function to remove sensitive data

### Requirement 8: AWS Service Integration - Audit and Cost

**User Story:** As a security analyst, I want to access audit trails and cost information, so that I can investigate who made changes and understand financial impact.

#### Acceptance Criteria

1. WHEN the user requests CloudTrail events, THE Zero_Shield_CLI SHALL execute [ACTION:CLOUDTRAIL] to retrieve recent API calls with user names, source IPs, and timestamps
2. WHEN the user requests instance cost estimation, THE Zero_Shield_CLI SHALL execute [ACTION:COST_INSIGHT:instance_id] to calculate hourly rate and monthly estimate
3. WHEN the user requests cost breakdown, THE Zero_Shield_CLI SHALL execute [ACTION:COST_EXPLORER] to retrieve 7-day spending with service breakdown
4. WHEN displaying CloudTrail events, THE Zero_Shield_CLI SHALL show the last 6 hours of management events by default
5. WHEN displaying cost information, THE Zero_Shield_CLI SHALL format currency values with appropriate precision

### Requirement 9: AWS Service Integration - Serverless

**User Story:** As a security analyst, I want to audit Lambda functions, so that I can investigate serverless security incidents.

#### Acceptance Criteria

1. WHEN the user requests Lambda function listing, THE Zero_Shield_CLI SHALL execute [ACTION:LAMBDA_FUNCTIONS] to retrieve function names, runtimes, memory configurations, and last modified dates
2. WHEN displaying Lambda function information, THE Zero_Shield_CLI SHALL include runtime version for security assessment


### Requirement 10: Multi-Model LLM Support

**User Story:** As a security analyst, I want to switch between different LLM models, so that I can optimize for speed, capability, or compliance based on my current task.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL support 5 LLM models: gpt-4o-mini, Llama-3.3-70B-Instruct, Phi-4, DeepSeek-V3, and gpt-4o
2. WHEN the application starts, THE Zero_Shield_CLI SHALL prompt the user to select an LLM model from the available options
3. WHEN the user enters "/switch", THE Zero_Shield_CLI SHALL display the model selection interface with quota status
4. WHEN the user selects a model, THE Zero_Shield_CLI SHALL initialize the GitHub_Models_API client with the selected model
5. WHEN a model encounters rate limiting, THE Zero_Shield_CLI SHALL display cooldown status and allow switching to an alternative model
6. THE Zero_Shield_CLI SHALL track per-model quota consumption including request counts and token usage
7. WHEN displaying model options, THE Zero_Shield_CLI SHALL show context window sizes: gpt-4o-mini (128K), Llama-3.3-70B (131K), Phi-4 (16K), DeepSeek-V3 (65K), gpt-4o (128K)
8. WHEN a model switch occurs, THE Zero_Shield_CLI SHALL preserve conversation context and replay the last user input to the new model
9. IF the GITHUB_MODELS_URL environment variable is set, THEN THE Zero_Shield_CLI SHALL use the custom endpoint for LLM inference
10. WHEN displaying model selection, THE Zero_Shield_CLI SHALL show model-specific characteristics: Phi-4 (most compliant), gpt-4o (most capable), Llama-3.3-70B (best reasoning), DeepSeek-V3 (deep analysis), gpt-4o-mini (fastest)

### Requirement 11: Credential Redaction Security

**User Story:** As a security administrator, I want all sensitive credentials automatically redacted from outputs, so that secrets are never exposed in terminal displays or logs.

#### Acceptance Criteria

1. THE Credential_Redaction_Engine SHALL implement 5 distinct redaction layers for comprehensive secret detection
2. WHEN processing any text output, THE Credential_Redaction_Engine SHALL detect and redact AWS access key IDs matching pattern AKIA[0-9A-Z]{16}
3. WHEN processing any text output, THE Credential_Redaction_Engine SHALL detect and redact AWS secret access keys matching pattern [A-Za-z0-9/+=]{40}
4. WHEN processing any text output, THE Credential_Redaction_Engine SHALL detect and redact AWS session tokens matching pattern [A-Za-z0-9/+=]{100,}
5. WHEN processing any text output, THE Credential_Redaction_Engine SHALL detect and redact JWT tokens matching pattern eyJ[A-Za-z0-9_-]+\\.eyJ[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+
6. WHEN processing any text output, THE Credential_Redaction_Engine SHALL detect and redact high-entropy strings between 16-40 characters to prevent Base64 encoding bypass
7. WHEN a credential is detected, THE Credential_Redaction_Engine SHALL replace it with "[REDACTED_AWS_KEY]", "[REDACTED_SECRET]", "[REDACTED_TOKEN]", or "[REDACTED_JWT]" as appropriate
8. THE Credential_Redaction_Engine SHALL apply redaction before any text is displayed to the user
9. THE Credential_Redaction_Engine SHALL apply redaction to all AWS API responses before processing
10. THE Credential_Redaction_Engine SHALL apply redaction to all LLM responses before display

### Requirement 12: Prompt Injection Prevention

**User Story:** As a security administrator, I want the system to prevent prompt injection attacks via AWS resource metadata, so that attackers cannot manipulate system behavior through malicious resource names or tags.

#### Acceptance Criteria

1. THE Sanitization_Layer SHALL implement the _sanitize_aws_tag function as a mandatory data-plane defanger
2. WHEN ingesting AWS resource metadata, THE Sanitization_Layer SHALL remove square brackets "[" and "]" from all text
3. WHEN ingesting AWS resource metadata, THE Sanitization_Layer SHALL remove backticks "`" from all text
4. WHEN ingesting AWS resource metadata, THE Sanitization_Layer SHALL remove angle brackets "<" and ">" from all text
5. WHEN ingesting AWS resource metadata, THE Sanitization_Layer SHALL remove the literal string "ACTION:" from all text
6. THE Sanitization_Layer SHALL use an allowlist-only approach for permitted characters in AWS resource names
7. THE Sanitization_Layer SHALL apply sanitization during the OODA Observe phase before data reaches the LLM
8. THE Sanitization_Layer SHALL prevent environment poisoning attacks where EC2 Name tags or S3 bucket names contain prompt instructions
9. THE Sanitization_Layer SHALL apply sanitization to all AWS resource identifiers, names, and tags
10. THE Sanitization_Layer SHALL preserve legitimate AWS resource naming while removing structural characters

### Requirement 13: Human-in-the-Loop Confirmations

**User Story:** As a security administrator, I want destructive actions to require explicit human confirmation, so that the system cannot autonomously execute high-risk operations.

#### Acceptance Criteria

1. WHEN executing [ACTION:QUARANTINE], THE HITL SHALL prompt the user to type the full instance ID for confirmation
2. WHEN executing [ACTION:MODIFY_SG], THE HITL SHALL prompt the user to type the full instance ID for confirmation
3. WHEN executing [ACTION:DEACTIVATE_ACCESS_KEY], THE HITL SHALL prompt the user to type the full access key ID for confirmation
4. IF the user-entered confirmation does not exactly match the resource ID, THEN THE HITL SHALL abort the operation and display an error
5. THE HITL SHALL not accept simple "yes/no" responses for destructive action confirmation
6. THE HITL SHALL require full resource ID re-entry to ensure conscious user intent
7. WHEN a HITL confirmation is required, THE HITL SHALL display the resource ID and action being confirmed
8. WHEN a HITL confirmation is aborted, THE HITL SHALL return control to the REPL without executing the action
9. THE HITL SHALL apply to all operations classified as destructive or state-changing
10. THE HITL SHALL log confirmation attempts for audit purposes

### Requirement 14: Session State Management

**User Story:** As a security analyst, I want my investigation context preserved across commands, so that I can maintain workflow continuity without re-specifying resources.

#### Acceptance Criteria

1. THE Session_State SHALL maintain the active target resource ID across multiple commands
2. WHEN the user executes "/target resource_id", THE Session_State SHALL set the active target to the specified resource
3. WHEN the user references "this instance" or "the instance", THE Session_State SHALL resolve to the active target
4. THE Session_State SHALL track per-model quota consumption including request counts and token usage
5. THE Session_State SHALL track per-model cooldown timers for rate limit management
6. WHEN the application exits, THE Session_State SHALL save state to session_state.json using atomic write pattern
7. WHEN the application starts, THE Session_State SHALL load previous state from session_state.json if it exists
8. THE Session_State SHALL encrypt session_state.json using XOR encryption with GITHUB_TOKEN as key
9. THE Session_State SHALL set file permissions to 0600 (owner read/write only) on Unix systems
10. IF the active target is None, THEN THE Session_State SHALL inject "[ACTIVE TARGET: NONE]" into the OODA prompt to prevent hallucination


### Requirement 15: Knowledge Graph Persistence

**User Story:** As a security analyst, I want audited resource information cached persistently, so that I can reference previous investigation data without re-querying AWS APIs.

#### Acceptance Criteria

1. THE Knowledge_Graph SHALL maintain a persistent cache of audited AWS resources in session_kg.json
2. WHEN the user queries a resource, THE Knowledge_Graph SHALL store the response for future reference
3. WHEN the OODA_Loop executes the Observe phase, THE Knowledge_Graph SHALL inject cached resource data into the prompt
4. THE Knowledge_Graph SHALL survive application restarts and system reboots
5. WHEN the application exits, THE Knowledge_Graph SHALL save data to session_kg.json using atomic write pattern
6. WHEN the application starts, THE Knowledge_Graph SHALL load previous data from session_kg.json if it exists
7. THE Knowledge_Graph SHALL encrypt session_kg.json using XOR encryption with GITHUB_TOKEN as key
8. THE Knowledge_Graph SHALL set file permissions to 0600 (owner read/write only) on Unix systems
9. THE Knowledge_Graph SHALL store security group rules, VPC configurations, and IAM role mappings
10. WHEN the user executes "/export", THE Knowledge_Graph SHALL export cached data for external analysis

### Requirement 16: Atomic Write Pattern for Data Integrity

**User Story:** As a system administrator, I want session files protected from corruption during power loss, so that investigation data remains recoverable.

#### Acceptance Criteria

1. WHEN writing session_state.json, THE Atomic_Write_Pattern SHALL create a temporary file using tempfile.NamedTemporaryFile
2. WHEN writing session_kg.json, THE Atomic_Write_Pattern SHALL create a temporary file using tempfile.NamedTemporaryFile
3. WHEN the temporary file write completes, THE Atomic_Write_Pattern SHALL use os.replace to atomically move the file to the target location
4. THE Atomic_Write_Pattern SHALL ensure data is never left in a partial state during write operations
5. THE Atomic_Write_Pattern SHALL prevent corruption from interrupted write operations
6. THE Atomic_Write_Pattern SHALL apply to all session file persistence operations
7. IF a write operation fails, THEN THE Atomic_Write_Pattern SHALL preserve the existing file without corruption
8. THE Atomic_Write_Pattern SHALL complete writes before the application exits
9. THE Atomic_Write_Pattern SHALL handle write failures gracefully with error messages
10. THE Atomic_Write_Pattern SHALL not use direct writes to session files

### Requirement 17: XOR Encryption for Session Files

**User Story:** As a security administrator, I want session files encrypted at rest, so that sensitive investigation data is protected from unauthorized access.

#### Acceptance Criteria

1. THE XOR_Encryption SHALL use the GITHUB_TOKEN environment variable as the encryption key
2. WHEN writing session_state.json, THE XOR_Encryption SHALL encrypt the file content before writing
3. WHEN writing session_kg.json, THE XOR_Encryption SHALL encrypt the file content before writing
4. WHEN reading session_state.json, THE XOR_Encryption SHALL decrypt the file content after reading
5. WHEN reading session_kg.json, THE XOR_Encryption SHALL decrypt the file content after reading
6. THE XOR_Encryption SHALL apply byte-wise XOR operation between plaintext and key
7. THE XOR_Encryption SHALL handle key length mismatches by repeating the key cyclically
8. IF the GITHUB_TOKEN is not set, THEN THE XOR_Encryption SHALL fail with a clear error message
9. THE XOR_Encryption SHALL prevent plaintext storage of session data
10. THE XOR_Encryption SHALL maintain data integrity through encryption/decryption cycles

### Requirement 18: Lazy Client Factory for AWS SDK

**User Story:** As a system architect, I want AWS clients cached and reused, so that the system avoids unnecessary client recreation overhead.

#### Acceptance Criteria

1. THE Lazy_Client_Factory SHALL implement the _client(service) function for AWS client management
2. WHEN a service client is requested, THE Lazy_Client_Factory SHALL check if the client already exists in the cache
3. IF the client exists in the cache, THEN THE Lazy_Client_Factory SHALL return the cached client
4. IF the client does not exist in the cache, THEN THE Lazy_Client_Factory SHALL create a new client and cache it
5. THE Lazy_Client_Factory SHALL support exactly 14 AWS services: ec2, iam, s3, logs, rds, lambda, cloudwatch, cloudtrail, ce, guardduty, kms, dynamodb, efs, wafv2
6. IF an unsupported service is requested, THEN THE Lazy_Client_Factory SHALL raise a ValueError with a descriptive message
7. THE Lazy_Client_Factory SHALL maintain a single client instance per service for the application lifetime
8. THE Lazy_Client_Factory SHALL use explicit elif branches for each supported service
9. THE Lazy_Client_Factory SHALL not use catch-all else clauses that silently create arbitrary clients
10. THE Lazy_Client_Factory SHALL configure clients with appropriate region and credential settings

### Requirement 19: Paste Guard for Terminal Buffer Protection

**User Story:** As a security administrator, I want the system protected from terminal paste attacks, so that multi-line bursts cannot cause token-burning loops.

#### Acceptance Criteria

1. THE Paste_Guard SHALL use non-blocking I/O to poll the terminal input buffer
2. WHEN the REPL reads user input, THE Paste_Guard SHALL check for multi-line bursts in the buffer
3. IF a multi-line burst is detected, THEN THE Paste_Guard SHALL trigger universal_flush to drain the buffer
4. THE Paste_Guard SHALL use select.select with 0.0 timeout on Unix systems for non-blocking polling
5. THE Paste_Guard SHALL use msvcrt.kbhit on Windows systems for non-blocking polling
6. WHEN universal_flush is triggered, THE Paste_Guard SHALL enforce a 0.2 second physical buffer drain
7. THE Paste_Guard SHALL prevent rapid buffer fills from reaching the LLM
8. THE Paste_Guard SHALL discard runaway stdin data before it causes processing overhead
9. THE Paste_Guard SHALL maintain REPL responsiveness during normal single-line input
10. THE Paste_Guard SHALL apply to all user input operations in the REPL

### Requirement 20: Skeptical Architecture for API Resilience

**User Story:** As a system architect, I want the system to handle API rate limiting robustly, so that operations continue reliably despite provider saturation.

#### Acceptance Criteria

1. THE Skeptical_Architecture SHALL assume API provider headers are misleading during saturation
2. WHEN a 429 rate limit response occurs, THE Adaptive_Triage SHALL enforce a mandatory 60-second safety floor
3. WHEN a second consecutive 429 occurs, THE Adaptive_Triage SHALL escalate the cooldown to 120 seconds
4. THE Adaptive_Triage SHALL recognize severe "Window Contamination" and adjust cooldown accordingly
5. THE Skeptical_Architecture SHALL implement exponential backoff with deterministic ladder: 2s, 4s, 8s, 16s, 32s
6. THE Skeptical_Architecture SHALL cap exponential backoff at 32 seconds maximum
7. WHEN a cooldown is active, THE Skeptical_Architecture SHALL display remaining time to the user
8. WHEN a cooldown expires, THE Skeptical_Architecture SHALL allow the model to be used again
9. THE Skeptical_Architecture SHALL track cooldowns per model independently
10. WHEN all models are in cooldown, THE Skeptical_Architecture SHALL display an exhausted summary with reset times


### Requirement 21: Error Handling and Resilience

**User Story:** As a security analyst, I want clear error messages for all failure conditions, so that I can understand and resolve issues quickly.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL never use bare except clauses without specific exception types
2. WHEN a Boto3 error occurs, THE Zero_Shield_CLI SHALL catch boto3.exceptions.Boto3Error and display a descriptive message
3. WHEN an OpenAI API error occurs, THE Zero_Shield_CLI SHALL catch openai.OpenAIError and display a descriptive message
4. WHEN a data validation error occurs, THE Zero_Shield_CLI SHALL catch KeyError or ValueError and display a descriptive message
5. WHEN an AWS API returns an error, THE Zero_Shield_CLI SHALL extract and display the error code and message
6. WHEN a resource is not found, THE Zero_Shield_CLI SHALL display a clear "Resource not found" message with the resource ID
7. WHEN an access denied error occurs, THE Zero_Shield_CLI SHALL display a message suggesting IAM policy review
8. WHEN a network error occurs, THE Zero_Shield_CLI SHALL display a message indicating connectivity issues
9. THE Zero_Shield_CLI SHALL never return empty strings or None for error conditions
10. THE Zero_Shield_CLI SHALL log all errors with sufficient context for debugging

### Requirement 22: Cross-Platform Compatibility

**User Story:** As a security analyst, I want to run Zero-Shield CLI on multiple platforms, so that I can use it in my preferred environment.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL support Python 3.9 and higher versions
2. THE Zero_Shield_CLI SHALL run on Unix/Linux systems with full terminal I/O support using termios
3. THE Zero_Shield_CLI SHALL run on Windows systems with full terminal I/O support using msvcrt
4. THE Zero_Shield_CLI SHALL run on AWS CloudShell with native IAM role credential inheritance
5. WHEN running on Windows, THE Zero_Shield_CLI SHALL enable ANSI color codes via ctypes
6. WHEN running on Unix systems, THE Zero_Shield_CLI SHALL set session file permissions to 0600
7. THE Zero_Shield_CLI SHALL enforce UTF-8 encoding for cross-platform text compatibility
8. THE Zero_Shield_CLI SHALL handle platform-specific path separators correctly
9. THE Zero_Shield_CLI SHALL detect the operating system and use appropriate I/O mechanisms
10. THE Zero_Shield_CLI SHALL provide consistent functionality across all supported platforms

### Requirement 23: Environment Configuration

**User Story:** As a system administrator, I want to configure the application via environment variables, so that I can deploy it securely without hardcoding credentials.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL require the GITHUB_TOKEN environment variable for LLM API authentication
2. THE Zero_Shield_CLI SHALL require AWS credentials via environment variables, IAM role, or AWS CLI configuration
3. THE Zero_Shield_CLI SHALL require the QUARANTINE_SG_ID environment variable for quarantine operations
4. THE Zero_Shield_CLI SHALL support the GITHUB_MODELS_URL environment variable for custom LLM endpoints
5. WHEN GITHUB_TOKEN is not set, THE Zero_Shield_CLI SHALL display an error and exit
6. WHEN AWS credentials are not available, THE Zero_Shield_CLI SHALL display an error and exit
7. WHEN QUARANTINE_SG_ID is not set, THE Zero_Shield_CLI SHALL display a warning but allow non-quarantine operations
8. THE Zero_Shield_CLI SHALL load environment variables from a .env file using python-dotenv
9. THE Zero_Shield_CLI SHALL never log or display the GITHUB_TOKEN value
10. THE Zero_Shield_CLI SHALL validate required environment variables during preflight checks

### Requirement 24: Preflight Validation

**User Story:** As a security analyst, I want the system to validate configuration before starting, so that I can identify setup issues immediately.

#### Acceptance Criteria

1. WHEN the application starts, THE Zero_Shield_CLI SHALL execute run_preflight to validate configuration
2. WHEN run_preflight executes, THE Zero_Shield_CLI SHALL verify the GITHUB_TOKEN environment variable is set
3. WHEN run_preflight executes, THE Zero_Shield_CLI SHALL verify AWS credentials are available
4. WHEN run_preflight executes, THE Zero_Shield_CLI SHALL test AWS API connectivity by listing EC2 instances
5. WHEN run_preflight executes, THE Zero_Shield_CLI SHALL test GitHub Models API connectivity
6. IF preflight validation fails, THEN THE Zero_Shield_CLI SHALL display a clear error message and exit
7. IF preflight validation succeeds, THEN THE Zero_Shield_CLI SHALL display a success message
8. THE Zero_Shield_CLI SHALL display the AWS region being used during preflight
9. THE Zero_Shield_CLI SHALL display the number of available LLM models during preflight
10. THE Zero_Shield_CLI SHALL complete preflight validation before entering the REPL

### Requirement 25: Target Context Management

**User Story:** As a security analyst, I want to set and maintain an active target resource, so that I can issue context-aware commands without repeating resource IDs.

#### Acceptance Criteria

1. THE Target_Context SHALL maintain the last_id variable for the active resource
2. WHEN the user executes "/target resource_id", THE Target_Context SHALL set last_id to the specified resource
3. WHEN the user executes [ACTION:INSPECT:resource_id], THE Target_Context SHALL set last_id to the inspected resource
4. WHEN the user references "this instance" or "the instance", THE Target_Context SHALL resolve to last_id
5. IF last_id is None, THEN THE Target_Context SHALL inject "[ACTIVE TARGET: NONE]" into the OODA prompt
6. THE Target_Context SHALL prevent the LLM from assuming targets from training data when last_id is None
7. THE Target_Context SHALL display the active target in "/status" command output
8. THE Target_Context SHALL persist last_id in session_state.json across application restarts
9. THE Target_Context SHALL allow the user to clear the active target with "/target none"
10. THE Target_Context SHALL enforce the "Target-First" operational doctrine

### Requirement 26: Security Group Risk Assessment

**User Story:** As a security analyst, I want automatic risk assessment of security group rules, so that I can quickly identify dangerous configurations.

#### Acceptance Criteria

1. WHEN analyzing security group rules, THE Zero_Shield_CLI SHALL identify rules allowing 0.0.0.0/0 as public internet exposure
2. WHEN analyzing security group rules, THE Zero_Shield_CLI SHALL distinguish RFC 1918 private CIDR blocks (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) from public IPs
3. WHEN analyzing security group rules, THE Zero_Shield_CLI SHALL flag SSH (port 22) open to 0.0.0.0/0 as high risk
4. WHEN analyzing security group rules, THE Zero_Shield_CLI SHALL flag RDP (port 3389) open to 0.0.0.0/0 as high risk
5. WHEN analyzing security group rules, THE Zero_Shield_CLI SHALL provide auto-remediation hints for risky configurations
6. THE Zero_Shield_CLI SHALL implement the is_private_cidr function to check if a CIDR block is private
7. THE Zero_Shield_CLI SHALL implement the auto_remediation_hint function to suggest fixes for risky rules
8. THE Zero_Shield_CLI SHALL implement the interpret_sg_rules function to provide human-readable rule analysis
9. WHEN displaying security group rules, THE Zero_Shield_CLI SHALL use color coding: green for safe, yellow for warning, red for risky
10. THE Zero_Shield_CLI SHALL eliminate noise from VPC-internal rules when assessing internet exposure


### Requirement 27: Quota and Rate Limit Tracking

**User Story:** As a security analyst, I want to see API quota consumption and rate limits, so that I can manage my usage and avoid service interruptions.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL track per-model request counts for quota monitoring
2. THE Zero_Shield_CLI SHALL track per-model token consumption for quota monitoring
3. WHEN an API response includes rate limit headers, THE Zero_Shield_CLI SHALL extract and store quota information
4. WHEN displaying model selection, THE Zero_Shield_CLI SHALL show request quota bars for each model
5. WHEN displaying model selection, THE Zero_Shield_CLI SHALL show token quota bars for each model
6. WHEN displaying model selection, THE Zero_Shield_CLI SHALL show cooldown reset times for rate-limited models
7. THE Zero_Shield_CLI SHALL implement _update_quota_from_headers to parse API response headers
8. THE Zero_Shield_CLI SHALL implement _quota_req_bar to display request quota as a progress bar
9. THE Zero_Shield_CLI SHALL implement _quota_tok_bar to display token quota as a progress bar
10. WHEN a model is rate-limited, THE Zero_Shield_CLI SHALL display the remaining cooldown time in the quota table

### Requirement 28: Conversation History Management

**User Story:** As a security analyst, I want to manage conversation history, so that I can maintain context or start fresh as needed.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL maintain conversation history across multiple turns within a session
2. WHEN the user enters "/clear", THE Zero_Shield_CLI SHALL reset conversation history to empty
3. WHEN the user enters "/clear", THE Zero_Shield_CLI SHALL preserve session state and Knowledge_Graph
4. WHEN switching models, THE Zero_Shield_CLI SHALL optionally roll back conversation history to prevent corrupted context
5. THE Zero_Shield_CLI SHALL implement context cleanse (air-gap) to strip corrupted or hallucinated messages
6. THE Zero_Shield_CLI SHALL cache the last user input for replay when switching models
7. WHEN replaying input to a new model, THE Zero_Shield_CLI SHALL provide clean context without previous model's responses
8. THE Zero_Shield_CLI SHALL limit conversation history to prevent context window overflow
9. THE Zero_Shield_CLI SHALL estimate token usage for conversation history using the estimate_tokens function
10. WHEN conversation history approaches context window limits, THE Zero_Shield_CLI SHALL warn the user

### Requirement 29: Action Detection and Parsing

**User Story:** As a system architect, I want LLM responses parsed for action commands, so that the system can execute AWS operations deterministically.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the detect_action function to parse [ACTION:TAG] patterns from LLM responses
2. WHEN an LLM response contains [ACTION:LIST], THE Zero_Shield_CLI SHALL execute tool_list_resources
3. WHEN an LLM response contains [ACTION:INSPECT:resource_id], THE Zero_Shield_CLI SHALL execute tool_inspect_resource with the specified resource ID
4. WHEN an LLM response contains [ACTION:SG_RULES:sg_id], THE Zero_Shield_CLI SHALL execute tool_sg_rules with the specified security group ID
5. THE Zero_Shield_CLI SHALL support 32 distinct action patterns corresponding to all AWS operations
6. THE Zero_Shield_CLI SHALL extract resource IDs from action tags using regex pattern matching
7. IF an action tag is malformed, THEN THE Zero_Shield_CLI SHALL display an error and not execute the action
8. THE Zero_Shield_CLI SHALL validate resource ID formats before executing actions
9. THE Zero_Shield_CLI SHALL log all detected actions for audit purposes
10. THE Zero_Shield_CLI SHALL feed action execution results back into the OODA observation loop

### Requirement 30: Spinner and Progress Indication

**User Story:** As a security analyst, I want visual feedback during long-running operations, so that I know the system is working.

#### Acceptance Criteria

1. WHEN making an LLM API call, THE Zero_Shield_CLI SHALL display an animated spinner
2. WHEN making an AWS API call, THE Zero_Shield_CLI SHALL display an animated spinner
3. THE Zero_Shield_CLI SHALL implement spinner_start to begin spinner animation in a separate thread
4. THE Zero_Shield_CLI SHALL implement spinner_stop to terminate spinner animation
5. THE Zero_Shield_CLI SHALL use a rotating character sequence for spinner animation: |, /, -, \\
6. WHEN an operation completes, THE Zero_Shield_CLI SHALL stop the spinner and clear the spinner line
7. THE Zero_Shield_CLI SHALL display operation status after spinner stops: success, error, or warning
8. THE Zero_Shield_CLI SHALL not interfere with normal output during spinner operation
9. THE Zero_Shield_CLI SHALL handle spinner thread cleanup gracefully on errors
10. THE Zero_Shield_CLI SHALL provide visual feedback for operations taking longer than 1 second

### Requirement 31: Color-Coded Output Formatting

**User Story:** As a security analyst, I want color-coded output, so that I can quickly identify success, errors, warnings, and information.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the Colors class with ANSI color code constants
2. THE Zero_Shield_CLI SHALL display success messages in green using print_success
3. THE Zero_Shield_CLI SHALL display error messages in red using print_error
4. THE Zero_Shield_CLI SHALL display warning messages in yellow using print_warning
5. THE Zero_Shield_CLI SHALL display informational messages in cyan using print_info
6. THE Zero_Shield_CLI SHALL implement colorize function to apply color codes to text
7. THE Zero_Shield_CLI SHALL implement Colors.strip to remove color codes from text for logging
8. WHEN running on Windows, THE Zero_Shield_CLI SHALL enable ANSI color support via ctypes
9. THE Zero_Shield_CLI SHALL use color coding consistently across all output types
10. THE Zero_Shield_CLI SHALL provide a monochrome fallback if color support is unavailable

### Requirement 32: Table and Banner Formatting

**User Story:** As a security analyst, I want well-formatted tables and banners, so that information is easy to read and understand.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement print_banner to display the application welcome banner
2. THE Zero_Shield_CLI SHALL implement print_header to display section headers with borders
3. THE Zero_Shield_CLI SHALL implement print_section to display subsection titles
4. THE Zero_Shield_CLI SHALL implement print_table_row to display formatted table rows with column alignment
5. THE Zero_Shield_CLI SHALL implement progress_bar to display progress indicators with percentage
6. WHEN displaying the welcome banner, THE Zero_Shield_CLI SHALL include version information and copyright
7. WHEN displaying tables, THE Zero_Shield_CLI SHALL align columns consistently with appropriate widths
8. WHEN displaying tables, THE Zero_Shield_CLI SHALL support optional color coding per column
9. THE Zero_Shield_CLI SHALL use box-drawing characters for visual separation in tables
10. THE Zero_Shield_CLI SHALL format all structured output using consistent table and banner styles

### Requirement 33: Signal Handling and Graceful Shutdown

**User Story:** As a security analyst, I want the application to save state when I interrupt it, so that I don't lose investigation progress.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL register a SIGINT handler using signal.signal
2. WHEN the user presses Ctrl+C, THE Zero_Shield_CLI SHALL catch the SIGINT signal
3. WHEN SIGINT is caught, THE Zero_Shield_CLI SHALL save session state using state_save
4. WHEN SIGINT is caught, THE Zero_Shield_CLI SHALL save Knowledge_Graph using kg_save
5. WHEN SIGINT is caught, THE Zero_Shield_CLI SHALL display a goodbye message
6. WHEN SIGINT is caught, THE Zero_Shield_CLI SHALL exit with status code 0
7. THE Zero_Shield_CLI SHALL implement _handle_sigint function for signal handling
8. THE Zero_Shield_CLI SHALL ensure all file writes complete before exit
9. THE Zero_Shield_CLI SHALL handle multiple SIGINT signals gracefully
10. THE Zero_Shield_CLI SHALL not leave session files in corrupted state on interrupt


### Requirement 34: Testing and Validation

**User Story:** As a developer, I want comprehensive test coverage, so that I can verify system correctness and prevent regressions.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL include a security test suite with 35 tests covering credential redaction, HITL, and encryption
2. THE Zero_Shield_CLI SHALL include an integration test suite with 66 tests covering all functionality (using mocked AWS responses)
3. WHEN security tests execute, THE Zero_Shield_CLI SHALL verify all 5 layers of credential redaction
4. WHEN security tests execute, THE Zero_Shield_CLI SHALL verify HITL confirmation mechanisms
5. WHEN security tests execute, THE Zero_Shield_CLI SHALL verify XOR encryption for session files
6. WHEN security tests execute, THE Zero_Shield_CLI SHALL verify prompt injection prevention via _sanitize_aws_tag
7. WHEN comprehensive tests execute, THE Zero_Shield_CLI SHALL verify all 32 AWS action functions
8. WHEN comprehensive tests execute, THE Zero_Shield_CLI SHALL verify OODA loop formatting enforcement
9. WHEN comprehensive tests execute, THE Zero_Shield_CLI SHALL verify multi-model LLM support
10. THE Zero_Shield_CLI SHALL achieve 100% test pass rate before release

### Requirement 35: Documentation and Audit Standards

**User Story:** As a system administrator, I want comprehensive documentation, so that I can deploy, operate, and maintain the system effectively.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL provide user documentation including quick start guides for CloudShell and local deployment
2. THE Zero_Shield_CLI SHALL provide administrator documentation including deployment, monitoring, security, troubleshooting, maintenance, and backup/recovery guides
3. THE Zero_Shield_CLI SHALL provide architecture documentation including OODA loop details and technical architecture
4. THE Zero_Shield_CLI SHALL provide a complete command reference documenting all 32 AWS actions
5. THE Zero_Shield_CLI SHALL provide real-world usage examples for common security scenarios
6. THE Zero_Shield_CLI SHALL provide IAM policy documentation with 3 policy tiers: minimal, standard, and full
7. THE Zero_Shield_CLI SHALL provide validation reports documenting security audits, code quality, and synchronization verification
8. THE Zero_Shield_CLI SHALL maintain a commit-based changelog documenting all changes
9. THE Zero_Shield_CLI SHALL provide contribution guidelines for developers
10. THE Zero_Shield_CLI SHALL ensure all documentation metrics match actual code implementation

### Requirement 36: Deployment Automation

**User Story:** As a system administrator, I want automated deployment scripts, so that I can deploy the system quickly and reliably.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL provide a deploy_to_cloudshell.sh script for AWS CloudShell deployment
2. WHEN the deployment script executes, THE deployment script SHALL create backups of existing files
3. WHEN the deployment script executes, THE deployment script SHALL verify environment configuration
4. WHEN the deployment script executes, THE deployment script SHALL run security validation tests
5. WHEN the deployment script executes, THE deployment script SHALL display a comprehensive deployment summary
6. THE deployment script SHALL implement a 5-step deployment process
7. THE deployment script SHALL verify Python dependencies are installed
8. THE deployment script SHALL verify AWS credentials are configured
9. THE deployment script SHALL verify the GITHUB_TOKEN environment variable is set
10. IF deployment validation fails, THEN THE deployment script SHALL display clear error messages and exit

### Requirement 37: IAM Policy Management

**User Story:** As a security administrator, I want tiered IAM policies, so that I can grant appropriate permissions based on operational requirements.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL provide a minimal IAM policy for read-only investigation operations
2. THE Zero_Shield_CLI SHALL provide a standard IAM policy for common security operations
3. THE Zero_Shield_CLI SHALL provide a full IAM policy for complete functionality including destructive actions
4. THE minimal IAM policy SHALL grant permissions for LIST, INSPECT, and audit operations only
5. THE standard IAM policy SHALL grant permissions for all read operations plus non-destructive modifications
6. THE full IAM policy SHALL grant permissions for all operations including QUARANTINE and DEACTIVATE_ACCESS_KEY
7. THE Zero_Shield_CLI SHALL provide production IAM policy examples for audit and remediation separation
8. THE Zero_Shield_CLI SHALL document required permissions for each AWS action
9. THE Zero_Shield_CLI SHALL provide IAM setup guides for CloudShell and local environments
10. THE Zero_Shield_CLI SHALL verify IAM permissions during preflight checks

### Requirement 38: Snapshot Data Injection

**User Story:** As a system architect, I want live AWS data injected into the OODA Observe phase, so that the LLM has current environment context.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the fetch_snapshot function to retrieve live AWS data
2. WHEN the OODA_Loop executes the Observe phase, THE Zero_Shield_CLI SHALL call fetch_snapshot to retrieve current EC2 instances
3. WHEN the OODA_Loop executes the Observe phase, THE Zero_Shield_CLI SHALL inject snapshot data into the system prompt
4. THE snapshot data SHALL include instance IDs, names, states, types, and IP addresses
5. THE snapshot data SHALL be sanitized through _sanitize_aws_tag before injection
6. THE snapshot data SHALL be combined with Knowledge_Graph data for comprehensive context
7. THE Zero_Shield_CLI SHALL implement build_sg_map to create security group mappings from snapshot data
8. THE Zero_Shield_CLI SHALL implement resolve_target to resolve resource references from snapshot data
9. THE Zero_Shield_CLI SHALL implement format_kg to format Knowledge_Graph data for prompt injection
10. THE snapshot data SHALL be refreshed on each OODA loop iteration

### Requirement 39: System Prompt Construction

**User Story:** As a system architect, I want dynamic system prompts constructed with current context, so that the LLM has all necessary information for decision-making.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the build_sys_msg function to construct system prompts
2. WHEN building a system prompt, THE Zero_Shield_CLI SHALL include the OODA loop framework instructions
3. WHEN building a system prompt, THE Zero_Shield_CLI SHALL include live AWS snapshot data
4. WHEN building a system prompt, THE Zero_Shield_CLI SHALL include Knowledge_Graph context
5. WHEN building a system prompt, THE Zero_Shield_CLI SHALL include the active target resource ID
6. WHEN building a system prompt, THE Zero_Shield_CLI SHALL include model-specific instructions
7. WHEN building a system prompt, THE Zero_Shield_CLI SHALL include the [STRICT_COMPLIANCE_PROTOCOL] anchor
8. WHEN the active target is None, THE Zero_Shield_CLI SHALL include "[ACTIVE TARGET: NONE]" warning
9. THE system prompt SHALL enforce the "Target-First" operational doctrine
10. THE system prompt SHALL include all 32 available AWS actions with their formats

### Requirement 40: Model-Specific Optimization

**User Story:** As a system architect, I want model-specific optimizations, so that each LLM performs optimally for its characteristics.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL provide model-specific tips via the show_model_tips function
2. WHEN Phi-4 is selected, THE Zero_Shield_CLI SHALL display compliance-focused usage tips
3. WHEN gpt-4o is selected, THE Zero_Shield_CLI SHALL display capability-focused usage tips
4. WHEN Llama-3.3-70B is selected, THE Zero_Shield_CLI SHALL display reasoning-focused usage tips
5. WHEN DeepSeek-V3 is selected, THE Zero_Shield_CLI SHALL display analysis-focused usage tips
6. WHEN gpt-4o-mini is selected, THE Zero_Shield_CLI SHALL display speed-focused usage tips
7. THE Zero_Shield_CLI SHALL adjust system prompt complexity based on model context window size
8. THE Zero_Shield_CLI SHALL track model-specific performance characteristics
9. THE Zero_Shield_CLI SHALL recommend model switches based on task requirements
10. THE Zero_Shield_CLI SHALL display model characteristics in the selection interface


### Requirement 41: Path Sanitization

**User Story:** As a security administrator, I want file paths sanitized, so that the system is protected from path traversal attacks.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the _sanitize_path function for file path validation
2. WHEN processing file paths, THE _sanitize_path function SHALL remove parent directory references ".."
3. WHEN processing file paths, THE _sanitize_path function SHALL remove absolute path indicators
4. WHEN processing file paths, THE _sanitize_path function SHALL validate paths are within allowed directories
5. THE _sanitize_path function SHALL prevent path traversal attacks
6. THE _sanitize_path function SHALL apply to all user-provided file paths
7. THE _sanitize_path function SHALL apply to all file export operations
8. IF a path fails sanitization, THEN THE _sanitize_path function SHALL raise a ValueError
9. THE _sanitize_path function SHALL preserve legitimate relative paths
10. THE _sanitize_path function SHALL log path sanitization attempts for audit purposes

### Requirement 42: Log Sanitization

**User Story:** As a security administrator, I want CloudWatch logs sanitized, so that sensitive data in logs is redacted before display.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the _sanitize_logs function for log content sanitization
2. WHEN retrieving CloudWatch logs, THE _sanitize_logs function SHALL apply credential redaction
3. WHEN retrieving CloudWatch logs, THE _sanitize_logs function SHALL remove sensitive patterns
4. THE _sanitize_logs function SHALL apply before logs are displayed to the user
5. THE _sanitize_logs function SHALL preserve log structure and readability
6. THE _sanitize_logs function SHALL handle multi-line log entries correctly
7. THE _sanitize_logs function SHALL apply to all log retrieval operations
8. THE _sanitize_logs function SHALL not modify original log data in CloudWatch
9. THE _sanitize_logs function SHALL redact AWS credentials found in log content
10. THE _sanitize_logs function SHALL redact API keys and tokens found in log content

### Requirement 43: Timestamp Formatting

**User Story:** As a security analyst, I want consistent timestamp formatting, so that I can correlate events across different outputs.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the ts function for timestamp generation
2. WHEN generating timestamps, THE ts function SHALL use ISO 8601 format
3. WHEN generating timestamps, THE ts function SHALL include date, time, and timezone
4. THE ts function SHALL use UTC timezone for consistency
5. THE ts function SHALL apply to all event logging operations
6. THE ts function SHALL apply to all audit trail entries
7. THE ts function SHALL provide millisecond precision when available
8. THE ts function SHALL format timestamps consistently across all outputs
9. THE ts function SHALL handle timezone conversions correctly
10. THE ts function SHALL be used for all time-based operations

### Requirement 44: Cooldown Management

**User Story:** As a system architect, I want rate limit cooldowns managed automatically, so that the system respects API limits without manual intervention.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement _parse_cooldown_headers to extract rate limit information from API responses
2. THE Zero_Shield_CLI SHALL implement _record_cooldown to store cooldown timers per model
3. WHEN a 429 rate limit response occurs, THE Zero_Shield_CLI SHALL parse the Retry-After header
4. WHEN a 429 rate limit response occurs, THE Zero_Shield_CLI SHALL record the cooldown with the safety floor applied
5. WHEN a model is in cooldown, THE Zero_Shield_CLI SHALL prevent API calls to that model
6. WHEN a model is in cooldown, THE Zero_Shield_CLI SHALL display remaining cooldown time
7. WHEN a cooldown expires, THE Zero_Shield_CLI SHALL automatically re-enable the model
8. THE Zero_Shield_CLI SHALL implement _print_exhausted_summary to display all model cooldown states
9. THE Zero_Shield_CLI SHALL track cooldown expiration times per model
10. THE Zero_Shield_CLI SHALL persist cooldown state in session_state.json

### Requirement 45: Model Selection Interface

**User Story:** As a security analyst, I want an intuitive model selection interface, so that I can choose the best LLM for my current task.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the select_model function for interactive model selection
2. THE Zero_Shield_CLI SHALL implement print_quota_table to display model status and quotas
3. WHEN displaying model selection, THE Zero_Shield_CLI SHALL show all 5 available models
4. WHEN displaying model selection, THE Zero_Shield_CLI SHALL show request quota status for each model
5. WHEN displaying model selection, THE Zero_Shield_CLI SHALL show token quota status for each model
6. WHEN displaying model selection, THE Zero_Shield_CLI SHALL show cooldown status for rate-limited models
7. WHEN displaying model selection, THE Zero_Shield_CLI SHALL highlight available models in green
8. WHEN displaying model selection, THE Zero_Shield_CLI SHALL highlight rate-limited models in red
9. THE model selection interface SHALL accept numeric input (1-5) to select a model
10. THE model selection interface SHALL validate user input and reject invalid selections

### Requirement 46: API Call Execution

**User Story:** As a system architect, I want robust API call execution with retry logic, so that transient failures don't disrupt operations.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the call_model function for LLM API calls
2. WHEN making an LLM API call, THE call_model function SHALL display a spinner during execution
3. WHEN making an LLM API call, THE call_model function SHALL handle rate limiting with exponential backoff
4. WHEN making an LLM API call, THE call_model function SHALL catch and handle API errors gracefully
5. WHEN an API call fails with a retryable error, THE call_model function SHALL retry with exponential backoff
6. WHEN an API call fails with a non-retryable error, THE call_model function SHALL display an error and return
7. THE call_model function SHALL update quota information from API response headers
8. THE call_model function SHALL record cooldowns when rate limits are encountered
9. THE call_model function SHALL estimate and track token usage for quota management
10. THE call_model function SHALL return the LLM response or None on failure

### Requirement 47: Main CLI Loop

**User Story:** As a system architect, I want a robust main CLI loop, so that the REPL handles all user interactions reliably.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL implement the run_cli function as the main REPL loop
2. WHEN run_cli starts, THE Zero_Shield_CLI SHALL load session state and Knowledge_Graph
3. WHEN run_cli starts, THE Zero_Shield_CLI SHALL execute preflight validation
4. WHEN run_cli starts, THE Zero_Shield_CLI SHALL prompt for model selection
5. WHEN run_cli starts, THE Zero_Shield_CLI SHALL display the welcome banner
6. WHILE run_cli is active, THE Zero_Shield_CLI SHALL continuously accept user input
7. WHEN the user enters a command, THE run_cli function SHALL process it through the OODA loop
8. WHEN the user enters a system command, THE run_cli function SHALL execute the corresponding meta-operation
9. WHEN the user exits, THE run_cli function SHALL save session state and Knowledge_Graph
10. THE run_cli function SHALL handle all exceptions gracefully and maintain REPL stability

### Requirement 48: Version Information

**User Story:** As a system administrator, I want version information displayed, so that I can track which version is deployed.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL display version "v2.0.0-dev" in the welcome banner
2. THE Zero_Shield_CLI SHALL display version information in the "/status" command output
3. THE Zero_Shield_CLI SHALL include version information in all error reports
4. THE Zero_Shield_CLI SHALL maintain version consistency across all 5 locations in code
5. THE version string SHALL indicate development status with "-dev" suffix
6. THE version string SHALL follow semantic versioning format
7. THE version string SHALL be updated for each release
8. THE version string SHALL be documented in CHANGELOG.md
9. THE version string SHALL match the git branch naming convention
10. THE version string SHALL be verified during documentation audits

### Requirement 49: Dependency Management

**User Story:** As a system administrator, I want pinned dependency versions, so that deployments are reproducible and stable.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL specify openai==2.24.0 in requirements.txt
2. THE Zero_Shield_CLI SHALL specify boto3==1.42.1 in requirements.txt
3. THE Zero_Shield_CLI SHALL specify python-dotenv==1.2.1 in requirements.txt
4. THE Zero_Shield_CLI SHALL specify httpx>=0.24.0 in requirements.txt
5. THE requirements.txt file SHALL use exact version pinning for critical dependencies
6. THE requirements.txt file SHALL use minimum version constraints for flexible dependencies
7. THE Zero_Shield_CLI SHALL verify all dependencies are installed during preflight
8. THE Zero_Shield_CLI SHALL display clear error messages for missing dependencies
9. THE Zero_Shield_CLI SHALL document dependency installation in setup guides
10. THE Zero_Shield_CLI SHALL test with specified dependency versions before release


### Requirement 50: Parser and Serializer Requirements

**User Story:** As a system architect, I want robust parsing and serialization of session data, so that state is preserved correctly across restarts.

#### Acceptance Criteria

1. THE Zero_Shield_CLI SHALL parse session_state.json using JSON parser
2. THE Zero_Shield_CLI SHALL parse session_kg.json using JSON parser
3. THE Zero_Shield_CLI SHALL serialize session state to JSON format before encryption
4. THE Zero_Shield_CLI SHALL serialize Knowledge_Graph to JSON format before encryption
5. THE Zero_Shield_CLI SHALL implement a pretty printer for JSON session files
6. FOR ALL valid session state objects, parsing then serializing then parsing SHALL produce an equivalent object (round-trip property)
7. FOR ALL valid Knowledge_Graph objects, parsing then serializing then parsing SHALL produce an equivalent object (round-trip property)
8. WHEN parsing fails, THE Zero_Shield_CLI SHALL display a descriptive error message
9. WHEN serialization fails, THE Zero_Shield_CLI SHALL display a descriptive error message
10. THE Zero_Shield_CLI SHALL validate JSON structure after parsing and before use

---

## Special Requirements Guidance

### Parser and Serializer Testing

The session state and Knowledge_Graph persistence mechanisms are critical for system reliability. The following testing requirements are ESSENTIAL:

**Session State Parser Requirements:**
- Parse session_state.json into SessionState object
- Handle missing or corrupted files gracefully
- Validate all required fields exist after parsing
- Round-trip property: parse → serialize → parse produces equivalent object

**Knowledge Graph Parser Requirements:**
- Parse session_kg.json into KnowledgeGraph object
- Handle missing or corrupted files gracefully
- Validate graph structure after parsing
- Round-trip property: parse → serialize → parse produces equivalent object

**Pretty Printer Requirements:**
- Format SessionState objects back into valid JSON
- Format KnowledgeGraph objects back into valid JSON
- Maintain data integrity through formatting
- Produce human-readable output for debugging

**Round-Trip Testing:**
This is ESSENTIAL - parsers are tricky and round-trip testing catches bugs. The system MUST verify that:
```
FOR ALL valid SessionState objects:
  parse(serialize(state)) == state

FOR ALL valid KnowledgeGraph objects:
  parse(serialize(kg)) == kg
```

### Encryption and Serialization Order

The correct order of operations for session file persistence is:
1. Serialize object to JSON string
2. Encrypt JSON string using XOR encryption
3. Write encrypted data using atomic write pattern

The correct order for session file loading is:
1. Read encrypted data from file
2. Decrypt data using XOR encryption
3. Parse JSON string to object

This ordering ensures data integrity and security throughout the persistence lifecycle.

---

## Acceptance Criteria Testing Patterns

The following testing patterns should be applied to verify acceptance criteria:

### 1. Invariants
Properties that remain constant despite changes:
- Session state structure preserved after save/load cycle
- Knowledge_Graph contents preserved after encryption/decryption
- OODA loop formatting maintained across all responses
- Credential redaction applied to all outputs

### 2. Round Trip Properties
Operations with inverses that return to original value:
- parse(serialize(session_state)) == session_state
- decrypt(encrypt(data, key), key) == data
- load(save(state)) == state

### 3. Idempotence
Operations where doing it twice equals doing it once:
- Applying credential redaction multiple times produces same result
- Sanitizing AWS tags multiple times produces same result
- Setting the same target multiple times produces same state

### 4. Metamorphic Properties
Relationships that must hold between components:
- len(redacted_text) <= len(original_text)
- All [ACTION:TAG] patterns detected must be valid AWS actions
- All HITL confirmations must match exact resource IDs

### 5. Error Conditions
Generate bad inputs and ensure proper error handling:
- Invalid resource IDs should return descriptive errors
- Missing environment variables should fail preflight
- Malformed JSON should fail parsing with clear messages
- Invalid action tags should not execute operations

### 6. Security Properties
Critical security invariants that must always hold:
- No AWS credentials appear in any output
- All destructive actions require HITL confirmation
- Session files are always encrypted at rest
- All AWS resource metadata is sanitized before LLM processing

---

## Requirements Summary

This requirements document captures the complete Zero-Shield CLI system with 50 comprehensive requirements covering:

- **Core REPL Functionality** (Requirements 1, 47): Interactive command-line interface with natural language processing
- **OODA Loop Implementation** (Requirement 2): Deterministic cognitive cycle for all operations
- **AWS Service Integration** (Requirements 3-9): 32 actions across 14 AWS service categories
- **LLM Integration** (Requirements 10, 40): Multi-model support with 5 LLM options
- **Security Features** (Requirements 11-13, 41-42): 5-layer credential redaction, prompt injection prevention, HITL confirmations
- **Memory Management** (Requirements 14-17, 50): Dual-layer persistence with encryption and atomic writes
- **AWS SDK Integration** (Requirement 18): Lazy client factory for efficient resource management
- **Terminal Security** (Requirement 19): Paste guard for buffer overflow protection
- **API Resilience** (Requirements 20, 44, 46): Skeptical architecture with adaptive rate limit handling
- **Error Handling** (Requirement 21): Specific exception handling with descriptive messages
- **Cross-Platform Support** (Requirement 22): Unix/Linux, Windows, and AWS CloudShell compatibility
- **Configuration Management** (Requirements 23-24): Environment-based configuration with validation
- **Context Management** (Requirements 25, 38-39): Target tracking and snapshot data injection
- **Risk Assessment** (Requirement 26): Automated security group rule analysis
- **Quota Management** (Requirements 27, 45): Per-model tracking with visual indicators
- **Conversation Management** (Requirement 28): History management with context cleanse
- **Action Execution** (Requirement 29): Deterministic parsing and execution of AWS operations
- **User Experience** (Requirements 30-32): Spinners, color coding, and formatted output
- **Lifecycle Management** (Requirement 33): Graceful shutdown with state preservation
- **Quality Assurance** (Requirements 34-35): Comprehensive testing and documentation
- **Deployment** (Requirements 36-37): Automated deployment with tiered IAM policies
- **System Information** (Requirements 43, 48-49): Timestamps, versioning, and dependency management

All requirements follow EARS (Easy Approach to Requirements Syntax) protocol for clarity, testability, and traceability.

