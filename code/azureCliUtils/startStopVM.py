from azure.cli.core import get_default_cli
import os
import threading
from datetime import datetime
import argparse

#------------------------------
# Direct execution example through a command line shell:
# python3.8 /home/dpavez/script/python/vm/startStopVMv5.py --subId 12345a67-b890-12c3-d4ef-g5678901h23 --rgNms rg1 rg2 rg3 --vmNms rg1/myvm2 rg2/myvm1 --exclNms myvm3 myvm4
#
# The script needs three environment variables:
# → SPPASS → A Service Principal password with the required privileges to execute the start and stop tasks over VMs in multiple subscriptions
# → SPNAME → A Service Principal name with the required privileges to execute the start and stop tasks over VMs in multiple subscriptions
# → TENAID → The tenant Id in where the process will be executed
#
# Remember that, to create and keep global environment variables, you need to edit the file /etc/environment adding new lines with the variables as followed:
# SPPASS="AB0c1deFghIj2KLm.3NOpqRs~TUV45Wxyz"
# SPNAME="12345a67-b890-12c3-d4ef-g5678901h23"
# TENAID="98765a43-b210-12c3-d4ef-g5678901h23"
#
# You need a directory in the root called "log" which allows processes to read and write in it
#
# Paramenters:
# → fx      → accepted values: stopVM (to stop vms) / startVM (to start vms)
# → subId   → subscription Id to define the scope
# → rgNms   → space-separated resource group names to be affected
# → vmNms   → space-separated virtual machines names (and their resource name) to be affected (if applies)
# → exclNms → space-separated virtual machine names to be excluded (if applies)
#------------------------------

fx='stopVM' #accepted values: stopVM (to stop vms) / startVM (to start vms)

def main():
    receivedArgs = argparse.ArgumentParser()
    receivedArgs.add_argument('--subId', dest='subId', required=True, help='--subId 12345a67-b890-12c3-d4ef-g5678901h23, subscription Id to define the scope', nargs='?', type=str, default='')
    receivedArgs.add_argument('--rgNms', dest='rgNms', required=True, help='--rgNms rg1 rg2 rg3, space-separated resource group names to be affected', nargs='*', type=str, default='')
    receivedArgs.add_argument('--vmNms', dest='vmNms', required=True, help='--vmNms rg1/myvm1 rg1/myvm2 rg2/myvm1, space-separated virtual machines names (and their resource name) to be affected (if applies)', nargs='*', type=str, default='')
    receivedArgs.add_argument('--exclNms', dest='exclNms', required=True, help='--exclNms myvm1 myvm2, space-separated virtual machine names to be excluded (if applies)', nargs='*', type=str, default='')
    args = receivedArgs.parse_args() #passes the received variables to a structure
    if fx!='stopVM' and fx!='startVM':
        print('Invalid function: accepted values → stopVM (to stop vms), startVM (to start vms)')
    else:
        exAzCli('login --service-principal -u ' + os.environ['SPNAME'] + ' -p ' + os.environ['SPPASS'] + ' --tenant ' + os.environ['TENAID'],False) #logs in to Azure using the service principal credentials
        subs = exAzCli('account list --all',False) #gets the available subscriptions
        subData = exAzCli('account show -n ' + args.subId,False) #gets the current subscription data
        dir = 'pythonAutomation'
        pDir = '/log/'
        path = os.path.join(pDir,dir) #defines the path "/log/pythonAutomation" and checks if exists. If not, it creates the path
        try:
            os.stat(path)
        except:
            os.mkdir(path)
        save_path = '/log/pythonAutomation'
        fnameLog = fx + '_' + str(subData['name']) + '_' + args.subId + '.log' #creates a log file using the subscription name and Id
        fFullName = os.path.join(save_path, fnameLog)
        fe = os.path.exists(fFullName)
        if (fe): #checks if the log file exists to create it or write in it
            f = open(fFullName, 'a')
            dtime = datetime.now().strftime("%Y-%m-%d %H:%M")
            f.write('\n\n**************************************************\n\nExecution at ' + dtime + ' in Subscription ' + str(subData['name']) + ' id (' + args.subId + ')\n\n')
            f.close()
        else:
            f = open(fFullName, 'w')
            dtime = datetime.now().strftime("%Y-%m-%d %H:%M")
            f.write('Execution at ' + dtime + ' in Subscription ' + str(subData['name']) + ' id (' + args.subId + ')\n\n')
            f.close()
        if str(subs) != 'None': #validates the received parameter values
            for sub in subs:
                if str(sub['id']) == args.subId and str(sub['state']) == 'Enabled':
                    if not args.rgNms:
                        print('args.vmNms → ' + str(args.vmNms))
                        rgNmsStr = []
                    else:
                        rgNmsStr = args.rgNms[0].split()
                    if not args.vmNms:
                        print('args.vmNms → ' + str(args.vmNms))
                        vmNmsStr = []
                    else:
                        vmNmsStr = args.vmNms[0].split()
                    if not args.exclNms:
                        print('args.exclNms → ' + str(args.exclNms))
                        exclNmsStr = []
                    else:
                        exclNmsStr = args.exclNms[0].split()
                    t = threading.Thread(target=createRGThreadStopByRG, args=(fx,sub,rgNmsStr,vmNmsStr,exclNmsStr,fFullName,), daemon=False)
                    t.start()

def createRGThreadStopByRG(fx,sub,rgNms,vmNms,exclNms,file):
    print('Main: create and start thread ' + str(sub['name']))
    if fx=='stopVM':
        f = open(file, 'a')
        f.write('The selected function is \'stopVM\', and the executed commands are the following:\n\n')
        f.close()
    elif fx=='startVM':
        f = open(file, 'a')
        f.write('The selected function is \'startVM\', and the executed commands are the following:\n\n')
        f.close()
    rgs = exAzCli('group list --subscription ' + str(sub['id']),False)
    if str(rgs) != 'None':
        for rg in rgs:
            if str(rgNms) != 'None':
                for resourceGroupName in rgNms:
                    if str(rg['name']).lower() == resourceGroupName.lower():
                        print('\t\tRG → ' + str(rg['name']))
                        t = threading.Thread(target=getRGVM, args=(fx,sub,rg,exclNms,file,), daemon=False) #checks the received resource groups to trigger a function which gets the vms in the resource group
                        t.start()
                        t.join()
    if str(vmNms) != 'None':
        for vmName in vmNms: #checks the received vms list to trigger a function for all the particular vms
            vmNameStr = vmName.split('/')
            flag = True
            if str(exclNms) != 'None':
                for excludeVMName in exclNms:
                    if vmNameStr[1].lower() == excludeVMName.lower():
                        flag = False
            if flag:
                if fx=='stopVM':
                    t = threading.Thread(target=stopVM, args=(sub,vmNameStr[0],vmNameStr[1],file,), daemon=False)
                    t.start()
                elif fx=='startVM':
                    t = threading.Thread(target=startVM, args=(sub,vmNameStr[0],vmNameStr[1],file,), daemon=False)
                    t.start()

def getRGVM(fx,sub,rg,exclNms,file):
    vms = exAzCli('vm list --subscription ' + str(sub['id']) + ' -g ' + str(rg['name']),False)
    if str(vms) != 'None':
        for vm in vms: #check the vms from both the rgs list and the specific vms list and then it validates they are not in the excluded vms lists
            flag = True
            if str(exclNms) != 'None':
                for excludeVMName in exclNms:
                    if str(vm['name']).lower() == excludeVMName.lower():
                        flag = False
            if flag:
                vmName=str(vm['name']) #triggers the defined function using the vm data
                if fx=='stopVM':
                    t = threading.Thread(target=stopVM, args=(sub,str(rg['name']),vmName,file,), daemon=False)
                    t.start()
                elif fx=='startVM':
                    t = threading.Thread(target=startVM, args=(sub,str(rg['name']),vmName,file,), daemon=False)
                    t.start()

def stopVM(sub,rg,vm,file): #stops the received vm
    exAzCli('vm stop --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm,False) #stopping a VM
    print('az vm stop --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm)
    f = open(file, 'a')
    f.write('az vm stop --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm + '\n')
    f.close()
    t = threading.Thread(target=deallocateVM, args=(sub,rg,vm,file,), daemon=False)
    t.start()
    t.join()

def deallocateVM(sub,rg,vm,file): #deallocates the received vm
    exAzCli('vm deallocate --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm,False) #deallocating a VM
    print('az vm deallocate --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm)
    f = open(file, 'a')
    f.write('az vm deallocate --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm + '\n')
    f.close()

def startVM(sub,rg,vm,file): #starts the received vm
    exAzCli('vm start --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm,False) #deallocating a VM
    print('az vm start --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm)
    f = open(file, 'a')
    f.write('az vm start --subscription ' + str(sub['id']) + ' -g ' + rg + ' -n ' + vm + '\n')
    f.close()

def exAzCli(str,isString): #triggers the azcli function received as a string
    if not isString:
        ipt = str.split()
    else:
        ipt = str.split('¤')
    azc = get_default_cli()
    azc.invoke(ipt, out_file = open(os.devnull, 'w'))
    if azc.result.result:
        return azc.result.result
    elif azc.result.error:
        return '{"return": "error"}'

if __name__ == "__main__":
    main()