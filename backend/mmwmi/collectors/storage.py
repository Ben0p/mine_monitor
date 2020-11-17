
def processStorage(vm):
    ''' Get storage information of a Hyper-V vitual machine
        https://docs.microsoft.com/en-us/windows/win32/hyperv_v2/msvm-virtualharddisksettingdata
    '''

    # Get setings data class
    results_a = vm.associators(wmi_result_class='Msvm_DiskDrive')
    print(results_a)
    

    # Extract results from class
    # TODO add other settings info to dictionary
    storage = {
        'ElementName' : results_a.ElementName,
        'Format' : results_a.Format,
        'MaxInternalSize' : results_a.MaxInternalSize,
        'ParentIdentifier' : results_a.ParentIdentifier,
        'ParentPath' : results_a.ParentPath,
        'Path' : results_a.Path,
        'VirtualSystemIdentifier' : results_a.VirtualSystemIdentifier
    }

    return(storage)