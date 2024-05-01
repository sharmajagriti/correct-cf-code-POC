import subprocess
import time

# Define the parameters as variables
pProject = "project"
pEnvironment = "dev"
pResourceName = ""
pRegion = "us-east-1"

# Function to execute AWS CloudFormation create stack command
def create_stack(stack_name, template_body, parameters):
    command = [
        "aws",
        "cloudformation",
        "create-stack",
        "--region",
        pRegion,
        "--stack-name",
        stack_name,
        "--template-body",
        f"file://{template_body}",
        "--parameters",
        f"file://{parameters}",
        "--capabilities",
        "CAPABILITY_NAMED_IAM",
        "--tags",
        f"Key=pProject,Value={pProject}",
        f"Key=pEnvironment,Value={pEnvironment}",
        f"Key=StackName,Value={stack_name}"
    ]
    subprocess.run(command, check=True)
    time.sleep(40)  # Wait for 40 seconds after creating the stack

# Function to wait for stack creation completion
def wait_for_stack_completion(stack_name):
    command = [
        "aws",
        "cloudformation",
        "wait",
        "stack-create-complete",
        "--region",
        pRegion,
        "--stack-name",
        stack_name
    ]
    subprocess.run(command, check=True)

# Create and wait for each stack individually
stacks = [
    (f"{pProject}-{pEnvironment}-InfraStackT2", "Templates/InfraStackT2.yml", f"Parameters/{pEnvironment}/InfraStackT2.json"),
    (f"{pProject}-{pEnvironment}-IAMRolesStack", "Templates/IAMRolesStack.yml", f"Parameters/{pEnvironment}/IAMRolesStack.json"),
    (f"{pProject}-{pEnvironment}-SecurityGroupStack", "Templates/SecurityGroupStack.yml", f"Parameters/{pEnvironment}/SecurityGroupStack.json"),
    (f"{pProject}-{pEnvironment}-NaclEntryStackPublic", "Templates/NaclEntryStackPublic.yml", f"Parameters/{pEnvironment}/NaclEntryStackPublic.json"),
    (f"{pProject}-{pEnvironment}-NaclEntryStackPrivate", "Templates/NaclEntryStackPrivate.yml", f"Parameters/{pEnvironment}/NaclEntryStackPrivate.json"),
    (f"{pProject}-{pEnvironment}-Web-Instance", "Templates/Web-Instance.yml", f"Parameters/{pEnvironment}/Web-Instance.json"),
    (f"{pProject}-{pEnvironment}-App-Instance", "Templates/App-Instance.yml", f"Parameters/{pEnvironment}/App-Instance.json")
]

for stack_name, template_body, parameters in stacks:
    create_stack(stack_name, template_body, parameters)
    wait_for_stack_completion(stack_name)

# Get stacks list
subprocess.run(["aws", "cloudformation", "list-stacks",
                "--query", "StackSummaries[?StackStatus!='DELETE_COMPLETE'].{Name:StackName,Status:StackStatus}"], check=True)
