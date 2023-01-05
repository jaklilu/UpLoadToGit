

# **********Step 1 Create Azure Exempt Policy**********



import azure.mgmt.subscription
import itertools
import time
from azure.identity import DefaultAzureCredential
import requests
from azure.cli.core import get_default_cli

# Request for input, and user object has to be an 'id' not name
subscription_id = input(
    "What is the subscription id you would like to cancel? ")
user_object_id = input(
    "What is the user object id you would like to grant owner rights? ")

# Create policy exemption
cli = get_default_cli()
result = cli.invoke(
    ["policy", "exemption", "create", "--name", "Allow Owner for Azure Decom Test AZ CLI",
     "--display-name", "Allow Owner For Azure Decom Test AZ CLI",
     "--policy-assignment", "/providers/Microsoft.Management/managementGroups/a4454629-85ac-4c26-b6be-438709073c2a/providers/Microsoft.Authorization/policyAssignments/c34560e1adab441d96fe8cf7",
     "--exemption-category", "Waiver", "--scope", f"/subscriptions/{subscription_id}"]
)
print("\n")
print("Stage 1 creatig exempt policy is completed!")


# **********Step 2 Grant Owner Rights**********


# Grant owner rights to the user object id
cli = get_default_cli()
result = cli.invoke(
    ["role", "assignment", "create", "--assignee-object-id", user_object_id,
     "--assignee-principal-type", "User", "--role", "owner", "--scope", f"/subscriptions/{subscription_id}"]
)
print("\n")
print("Stage 2 granting owner rights is completed!")
print("\n")
print("\n")


# **********Step 3 Cancel Subscription**********


def get_access_token():
    # Get the credentials
    credential = DefaultAzureCredential()

    # Get the access token
    access_token = credential.get_token('https://management.azure.com/')[0]

    return access_token


# Get the access token for the current user
access_token = get_access_token()

# Set the authorization header with the access token
headers = {"Authorization": f"Bearer {access_token}",
           "Content-Type": "application/json"}

# Build the URL for canceling the subscription
url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Subscription/cancel?IgnoreResourceCheck=true&api-version=2019-03-01-preview"

# Send the HTTP POST request to cancel the subscription
response = requests.post(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    print("Subscription successfully canceled!")
else:
    print(
        f"Failed to cancel subscription. Status code: {response.status_code}")
print("\n")
print("Waiting for confirmation...")
print("\n")


# Waiting for 15 seconds... before it runs the next module to confirm cancelation

start_time = time.time()  # Record the start time
dot_spin = "*"
while True:
    print(dot_spin, end=" ")  # Print the dot and a space after it
    time.sleep(1)
    if time.time() - start_time > 20:  # If 20 seconds have passed, exit the loop
        break
print("\n")
print("\n")
print("\n")


# ********** Stage 4 Verify Subscription Cancelation **********


# Get the credentials
credential = DefaultAzureCredential()

# Create an Azure Subscription Client
credential = DefaultAzureCredential()
subscription_client = azure.mgmt.subscription.SubscriptionClient(
    credential=credential)

# Get the subscription
subscription = subscription_client.subscriptions.get(subscription_id)

# Print the display name and state of the subscription
print(f"Subscription display name: {subscription.display_name}")
print(f"Subscription id: {subscription.id}")
print(f"Subscription state: {subscription.state}")
print("\n")
print('If "Subscription state" reads "Warned" then, it is canceled!')
print("\n")

# Done

