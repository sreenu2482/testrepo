import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
#-------------------------------------------------------------------------------------------------------
# if pipeline executed sequentially then we can increment number in key vault from here only.
# but if we run the pipeline parallelly then we need to increment number only after VM is created. 
# otherwise we will get 2 VMs with same name.
#-------------------------------------------------------------------------------------------------------


"""
linapp  10
lindb   20
winapp  30 
windb   40   
"""
tier = "db"
os_type = "lin"
default_val = "s"
default_number = "000"
req_vm_number = 5

keyVaultName = ""
Vlturl = ""
secretName = ""
vms_list = []

def fetch_vm_data():
    if ((tier == "app") and (os_type == "lin")):
        keyVaultName = "applinvlt"
        Vlturl = f"https://{keyVaultName}.vault.azure.net"
        secretName = "applinkey"
        generate_vm_name(keyVaultName, Vlturl, secretName)
        
    if ((tier == "app") and (os_type == "win")):
        keyVaultName = "appwinvlt"
        Vlturl = f"https://{keyVaultName}.vault.azure.net"
        secretName = "appwinkey"
        generate_vm_name(keyVaultName, Vlturl, secretName)
        
    if ((tier == "db") and (os_type == "lin")):
        keyVaultName = "dblinvlt"
        Vlturl = f"https://{keyVaultName}.vault.azure.net"
        secretName = "dblinkey"
        generate_vm_name(keyVaultName, Vlturl, secretName)
    
    if ((tier == "db") and (os_type == "win")):
        keyVaultName = "dbwinvlt"
        Vlturl = f"https://{keyVaultName}.vault.azure.net"
        secretName = "dbwinkey"
        generate_vm_name(keyVaultName, Vlturl, secretName)
    
def generate_vm_name(keyVaultName, Vlturl, secretName):
    global client
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=Vlturl, credential=credential)
    retrieved_secret = client.get_secret(secretName)
    current_vm_number = retrieved_secret.value
    print(f"Current VM Number is: '{current_vm_number}'")

    for i in range (1,req_vm_number + 1):
        num_incment = int(current_vm_number) + i
        VM_Name = default_val + os_type + tier + default_number + str(num_incment)
        #print(VM_Name)
        vms_list.append(VM_Name)
    updated_key_vault_num = int(current_vm_number) + int(req_vm_number)
    vm_num_update(secretName, updated_key_vault_num)
    
def vm_num_update(secretName, VM_IncNumber):
    VM_IncNumber = int(VM_IncNumber)
    print(f"The VM number to be updated in Key Vault is:'{VM_IncNumber}'")
    client.set_secret(secretName, VM_IncNumber)

def list_vms():
    fetch_vm_data()
    print("The VM Names:")
    for vm in vms_list:
        print(vm)

list_vms()

















