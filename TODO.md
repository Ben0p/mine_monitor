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
- [ ] Main page indicates status (% offline)
- [ ] nginx serve https
- [ ] East Camera
- [ ] RestAPI authentication token

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

#### Services
- [x] services service for service status
- [x] RestAPI services class (GET)
- [ ] RestAPI services class (POST) - start / stop service
- [x] angular module
- [x] angular services component
- [x] angular services data.service
- [ ] Start / Stop scipts from browser
- [ ] Service detail page

#### Trailers
- [ ] Trailer detail page
- [ ] Reduce details on main page

#### Fleet
- [x] Links to devices from fleet detail
- [x] Add ip addresses to fleet_data collection
- [x] Add ip addresses in fleet detail page

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

#### RestAPI
- [x] Delete
    - [x] Trailers
    - [x] Fleet
    - [x] GPS
    - [x] Alerts


#### Services
- [ ] Master script to run as a service to start other scipts and monitor status
- [ ] RestAPI to start / stop services

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

#### Alerts
- [x] Poll alerts without a delay

#### Fleet
- [x] Start pinging new fleet when added
- [x] Stop process when deleted
    - [x] Delete from both databases when deleted
    - [x] Fix bug where it re-adds fleet to fleet_data
- [ ] Pretty up UI
    - [ ] Perhaps have no data on main page or one latency only
    - [ ] Jarvisify cards

