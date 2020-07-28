import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';
import { TetraService } from '../../../@core/data/tetra.service'
import {  NbDialogService, NbToastrService } from '@nebular/theme';

@Component({
  selector: 'ngx-tetra-subscriber-table',
  templateUrl: './tetra-subscriber-table.component.html',
  styleUrls: ['./tetra-subscriber-table.component.scss']
})
export class TetraSubscriberTableComponent implements OnDestroy, OnInit {

  subscriberSettings: Object = { }

  loadTetraTableSettings() {
    return {
      edit: {
        editButtonContent: '<i class="nb-edit"></i>',
        saveButtonContent: '<i class="nb-checkmark"></i>',
        cancelButtonContent: '<i class="nb-close"></i>',
        confirmSave: true,
      },
      actions: {
        delete: false,
        add: false,
        edit: true,
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
        comment: {
          title: 'Comment',
          type: 'text',
          editable: true
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

  unloadAddNew(){
    (document.getElementsByClassName('ng2-smart-action-add-add') as HTMLCollection)[0].remove();
  }

  subscriberSource: Object
  subscriberDetail: Object
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


  tableEvent: any
  modifyType: string
  dialogMessage: string
  private index: number = 0;
  postResult: object
  ipPattern = new RegExp("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
  whiteSpace = new RegExp("([^\\s]*)")

  constructor(
    private tetra: TetraService,
    private dialogService: NbDialogService,
    private toastrService: NbToastrService,
  ) {  }

  refreshData(){
    this.tetra.getTetraSubscribers().subscribe(
      (
        data: {}) => {
        this.subscriberSource = data;
        this.subscriberSettings = this.loadTetraTableSettings()
        this.unloadAddNew()
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

  onDialog(dialog: TemplateRef<any>, crud, event) {
    this.tableEvent = event;
    this.modifyType = crud;
    if (crud == 'edit') {
      this.dialogMessage = 'Edit comment for ' + this.tableEvent.newData.ssi + ' to "' + this.tableEvent.newData.comment + '"?'
    }
    this.dialogService.open(dialog, {
      context: this.dialogMessage
    });
  }

  onModifyConfirm(confirmation): void {
    var invalidData = false
    if (confirmation) {
      if (this.modifyType == 'edit') {

        if (this.tableEvent.newData.comment === "") {
          this.dangerToast('top-right', 'danger', "Comment can't be blank.")
          invalidData = true
        }
        
        if (invalidData == false){
          this.tetra.updateTetraComment(this.tableEvent.newData).subscribe(
            (data: {}) => {
              this.postResult = data;
              if (this.postResult['success']) {
                this.successToast('top-right', 'success', this.postResult['message'])
                this.tableEvent.confirm.resolve();
                this.refreshData()
              } else {
                this.dangerToast('top-right', 'danger', this.postResult['message'])
                this.tableEvent.confirm.reject();
              }
            }
          )
        }

      }
    } else {
      this.tableEvent.confirm.reject();
    }
  }

  successToast(position, status, message) {

    if (this.modifyType == 'delete') {
      this.toastrService.show(
        message,
        `Success`,
        { position, status });
    } else if (this.modifyType == 'edit') {
      this.toastrService.show(
        message,
        `Success`,
        { position, status });
    } else if (this.modifyType == 'create') {
      this.toastrService.show(
        "Created  " + this.tableEvent.newData.name,
        `Success`,
        { position, status });
    }
  }

  dangerToast(position, status, message) {
    this.toastrService.show(
      message,
      `Error`,
      { position, status });
  }


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
