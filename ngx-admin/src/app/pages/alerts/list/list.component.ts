import { Component, OnDestroy, OnInit } from '@angular/core';

import { AlertService } from './../../../@core/data/alerts'


@Component({
  selector: 'ngx-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.scss'],
})
export class ListComponent implements OnDestroy, OnInit {

  settings = {
    add: {
      addButtonContent: '<i class="nb-plus"></i>',
      createButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
    },
    edit: {
      editButtonContent: '<i class="nb-edit"></i>',
      saveButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
    columns: {
      location: {
        title: 'location',
        type: 'string',
      },
      ip: {
        title: 'IP',
        type: 'string',
      },
    },
  };

  source: Object

  constructor(private alerts: AlertService, ) {

    this.alerts.getAlertModules().subscribe(
      (
        data: {}) => {
        this.source = data;
      }
    )

  }


  ngOnDestroy(): void { }

  ngOnInit() {
    console.log(this.alerts.getAlertModules())
  }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }
}