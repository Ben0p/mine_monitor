# mine-monitor

## Custom network device management system

## Features
- AD authentication
- Two overview dashboards
- Alert display boards status
- Generator fuel levels
- MPPT solar controller charge levels
- Eaton UPS info
- Wind speed data from SQL
- Tetra digital radio 
    - Node stats
    - Subscriber list
    - SDS GPS position decoding
- FM broadcast info
    - On-site FM re-broadcast status
- MAP
    - Cesium map with Tetra GPS positions
    - Additional mine model WMS layers

## General
- JABODC - Just a bunch of docker containers
- nginx web server
- nginx proxy to flask API
- data polling via various python scripts

## Frontend
- Based on the [Nebular UI Kit](https://akveo.github.io/nebular/)
- Full CRUD operation for devices

## Backend
- AD authentication via api
- Various python scripts in separate docker containers
- Polling scripts dump data into MongoDB
- Flask API serves data as a http json
    - Full CRUD
- Nginx proxies API through https://url/api

## Planned features
- More work on Cesium map
- PDU polling
- Microsoft SCOM and SCCM integrations
- Cisco switch integrations
