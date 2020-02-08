import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TetraService } from '../../../@core/data/tetra.service'

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
        description: {
          title: 'Description',
          type: 'text',
          editable: false
        },
      },
    }
  };

  subscriberSource: Object

  constructor(
    private tetra: TetraService,
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

  ngOnInit() {
    this.refreshData()
  }

  ngOnDestroy(): void { }

}
