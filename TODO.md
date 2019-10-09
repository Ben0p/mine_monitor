## Mine Monitor To Do
*Deleted redundant tasks*

### Minimum to deploy
- [x] Controlls working
- [x] Temp remove Sidebar and Layouts controlls
- [x] Temp remove auth menu
- [x] Change Title
- [x] Auth
- [ ] Frontend and API security

### Dockerisation
- [ ] Web Frontend
    - [x] nginx
    - [x] Self signed keys (localhost)
    - [x] https
    - [x] Redirect to https
    - [x] Reverse proxy for API
        - [x] API location */api/
- [ ] Rest API
    - [x] wsgi with gunicorn
    - [x] working Dockerfile and docker-compose.yml
    - [ ] Talk to docker mongo
- [ ] Mongo
    - [ ] password
- [ ] Alerts
    - [ ] Talk to docker mongo
    - [x] Get alerts.py working
    - [x] Log output

### Issues
- [x] Scrollbar 
- [x] Status card over-flow
- [x] Emergency control set to default color
- [ ] Status card sometimes offline but still 'ON'
- [ ] Need to ping a few times rather than once
- [ ] Flask https fails due to unsigned certificate
    - [ ] Use nginx reverse proxy 
- [ ] No way to create alert zones or locations

### Security
- [x] Domain auth through TLS
- [x] Rest API over HTTPS
- [x] API reverse proxy

### General
- [ ] Pull tetra data somehow
- [ ] Create proper README and docs
- [ ] Automate backups
- [ ] nginx serve https
- [ ] CCTV
- [ ] RestAPI authentication
- [ ] Database backup
- [x] Kerberos authentication against domain
- [ ] Pre-load pwa for offline mode
- [ ] Build number in footer
- [x] Auth

### Frontend

#### General
- [x] Git-clone ngx-admin
- [x] Install npm dependancies
- [x] Settings module
- [x] Alerts module

#### Data Services
- [ ] alerts.service
    - [x] Rename alerts.ts to alerts.service.ts
    - [x] Danger toast on error
    - [x] Infinite danger toast on multiple API call fails
        - [x] Disable duplicates
    - [x] Close danger toast on restoration of API
    - [x] Danger toast timeout if not re-activated

#### Dashboard
- [x] Alerts overview

#### Alerts
##### Overview
- [x] Advanced Pie chart working with data
##### All
- [x] Data service
- [x] Basic Cards
    - [x] Status Icons
    - [x] Status color
    - [x] Offline

##### List
- [x] List working
- [x] List with data
- [x] Delete
    - [x] Delete event
    - [x] Delete confirmation
    - [x] Delete data.service function
    - [x] Send to REST API
    - [x] ngx style popup
- [x] Edit
    - [x] Edit event
    - [x] Edit confirmation
    - [x] Edit data.service function
    - [x] Send to REST API
    - [x] ngx style popup
- [x] Create
    - [x] Create event
    - [x] Create confirmation
    - [x] Create data.service function
    - [x] Send to REST API
    - [x] ngx style popup
- [x] Refresh on after operation

##### Detail
- [x] Controlls
- [x] Information card
- [ ] Notes card
    - [ ] Post

#### Settings
- [x] Create settings module
- [x] Settings route
- [x] Settings menu

##### Style
- [x] Create style page
- [x] Theme
- [ ] Save settings per user

#### Auth
- [x] Domain AD Auth
- [x] JWT auth
- [x] JWT payload data
- [x] User name
- [ ] Role based ACL
    - [x] Single role
    - [ ] Multi-role (alerts, configs)
- [x] Log out

#### User
- [x] User name
- [ ] Profile page
- [ ] Save preferences
- [x] Log out
- [x] User Menu

### Backend
#### General
- [x] Convert scripts into linux services
    - [x] alert
    - [x] rest


#### RestAPI
##### General
- [x] Overview get request
- [x] Serve https

##### Auth
- [x] Login
- [x] JWT token

##### Services
- [ ] Re-do for new frontend

##### Alerts
- [x] Poll alerts without a delay
- [x] alerts_all collection clean up after module deleted
- [x] Change all to /alerts/{whatever}
- [x] Status
    - [x] Only return one status per zone
- [x] Overview
    - [x] Count status types
- [x] All
    - [x] Return all
- [x] Display
    - [x]  Add modules for trailers
- [x] Delete
    - [x] Delete from all and modules collections
    - [x] Return status
- [x] Update
    - [x] Update module
    - [x] Return status
- [x] Create
    - [x] Create module
    - [x] Return status
