## Mine Monitor To Do

### General
- [ ] Towers
- [ ] Pull tetra data somehow
- [ ] Master list
- [ ] Terrain
- [ ] Fleet delete
- [ ] Always general code cleaning, optimising, comments
- [ ] Organise TODO
- [ ] Create README and docs
- [ ] In-browser VNC
- [ ] Automate backups
- [ ] Main page indicates status (% offline)

### Frontend
#### General
- [ ] Indication on web page if script (service) not running (pop down)
- [ ] J.A.R.V.I.S boiii
- [ ] Indication if backend connection has dropped out
- [x] SVG angular material icons for no internet
- [ ] Production / development environment setup
- [x] Convert to progressive web app
- [ ] Add to home screen thing
- [ ] Change shortcut icon on phone
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
- [ ] Delete from GUI
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
- [ ] Add all machines to db through webui (done but not adding up)
- [ ] Pretty up page UI
- [ ] Base station stats
- [ ] TropOS server stats 
- [x] List button

#### Edit
- [ ] Blank edit form after submit and return 'OK'
- [ ] Form input verification
- [ ] Delete fleet
- [ ] Delete trailers
- [ ] Delete gps devices

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
- [ ] Start pinging new fleet when added
- [ ] Reduce amount of devices pinged on fleet

