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

### Frontend
#### General
- [ ] Indication on web page if script (service) not running (pop down)
- [ ] J.A.R.V.I.S boiii
- [ ] Indication if backend connection has dropped out
- [ ] SVG angular material icons for no internet
- [ ] Production / development environment setup
- [ ] Convert to progressive web app
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

#### Fleet
- [x] Links to devices from fleet detail
- [x] Add ip addresses to fleet_data collection
- [x] Add ip addresses in fleet detail page

### Edit
- [ ] Blank edit form after submit and return 'OK'

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

#### Corrections
- [ ] Convert gps corrections to headless
- [x] Corrections stats page
- [x] Add devices via webGUI
- [x] RestAPI class
- [x] RestAPI edit corrections
- [x] Migrate to mongo
- [x] Store stats in mongo
- [x] Create angular module
- [x] WebUI component
- [ ] Delete from GUI
- [ ] List page component
- [ ] Add all machines to db through webui (done but not adding up)

#### Trailers
- [ ] Devices
    - [x] Morningstar
    - [ ] TropOS
    - [ ] Cisco (+gps)
- [x] Add TriStar solar regulators from webui
- [x] Solar regulator modbus data aquisition
- [x] Fix solar current calculations always 0
- [ ] Trailers green / orange / red indicating status
- [x] Trailer temps

#### Alerts
- [x] Poll alerts without a delay

#### Fleet
- [ ] Start pinging new fleet when added
- [ ] Reduce amount of devices pinged on fleet

