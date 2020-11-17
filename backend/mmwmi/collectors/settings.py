



def process(client, DB):
    ''' Get settings information of a Hyper-V vitual machines
        https://docs.microsoft.com/en-us/windows/win32/hyperv_v2/msvm-virtualsystemsettingdata
    '''
    vms = client.query("select * from Msvm_ComputerSystem where Caption=\"Virtual Machine\"")

    paths = []

    for vm in vms:
        # Get setings data class
        results = vm.associators(wmi_result_class='Msvm_VirtualSystemSettingData')
        results = results[0]

        paths.append(results.path())
        
        # Insert results
        DB['server_data'].find_one_and_update(
            {
                'VirtualSystemIdentifier': results.VirtualSystemIdentifier,
            },
            {
                '$set': {
                    'CreationTime' : results.CreationTime,
                    'ElementName' : results.ElementName,
                    'Notes' : results.Notes,
                    'SecureBootEnabled' : results.SecureBootEnabled,
                    'Version' : results.Version,
                    'VirtualSystemIdentifier' : results.VirtualSystemIdentifier
                }
            },
            upsert=True
        )


    return(paths)