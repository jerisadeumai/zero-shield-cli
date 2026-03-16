# Local Development Setup

Set up Zero-Shield CLI on your local development machine.

## Prerequisites

- Python 3.9 or higher
- AWS CLI configured with credentials
- Git (for cloning repository)

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/jerisadeumai/zero-shield-cli.git
cd zero-shield-cli
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
cp environments/local/.env.example .env
```

Edit the `.env` file with your credentials:
```env
# GitHub Models API Token (Required)
GITHUB_TOKEN=your_github_personal_access_token_here

# AWS Credentials (Required for local development)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=us-east-1

# Quarantine Security Group (Optional but recommended)
QUARANTINE_SG_ID=sg-your_quarantine_group_id_here
```

### Step 4: Set Up AWS IAM Permissions

Choose the appropriate policy tier for your needs:

**Option 1: Standard Policy (Recommended)**
```bash
aws iam create-policy \
  --policy-name ZeroShield-Standard \
  --policy-document file://aws-setup/policies/zero-shield-standard.json

aws iam attach-user-policy \
  --user-name YOUR_USERNAME \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/ZeroShield-Standard
```

See [IAM Policies Guide](../../aws-setup/IAM_POLICIES.md) for all policy options.

### Step 5: Run Zero-Shield
```bash
python3 zero_shield_cli.py
```

## Verification

Test your setup:
```bash
# Start Zero-Shield
python3 zero_shield_cli.py

# Try these commands:
> list instances
> /status
> /help
> exit
```

## Troubleshooting

### "AWS credentials not found"
```bash
# Check AWS credentials
aws sts get-caller-identity

# If fails, configure:
aws configure
```

### "GITHUB_TOKEN not set"
```bash
# Check .env file
cat .env | grep GITHUB_TOKEN

# Or export directly
export GITHUB_TOKEN=your_token_here
```

### "No instances found"
- Verify you're in the correct AWS region
- Check IAM permissions
- Ensure you have EC2 instances in your account

## Development Features

Local development provides additional capabilities:

- **Code Editing**: Modify `zero_shield_cli.py` directly
- **Debug Mode**: Add print statements for troubleshooting
- **Custom Models**: Test different LLM configurations
- **Offline Testing**: Work with cached session data

## Next Steps

- [Read the User Guide](../../docs/user-guide/COMMANDS.md)
- [Try Example Commands](../../docs/user-guide/EXAMPLES.md)
- [Explore Architecture](../../docs/architecture/ARCHITECTURE.md)