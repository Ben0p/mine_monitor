import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';

import { AlertService } from './../../../@core/data/alerts'
import { NbDialogService } from '@nebular/theme';

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
      confirmCreate: true,
    },
    edit: {
      editButtonContent: '<i class="nb-edit"></i>',
      saveButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmSave: true,

    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
    columns: {
      location: {
        title: 'Location',
        type: 'string',
      },
      ip: {
        title: 'IP',
        type: 'string',
      },
      type: {
        title: 'Type',
        type: 'string',
      },
      zone: {
        title: 'Zone',
        type: 'string',
      },
    },
  };

  source: Object
  tableEvent: any
  modifyType: string
  dialogMessage: string

  constructor(
    private alerts: AlertService,
    private dialogService: NbDialogService,
    ) {

    this.alerts.getAlertModules().subscribe(
      (
        data: {}) => {
        this.source = data;
      }
    )

  }


  ngOnDestroy(): void { }

  ngOnInit() { }

  onDialog(dialog: TemplateRef<any>, crud, event){
    this.tableEvent = event;
    this.modifyType = crud;
    if (crud == 'create') {
      this.dialogMessage = 'Are you sure you want to '+crud+' '+this.tableEvent.newData.location + '?'
    } else {
      this.dialogMessage = 'Are you sure you want to '+crud+' '+this.tableEvent.data.location + '?'
    }
    this.dialogService.open(dialog, {
      context: this.dialogMessage
    });
  }

  onModifyConfirm(confirmation): void {
    if (confirmation) {
      if (this.modifyType == 'delete'){
        console.log("Deleted " + this.tableEvent.data.location)
      } else if (this.modifyType == 'edit' ) {
        console.log("Edited " + this.tableEvent.data.location)
      } else if (this.modifyType == 'create') {
        console.log("Created " + this.tableEvent.newData.location)
      }

      this.tableEvent.confirm.resolve();
    } else {
      this.tableEvent.confirm.reject();
    }
  }

}