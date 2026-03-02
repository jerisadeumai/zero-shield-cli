import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="Boto3 will no longer support Python 3.9")

import sys, os, json, boto3
from dotenv import load_dotenv
from openai import OpenAI
from botocore.exceptions import ClientError

# 1. INITIALIZATION
load_dotenv()
gh_client = OpenAI(
    base_url="https://models.github.ai/inference", 
    api_key=os.environ.get("GITHUB_TOKEN")
)

# Target Security Group for isolation
QUARANTINE_SG_ID = "sg-041a97ba55afb006e" 

# 2. THE TOOLS (The Muscle / ACTION Phase)
def get_client(service: str, region: str):
    """Dynamically initializes AWS clients with a safety fallback."""
    safe_region = "us-east-1" if not region or "region" in region.lower() else region
    return boto3.client(service, region_name=safe_region)

def tool_list_resources(region: str) -> str:
    """OBSERVE: Scans the environment for instances."""
    try:
        ec2 = get_client('ec2', region)
        res = ec2.describe_instances()
        summary = []
        for r in res['Reservations']:
            for i in r['Instances']:
                name = next((t['Value'] for t in i.get('Tags', []) if t['Key'] == 'Name'), "NoName")
                summary.append(f"{i['InstanceId']} ({name})")
        return f"OBSERVATION COMPLETE: {', '.join(summary)}" if summary else "No resources observed."
    except Exception as e:
        return f"OBSERVATION FAILED: {str(e)}"

def tool_inspect_resource(instance_id: str, region: str) -> str:
    """OBSERVE: Extracts security context for a target."""
    try:
        ec2 = get_client('ec2', region)
        res = ec2.describe_instances(InstanceIds=[instance_id])
        inst = res['Reservations'][0]['Instances'][0]
        sg_names = [g['GroupName'] for g in inst['SecurityGroups']]
        return f"STATE: {inst['State']['Name']} | GROUPS: {', '.join(sg_names)}"
    except Exception as e:
        return f"INSPECTION FAILED: {str(e)}"

def tool_apply_quarantine(instance_id: str, region: str) -> str:
    """ACT: Executes the isolation of the resource."""
    try:
        ec2 = get_client('ec2', region)
        ec2.modify_instance_attribute(InstanceId=instance_id, Groups=[QUARANTINE_SG_ID])
        return f"ACTION SUCCESS: {instance_id} isolated."
    except Exception as e:
        return f"ACTION FAILED: {str(e)}"

# 3. THE REASONING ENGINE (The Brain / ORIENT & DECIDE Phases)
def run_copilot_repl():
    """REPL: Read-Eval-Print Loop for continuous security management."""
    print("--------------------------------------------------")
    print("ZERO-SHIELD DYNAMIC REPL ACTIVE")
    print("FRAMEWORK: OODA (Observe-Orient-Decide-Act)")
    print("--------------------------------------------------")
    
    # Store history for context-aware ID extraction
    chat_history = []
    
    while True:
        user_input = input("\n[USER]: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            break
        if not user_input:
            continue

        system_instructions = """
        You are Zero-Shield, an Agentic Security Copilot. 
        
        RULES:
        1. TARGET: You MUST extract the Instance ID (starting with 'i-'). 
           If the user says 'it' or 'the instance', use the ID mentioned previously.
           NEVER use the word 'instance' as the target ID.
        2. REGION: Always use a valid region like 'us-east-1'.
        3. INTENT: LIST, INSPECT, QUARANTINE.

        JSON FORMAT ONLY:
        {
            "intent": "TOOL_NAME",
            "target": "i-xxxxxxxxxxxxxxxxx",
            "region": "us-east-1",
            "reply": "Orientation explanation"
        }
        """

        try:
            chat_history.append({"role": "user", "content": user_input})
            
            response = gh_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_instructions}] + chat_history[-5:],
                response_format={ "type": "json_object" }
            )
            
            data = json.loads(response.choices[0].message.content)
            intent, target, region, reply = data['intent'], data['target'], data['region'], data['reply']
            
            chat_history.append({"role": "assistant", "content": reply})

            print(f"\n[AI ORIENTATION]: {reply}")

            if intent == "LIST":
                print(f"[*] EXECUTION (Observe): {tool_list_resources(region)}")
            elif intent == "INSPECT" and "i-" in str(target):
                print(f"[*] EXECUTION (Observe): {tool_inspect_resource(target, region)}")
            elif intent == "QUARANTINE" and "i-" in str(target):
                print(f"[*] EXECUTION (Act): {tool_apply_quarantine(target, region)}")
            else:
                print("[*] STATUS: Waiting for a valid Instance ID (e.g., i-xxxx).")
            
        except Exception as e:
            print(f"[SYSTEM ERROR]: {e}")

if __name__ == "__main__":
    run_copilot_repl()
