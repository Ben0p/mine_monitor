import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TetraService } from '../../../@core/data/tetra.service'
import { NbDialogService } from '@nebular/theme';

@Component({
  selector: 'ngx-tetra-subscriber-table',
  templateUrl: './tetra-subscriber-table.component.html',
  styleUrls: ['./tetra-subscriber-table.component.scss']
})
export class TetraSubscriberTableComponent implements OnDestroy, OnInit {

  subscriberSettings: Object = { }

  loadTetraTableSettings() {
    return {
      actions: {
        delete: false,
        add: false,
        edit: false,
      },
      columns: {
        description: {
          title: 'Description',
          type: 'text',
          editable: false
        },
        talkgroup: {
          title: 'Current Talkgroup',
          type: 'text',
          editable: false
        },
        node: {
          title: 'Current Node',
          type: 'text',
          editable: false
        },
        ssi: {
          title: 'SSI',
          type: 'text',
          editable: false
        },
        type: {
          title: 'Type',
          type: 'text',
          editable: false,
          filter: {
            type: 'list',
            config: {
              selectText: 'Select...',
              list: [
                { value: 'Subscriber', title: 'Subscriber' },
                { value: 'Group', title: 'Group' },
                { value: 'Application', title: 'Application' },
                { value: 'Terminal', title: 'Terminal' },
              ],
            },
          },
        },
      },
    }
  };

  subscriberSource: Object
  subscriberDetail: Object
  tableEvent: any
  rssi: any = "Loading..."
  rssi_units: any = ""
  timestamp: any = "Loading..."
  node: any = "Loading..."
  gps: any = "Loading..."
  latitude: any = "Loading..."
  lat_meridian: any = ""
  longitude: any = "Loading..."
  lon_meridian: any = ""
  altitude: any = "Loading..."
  accuracy: any = "Loading..."
  gps_time: any = "Loading..."
  maps_url: any = "Loading..."
  link_text: any = ''
  units: any = ''
  speed: any = ''
  speed_units: any = ''
  direction: any = ''
  angle: any = 'Loading...'
  angle_units: any = ''

  constructor(
    private tetra: TetraService,
    private dialogService: NbDialogService,
  ) { }

  refreshData(){
    this.tetra.getTetraSubscribers().subscribe(
      (
        data: {}) => {
        this.subscriberSource = data;
        this.subscriberSettings = this.loadTetraTableSettings()
      }
    )
    }

    getSubscriberDetail(issi){
      this.tetra.getTetraSubscriberDetail(issi).subscribe(
        (
          data: {}) => {

          if(data['gps']){
            this.subscriberDetail = data;
            this.timestamp = data['timestamp']
            this.rssi = data['rssi']
            this.rssi_units = "dBm"
            this.node = data['node']
            this.gps = "Active"
            this.latitude = data['location']['location']['latitude']['decimal_degrees']
            this.lat_meridian = data['location']['location']['latitude']['meridian']
            this.longitude = data['location']['location']['longitude']['decimal_degrees']
            this.lon_meridian = data['location']['location']['longitude']['meridian']
            this.altitude = data['location']['location']['altitude']['meters']
            this.accuracy = data['location']['location']['uncertainty']
            this.gps_time = data['location']['time']['local']
            this.maps_url = data['location']['location']['maps_url']
            this.link_text = "Google Maps"
            this.units = "Meters"
            this.speed = data['location']['velocity']['kmh']
            this.speed_units = "km/h"
            this.direction = data['location']['direction']['direction']
            this.angle = data['location']['direction']['angle']
            this.angle_units = 'deg'
          } else {
            this.gps = "Inactive"
            this.timestamp = "None"
            this.rssi = "None"
            this.rssi_units = ""
            this.node = "None"
            this.latitude = "None"
            this.lat_meridian = ""
            this.longitude = "None"
            this.lon_meridian = ""
            this.altitude = "None"
            this.accuracy = "None"
            this.gps_time = "None"
            this.maps_url = ""
            this.link_text = ""
            this.units = ""
            this.speed_units = ""
            this.speed = "None"
            this.direction = "None"
            this.angle = "None"
            this.angle_units = ""
          }
        }
      )
    }


  ngOnInit() {
    this.refreshData()
  }

  ngOnDestroy(): void { }

  onSelect(dialog: TemplateRef<any>, event){
    this.tableEvent = event;
    this.rssi = 'Loading...'
    this.rssi_units = ""
    this.node = 'Loading...'
    this.timestamp = 'Loading...'
    this.gps = 'Loading...'
    this.latitude = 'Loading...'
    this.lat_meridian = ''
    this.longitude = 'Loading...'
    this.lon_meridian = ''
    this.altitude = 'Loading...'
    this.accuracy = 'Loading...'
    this.gps_time = 'Loading...'
    this.maps_url = 'Loading...'
    this.link_text = ''
    this.units = ''
    this.speed = 'Loading...'
    this.speed_units = ''
    this.speed = "Loading"
    this.direction = ""
    this.angle = "Loading..."
    this.angle_units = ""

    this.getSubscriberDetail(this.tableEvent.data.ssi)
    this.dialogService.open(dialog, {
      context: this.tableEvent.data
    });
  }

}
