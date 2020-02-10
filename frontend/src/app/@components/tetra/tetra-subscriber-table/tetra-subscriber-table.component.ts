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
  timestamp: any = "Loading..."
  node: any = "Loading..."

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
          this.subscriberDetail = data;
          this.timestamp = data['timestamp']
          this.rssi = data['rssi']
          this.node = data['node']
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
    this.node = 'Loading...'
    this.timestamp = 'Loading...'
    this.getSubscriberDetail(this.tableEvent.data.ssi)
    this.dialogService.open(dialog, {
      context: this.tableEvent.data
    });
  }

}
