## Mine Monitor To Do
*Deleted redundant tasks*

### Minimum to deploy
- [x] Controlls working
- [x] Temp remove Sidebar and Layouts controlls
- [x] Temp remove auth menu
- [x] Change Title

### General
- [ ] Pull tetra data somehow
- [ ] Create proper README and docs
- [ ] Automate backups
- [ ] nginx serve https
- [ ] CCTV
- [ ] RestAPI authentication
- [ ] Database backup
- [ ] Kerberos authentication against domain
- [ ] Pre-load pwa for offline mode
- [ ] Build number in footer
- [ ] Editable header name
- [ ] 

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
- [ ] 
- [ ] Information card
- [ ] Notes card
    - [ ] Post

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
- [ ] Domain AD Auth

### Backend
#### General
- [x] Convert scripts into linux services
    - [x] alert
    - [x] rest


#### RestAPI
- [x] Delete
    - [x] Alerts
- [x] Overview get request
- [ ] Alerts
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


#### Services
- [ ] Re-do for new frontend

#### Alerts
- [x] Poll alerts without a delay
- [x] alerts_all collection clean up after module deleted
