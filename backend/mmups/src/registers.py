master = {
    "Van Input" : 0,
    "Vbn Input" : 0,
    "Vcn Input" : 0,
    "System Status"	: "",
    "Output State" : "",
    "Battery Voltage" : 0,
    "VA Out" : 0,
    "Percent Full Load" : 0,
    "Output PF" : 0,
    "Battery Capacity Remaining" : 0,
    "Output Demand KW" : 0,
    "Ambient Temperature" : 0
}

holding_integers =  {
    "System Status"	: 3000,
    "Output State" : 3002,
}

holding_floats = {
    "Van Input" : 4040,
    "Vbn Input" : 4042,
    "Vcn Input" : 4044,
    "Battery Voltage" : 4377,
    "VA Out" : 6088,
    "Percent Full Load" : 6184,
    "Output PF" : 6202,
    "Battery Capacity Remaining" : 7000,
    "Output Demand KW" : 7873,
    "Ambient Temperature" : 12000
}

system_status = {
    "0" : "Off",
    "1" : "System Normal",
    "2" : "System Normal - UPS Redundant",
    "3" : "System Normal - Not Redundant",
    "4" : "System On DC Source",
    "5" : "System On DC Source - Shutdown Imminent",
    "6" : "System Normal - Bypass Not Available",
    "7" : "System Normal - On Line",
    "8" : "System Normal - Energy Saver System",
    "9" : "System Normal - VMMS",
    "10" : "System Normal - HRS",
    "13" : "Output Overload",
    "14" : "System Normal - On Buck",
    "15" : "System Normal - On Boost",
    "16" : "On Bypass",
    "17" : "On Bypass - Starting",
    "18" : "On Bypass - Ready",
    "32" : "On Maintenance Bypass",
    "33" : "On MBS - UPS On Line",
    "34" : "ON MBS - UPS On Bypass",
    "35" : "ON MBS - UPS OFF",
    "36" : "ON MBS - UPS on Battery",
    "37" : "On MBS - UPS On Line + ESS",
    "38" : "On MBS - UPS On Line + VMMS",
    "39" : "On MBS - UPS On Line + HRS",
    "40" : "On MBS - Starting",
    "41" : "On MBS - Ready",
    "48" : "Load Off",
    "49" : "Load Off - Starting",
    "50" : "Load Off - Ready",
    "64" : "Supporting Load",
    "80" : "System Normal",
    "81" : "System Normal - Energy Saver System",
    "96" : "System On Bypass",
    "100" : "System On Manual/Maintenance Bypass",
    "224" : "Load Segment Overload",
    "240" : "System On DC Source",
    "241" : "System Off"
}

output_state = {
    "0" : "Unknown",
    "1" : "On",
    "2" : "Off",
    "3" : "On with pending Off",
    "4" : "Off with pending On",
    "5" : "Unknown",
    "6" : "Unknown",
    "7" : "Failed and Closed",
    "8" : "Failed and Open"
}