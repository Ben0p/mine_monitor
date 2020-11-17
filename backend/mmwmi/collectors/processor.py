


def process(client, DB):
    ''' Get processor information of a Hyper-V vitual machine
        https://docs.microsoft.com/en-us/windows/win32/hyperv_v2/msvm-processor
    '''

    processors = client.query("select * from Msvm_Processor")

    cpus = {
        'SystemName' : processors[0].SystemName,
        'cpus' : []
    }

    for processor in processors:

        if process

        DB['server_data'].find_one_and_update(
            {
                'ElementName': results.ElementName,
            },
            {
                '$set': {

                }
            },
            upsert=True
        )

        cpu = {
            'CurrentClockSpeed' : processor.CurrentClockSpeed,
            'ElementName' : processor.ElementName,
            'LoadPercentage' : processor.LoadPercentage,
            'LoadPercentageHistory' : processor.LoadPercentageHistory,
            'MaxClockSpeed' : processor.MaxClockSpeed,
            'Name' : processor.Name,
            'OtherIdentifyingInfo' : processor.OtherIdentifyingInfo,
            'Role' : processor.Role,
            'SystemName' : processor.SystemName
        }

        cpus['cpus'].append(cpu)
    
    return(cpus)

