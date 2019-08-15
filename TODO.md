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
- [ ] Tristar history + graphs
- [ ] Migrate to ngx-admin
- [ ] Remove redundant monitoring



### ngx-admin

#### General
- [x] Git clone starter-kit
- [x] Install npm dependancies
- [x] Settings module
- [x] Alerts module


#### Data Services
- [ ] alerts.service
    - [ ] Rename alerts.ts to alerts.service.ts
    - [x] Danger toast on error
    - [ ] Success toast on success


#### Dashboard
- [ ] Alerts overview

#### Alerts

##### Overview
- [x] Advanced Pie chart working with data

##### List
- [x] List working
- [x] List with data
- [ ] Delete
    - [x] Delete event
    - [x] Delete confirmation
    - [ ] Delete data.service function
    - [ ] Send to REST API
    - [ ] ngx style popup
- [x] Edit
    - [x] Edit event
    - [x] Edit confirmation
    - [ ] Edit data.service function
    - [ ] Send to REST API
    - [ ] ngx style popup
- [x] Create
    - [x] Create event
    - [x] Create confirmation
    - [ ] Create data.service function
    - [ ] Send to REST API
    - [ ] ngx style popup

#### Settings
- [x] Create settings module
- [x] Settings route
- [x] Settings menu

##### Style
- [x] Create style page
- [x] Theme
- [x] Layout Direction
- [ ] Sidebar (not working)
- [ ] Layouts (not working)
- [ ] Save settings per user

#### Auth
- [ ] Setup basic auth
- [ ] OPS AD Auth

#### Themes
- [ ] Install themes



## This is being depreciated
### Frontend (Old version)
#### General
- [x] Indication on web page if script (service) not running (pop down)
- [ ] J.A.R.V.I.S boiii
- [x] Indication if backend connection has dropped out
    - [x] http get from app.component every second
    - [x] Snackbar popup if fail
    - [x] import snackbar 
    - [x] data service function
    - [x] Indication for each service
        - [x] Alerts
        - [x] GPS
        - [x] Fleet
        - [x] Services
        - [x] Trailers
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
- [ ] Align cards middle of screen somehow to look better on big screen
- [ ]

#### Overview (home)
- [x] jarvisify box's (not cards)
- [ ] Color gradient based on percentage
- [x] Jarvis background
- [x] Create a overview data service
- [x] Grey and "Offline" if service offline
- [ ] Quick links (somewhere)
- [ ] Align box's middle
- [x] Get rid of scroll bars

#### Services
- [x] services service for service status
- [x] angular module
- [x] angular services component
- [x] angular services data.service
- [ ] Start / Stop scipts from browser
- [ ] Service detail page


#### Edit
- [x] Blank edit form after submit
- [ ] Return 'OK' after submit
- [x] Form input verification
    - [x] IP validation
    - [x] Required inputs
    - [ ] Trailer name starts with CT
    - [ ] Move IP pattern to dynamic section
- [ ] Tooltips
- [x] Delete fleet
- [ ] Delete trailers
    - [ ] Not deleting
- [x] Delete gps devices
- [x] Trailer 
    - [x] name
    - [x] tropos
        - [x] 2.4
        - [x] 5
        - [x] LAN
    - [x] cisco ip
    - [x] ub ip
    - [x] ISSI

#### Alerts
- [ ] Detail and controls page
    - [ ] Disable toggle for 2 sec after click
    - [ ] Make toggles less glitchy


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
- [x] Trailers
    - [x] Add Tropos
    - [x] Add Ubi
    - [x] Add Cisco
    - [x] Add tetra ISSI for reference only
    - [x] Add other Tropos IP's for reference
    - [x] Don't add tristar_live if no tristar
    - [x] TropOS LAN to ping to determine if gateway
- [x] Create trailer_detail
- [x] GPS
    - [x] Generate list for other samplicate servers
    - [x] Return list as download 'final.conf'
- [ ] Alerts
    - [x] Change all to /alerts/{whatever}


#### Services
- [x] Master script to run as a service to start other scipts and monitor status
- [x] Add overview service
- [ ] Fix uptime
- [ ] Service stopped info busted

#### Alerts
- [x] Poll alerts without a delay

#### Overview
- [x] Service running
- [x] Percent online
    - [x] Alerts
    - [x] GPS (Rx fail)?
    - [x] Fleet (per truck or device or somethingOffline)?
    - [x] Services
    - [x] Trailers
- [x] Fix key error if device doesn't exist
