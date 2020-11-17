

def process(client, DB, vm_paths):
    ''' Get summary information of a Hyper-V virtual machine
        https://docs.microsoft.com/en-us/windows/win32/hyperv_v2/msvm-summaryinformation
    '''

    vm_attrs = {
        'Name': 0, 
        'ElementName': 1, 
        'CreationTime': 2, 
        'Notes': 3, 
        'NumberOfProcessors': 4, 
        #'ThumbnailImage': 5, 
        #'ThumbnailImage': 6, 
        'ThumbnailImage': 7, # 320x240 px
        'AllocatedGPU': 8, 
        'EnabledState': 100, 
        'ProcessorLoad': 101, 
        'ProcessorLoadHistory': 102, 
        'MemoryUsage': 103,
        'Heartbeat': 104, 
        'UpTime': 105, 
        'GuestOperatingSystem': 106, 
        'Snapshots': 107, 
        'AsynchronousTasks': 108, 
        'HealthState': 109, 
        'OperationalStatus': 110, 
        'StatusDescriptions': 111, 
        'MemoryAvailable': 112, 
        'AvailableMemoryBuffer': 113 
    }
    values = list(vm_attrs.values())

    thumbnails = []

    for path in vm_paths:

        management_service = client.Msvm_VirtualSystemManagementService()[0]

        results = management_service.GetSummaryInformation(values, [path])
        results = results[1][0]

        thumbnails.append(
            {
                'name' : results.ElementName,
                'data' : results.ThumbnailImage
            }
        )

        # Insert results
        DB['server_data'].find_one_and_update(
            {
                'ElementName': results.ElementName,
            },
            {
                '$set': {
                    'Name': results.Name, 
                    'ElementName': results.ElementName, 
                    'CreationTime': results.CreationTime, 
                    'Notes': results.Notes, 
                    'NumberOfProcessors': results.NumberOfProcessors,
                    'AllocatedGPU': results.AllocatedGPU, 
                    'EnabledState': results.EnabledState, 
                    'ProcessorLoad': results.ProcessorLoad, 
                    'ProcessorLoadHistory': results.ProcessorLoadHistory, 
                    'MemoryUsage': results.MemoryUsage,
                    'Heartbeat': results.Heartbeat, 
                    'UpTime': results.UpTime, 
                    'GuestOperatingSystem': results.GuestOperatingSystem, 
                    'Snapshots': results.Snapshots, 
                    'AsynchronousTasks': results.AsynchronousTasks, 
                    'HealthState': results.HealthState, 
                    'OperationalStatus': results.OperationalStatus, 
                    'StatusDescriptions': results.StatusDescriptions, 
                    'MemoryAvailable': results.MemoryAvailable, 
                    'AvailableMemoryBuffer': results.AvailableMemoryBuffer 
                }
            },
            upsert=True
        )

    return(thumbnails)
