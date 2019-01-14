## Mine Monitor To Do

### General
- [ ] Towers
- [ ] Pull tetra data somehow
- [ ] Master list
- [ ] Terrain
- [x] Fleet delete
- [ ] Always general code cleaning, optimising, comments
- [x] Organise TODO
- [ ] Create README and docs
- [ ] In-browser VNC
- [ ] Automate backups
- [x] Main page indicates status (% offline)
- [ ] nginx serve https
- [ ] East Camera
- [ ] RestAPI authentication token
- [ ] Database backup
- [ ] Multiple user accounts and authentication
    - [ ] Tie into fmg.local or fmg.ops (long-term)
- [ ] Pre-load pwa for offline mode

### Frontend
#### General
- [ ] Indication on web page if script (service) not running (pop down)
- [ ] J.A.R.V.I.S boiii
- [x] Indication if backend connection has dropped out
    - [x] http get from app.component every second
    - [x] Snackbar popup if fail
    - [x] import snackbar 
    - [x] data service function
    - [ ] Indication for each service
        - [ ] Alerts
        - [ ] GPS
        - [ ] Fleet
        - [ ] Services
        - [ ] Trailers
- [x] SVG angular material icons for no internet
- [ ] Production / development environment setup
- [x] Convert to progressive web app
- [x] Add to home screen thing (manually through chrome)
- [x] Change shortcut icon on phone
- [ ] Graphs, because awesome
- [ ] Put angular components into modules (re-structure)
- [ ] Mobile size menu
- [x] Hide navbar button or something
- [x] Overview home page percentages
- [ ] Fix arrow down partly off screen on phones

#### Overview (home)
- [x] jarvisify box's (not cards)
- [ ] Color gradient based on percentage
- [x] Jarvis background
- [x] Create a overview data service
- [x] Grey and "Offline" if service offline
- [ ] Quick links (somewhere)
- [ ] Align box's middle

#### Services
- [x] services service for service status
- [x] angular module
- [x] angular services component
- [x] angular services data.service
- [ ] Start / Stop scipts from browser
- [ ] Service detail page

#### Trailers
- [ ] Trailer detail page
- [ ] Reduce details on main page
- [ ] Add Tropos / Cisco / Ubi

#### Fleet
- [x] Links to devices from fleet detail
- [x] Add ip addresses to fleet_data collection
- [x] Add ip addresses in fleet detail page
- [ ] Jarvisify
    - [ ] latency if online, "Offline" if offline
    - [ ] Perhaps have no data on main page or one latency only
- [ ] Fleet Detail
    - [ ] Shorten to fit on phone better
    - [ ] Jarvisify

### GPS
- [x] Create angular module
- [x] WebUI component
- [x] Delete from GUI
- [x] Correction device list
    - [x] List page component
    - [x] Data service
    - [x] Mat data table
        - [x] Sort
        - [x] Filter
        - [x] Pagination
        - [x] Default sort
        - [ ] Delete 
        - [ ] Add
    - [x] Title
- [x] Add all machines to db through webui
- [ ] Pretty up page UI
- [ ] Base station stats
- [ ] TropOS server stats 
- [x] List button

#### Edit
- [ ] Blank edit form after submit and return 'OK'
- [ ] Form input verification
- [x] Delete fleet
- [x] Delete trailers
- [x] Delete gps devices
- [ ] Trailer tropos / cisco / ubi


### Backend
#### General
- [ ] Create cisco 1572 script
- [ ] Make scripts headless (output text is hidden anyway)
- [x] Convert scripts into linux services
    - [x] alert
    - [x] rest
    - [x] fleet
    - [x] trailers
    - [x] corrections
    - [x] services
    - [x] overview
- [ ] change scripts to device type or modules
    - [ ] tropos
        - [ ] frontend add form
        - [ ] backend script
        - [ ] mongo collection
        - [ ] restAPI adjustment
    - [ ] alerts
        - [ ] frontend add form
        - [ ] backend script
        - [ ] mongo collection
        - [ ] restAPI adjustment
- [x] Create overview script

#### RestAPI
- [x] Delete
    - [x] Trailers
    - [x] Fleet
    - [x] GPS
    - [x] Alerts
- [x] Overview get request
- [x] Check get request for monitoring connection
- [ ] Services
    - [x] Services class (GET)
    - [ ] Services class (POST) - start / stop service
- [ ] Trailers
    - [ ] Add Tropos
    - [ ] Add Ubi
    - [ ] Add Cisco


#### Services
- [ ] Master script to run as a service to start other scipts and monitor status
- [x] Add overview service
- [ ] Fix uptime
- [ ] Service stopped info busted

#### GPS
- [x] Convert gps corrections to headless
- [x] Corrections stats page
- [x] Add devices via webGUI
- [x] RestAPI class
- [x] RestAPI edit corrections
- [x] Migrate to mongo
- [x] Store stats in mongo
- [x] restAPI to get list of devices
- [ ] Base station data
- [ ] TropOS corrections data


#### Trailers
- [ ] Devices
    - [x] Morningstar
    - [ ] TropOS
    - [ ] Cisco (+gps)
- [x] Add TriStar solar regulators from webui
- [x] Solar regulator modbus data aquisition
- [x] Fix solar current calculations always 0
- [ ] Trailers green / orange / red indicating status
    - [ ] On / offlne
    - [ ] Battery volts
    - [ ] Temp
- [x] Trailer temps
- [ ] Ping
    - [ ] Cisco
    - [ ] Topos
    - [ ] Ubi
    - [ ] Tristar
- [ ] Pull cisco data

#### Alerts
- [x] Poll alerts without a delay

#### Fleet
- [x] Start pinging new fleet when added
- [x] Stop process when deleted
    - [x] Delete from both databases when deleted
    - [x] Fix bug where it re-adds fleet to fleet_data
- [ ] Reduce pings
    - [ ] Don't bother about tropos 5ghz
    - [ ] Don't ping spare IP if not used


#### Overview
- [x] Service running
- [x] Percent online
    - [x] Alerts
    - [x] GPS (Rx fail)?
    - [x] Fleet (per truck or device or somethingOffline)?
    - [x] Services
    - [x] Trailers
