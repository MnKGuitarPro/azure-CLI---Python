# AZURE CLI Utils, using Python

## getSubs.py

- **Description**: The following code returns the name, state and Id of the available subscriptions in the Azure Tenant. In line `8` we can see the code uses a Service Principal login, so we need to provide the Service Principal id and password, and this Service Principal must have privileges over the Azure Tenant.
- **Execution**:
  ```bash
  time python3 getSubs.py <servicePrincipalId> <servicePrincipalPassword> <tenantId>
  ```
- **Login using my account**: If you want to use your username and password to log in, you need to change line `8` to:
  ```python
      commnd = f'login -u {uN} -p {uP} --tenant {tI}'
  ```
  And then, execute the code as follows:
  ```bash
  time python3 getSubs.py <userName> <userPassword> <tenantId>
  ```

## getPublisherOffers.py

- **Description**: The following code creates a file with the available VM images to all the available publishers and offers. In line `31` we can see the code uses a Service Principal login, so we need to provide the Service Principal id and password, and this Service Principal must have privileges over the Azure Tenant. You need a Storage Account with their Account Key to upload a file with the execution result. If you don't want to upload the file because you don't have an available Storage Account, you just need to comment line `25` and provide `foo` values to the parameters related to the Storage Account
- **Execution**:
  ```bash
  time python3 getSubs.py <servicePrincipalId> <servicePrincipalPassword> <tenantId> <storageAccountName> <storageAccountKey> <storageAccountSubscription>
  ```
- **Login using my account**: If you want to use your username and password to log in, you need to change line `8` to:
  ```python
      commnd = f'login -u {uN} -p {uP} --tenant {tI}'
  ```
  And then, execute the code as follows:
  ```bash
  time python3 getSubs.py <userName> <userPassword> <tenantId> <storageAccountName> <storageAccountKey> <storageAccountSubscription>
  ```

## createSubnetNSG

- **Description**: The following code adds a Network Security Group to all Subnets that don't have one (except the Gateway Subnets). The main idea is to add this code to an Azure Automation Account and run it using a Service Principal credential. On line `62` it sees the required input, which is: the service principal id, the service principal password and the tenant id (in that order). On line `34` it sees an output that shows the affected subnets.
- **Execution**:
  ```bash
  time python3 createSubnetNSG.py <servicePrincipalId> <servicePrincipalPassword> <tenantId>
  ```
- **Login using my account**: If you want to use your username and password to log in, you need to change line `9` to:
  ```python
      commnd = f'login -u {uN} -p {uP} --tenant {tI}'
  ```
  And then, execute the code as follows:
  ```bash
  time python3 createSubnetNSG.py <userName> <userPassword> <tenantId>
  ```

## createUDR

- **Description**: The following code maintains the necessary route tables to route the network traffic to an Azure Firewall appliance. The main idea is to add this code to an Azure Automation Account and run it using a Service Principal credential. On line `140` it sees the required input, which is: the service principal id, the service principal password and the tenant id (in that order).
- **Execution**:
  ```bash
  time python3 createUDR.py <servicePrincipalId> <servicePrincipalPassword> <tenantId>
  ```
- **Login using my account**: If you want to use your username and password to log in, you need to change line `9` to:
  ```python
      commnd = f'login -u {uN} -p {uP} --tenant {tI}'
  ```
  And then, execute the code as follows:
  ```bash
  time python3 createUDR.py <userName> <userPassword> <tenantId>
  ```

## startStopVM.py

- **Description**: The following code over an automation account which a hybrid worker group allows to schedule the start or stop/deallocate of a defined group of virtual machines. The main idea is to add this code to an Azure Automation Account and run it using a Service Principal credential which would be stored in the worker from the hybrid worker group as environmental variables. The script receives four (4) parameters: The subscription Id followed by the flag "--subId", the affected (if applies) space-separated resource groups names followed by the flag "--rgNms", the affected (if applies) space-separated resource groups/virtual machine names followed by the flag "--vmNms" and (if applies) the space-separated virtual machine names to be excluded of the process followed by the flag "--exclNms". If a parameter isn't defined, the flag must be specified anyway followed by nothing. Check the following examples:
- **Execution**:
  ```bash
  time python3.8 startStopVM.py --subId <12345a67-b890-12c3-d4ef-g5678901h23> --rgNms <rg1 rg2 rg3> --vmNms <rg1/myvm2 rg2/myvm1> --exclNms <myvm3 myvm4>
  time python3.8 startStopVM.py --subId <12345a67-b890-12c3-d4ef-g5678901h23> --rgNms <rg1 rg2 rg3> --vmNms --exclNms <myvm3 myvm4>
  time python3.8 startStopVM.py --subId <12345a67-b890-12c3-d4ef-g5678901h23> --rgNms --vmNms <rg1/myvm2 rg2/myvm1> --exclNms <myvm3 myvm4>
  time python3.8 startStopVM.py --subId <12345a67-b890-12c3-d4ef-g5678901h23> --rgNms <rg1 rg2 rg3> --vmNms --exclNms
  time python3.8 startStopVM.py --subId <12345a67-b890-12c3-d4ef-g5678901h23> --rgNms --vmNms <rg1/myvm2 rg2/myvm1> --exclNms
  ```
- **Login using my account**: If you want to use your username and password to log in, you need to change line `43` to:
  ```python
      exAzCli('login -u ' + os.environ['SPNAME'] + ' -p ' + os.environ['SPPASS'] + ' -t ' + os.environ['TENAID'],False) #logs in to Azure using your credentials
  ```
  Remember to define the environment variables with the corresponding values in the worker which will execute the Python runbook configured in the Automation Account or the Linux machine which will execute the code directly.