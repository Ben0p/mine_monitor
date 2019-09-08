import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AlertService } from '../../../@core/data/alerts.service'
import { NbDialogService, NbToastrService } from '@nebular/theme';

@Component({
  selector: 'ngx-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.scss'],
})

export class ListComponent implements OnDestroy, OnInit {

  alertForm: FormGroup;
  submitted = false;
  alertZones: Object;
  alertTypes: Object;

  settings: Object = {
    add: {
      addButtonContent: '<i class="nb-plus"></i>',
      createButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmCreate: true,
    },
  }

  loadTableSettings() {
    return {
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
        name: {
          title: 'Name',
          type: 'string',
        },
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
          editor: {
            type: 'list',
            config: {
              list: this.alertTypes
            }
          }
        },
        zone: {
          title: 'Zone',
          type: 'string',
          editor: {
            type: 'list',
            config: {
              list: this.alertZones
            }
          }
        },
        uid: {
          title: 'UID',
          type: 'text',
          editable: false,
          editor: {
            type: 'list',
            config: {
              list: [
                {
                  value: '',
                  title: '(auto)'
                }
              ]
            }
          }
        }
      },
    }
  };

  source: Object
  tableEvent: any
  modifyType: string
  dialogMessage: string
  private index: number = 0;
  postResult: object
  alertsArray: Object
  ipPattern = new RegExp("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
  whiteSpace = new RegExp("([^\\s]*)")


  constructor(
    private alerts: AlertService,
    private dialogService: NbDialogService,
    private toastrService: NbToastrService,
    private formBuilder: FormBuilder
  ) {

    this.alerts.getAlertModules().subscribe(
      (
        data: {}) => {
        this.source = data;
      }
    )

    this.alerts.getAlertZones().subscribe(
      (
        data: {}) => {
        this.alertZones = data;
        this.settings = this.loadTableSettings();
      }
    )

    this.alerts.getAlertTypes().subscribe(
      (
        data: {}) => {
        this.alertTypes = data;
        this.settings = this.loadTableSettings();
      }
    )
  }


  ngOnDestroy(): void { }

  ngOnInit() {

  }


  onDialog(dialog: TemplateRef<any>, crud, event) {
    this.tableEvent = event;
    this.modifyType = crud;
    if (crud == 'create') {
      this.dialogMessage = 'Are you sure you want to ' + crud + ' ' + this.tableEvent.newData.location + '?'
    } else {
      this.dialogMessage = 'Are you sure you want to ' + crud + ' ' + this.tableEvent.data.location + '?'
    }
    this.dialogService.open(dialog, {
      context: this.dialogMessage
    });
  }

  onModifyConfirm(confirmation): void {
    var invalidData = false
    if (confirmation) {
      if (this.modifyType == 'delete') {
        this.alerts.deleteAlertModule(this.tableEvent.data.name).subscribe(
          (data: {}) => {
            this.postResult = data;
            if (this.postResult['success']) {
              this.successToast('top-right', 'success', this.postResult['message'])
              this.tableEvent.confirm.resolve();
            } else {
              this.dangerToast('top-right', 'danger', this.postResult['message'])
              this.tableEvent.confirm.reject();
            }
          }
        )
      } else if (this.modifyType == 'edit') {
        if (this.ipPattern.test(this.tableEvent.newData.ip) == false) {
          this.dangerToast('top-right', 'danger', 'IP Address')
          invalidData = true
        }

        if (this.tableEvent.newData.name === "") {
          this.dangerToast('top-right', 'danger', 'Name')
          invalidData = true
        }

        if (this.tableEvent.newData.location === "") {
          this.dangerToast('top-right', 'danger', 'Location')
          invalidData = true
        }

        if (this.tableEvent.newData.type === "") {
          this.dangerToast('top-right', 'danger', 'Type')
          invalidData = true
        }

        if (this.tableEvent.newData.zone === "") {
          this.dangerToast('top-right', 'danger', 'Zone')
          invalidData = true
        }
        
        if (invalidData == false){
          this.successToast('top-right', 'success', 'Modify Success')
          this.tableEvent.confirm.resolve();
        }

      } else if (this.modifyType == 'create') {
        if (this.ipPattern.test(this.tableEvent.newData.ip) == false) {
          this.dangerToast('top-right', 'danger', 'IP Address')
          invalidData = true
        }

        if (this.tableEvent.newData.name === "") {
          this.dangerToast('top-right', 'danger', 'Name')
          invalidData = true
        }

        if (this.tableEvent.newData.location === "") {
          this.dangerToast('top-right', 'danger', 'Location')
          invalidData = true
        }

        if (this.tableEvent.newData.type === "") {
          this.dangerToast('top-right', 'danger', 'Type')
          invalidData = true
        }

        if (this.tableEvent.newData.zone === "") {
          this.dangerToast('top-right', 'danger', 'Zone')
          invalidData = true
        }
        
        if (invalidData == false){
          this.successToast('top-right', 'success', 'Modify Success')
          this.tableEvent.confirm.resolve();
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
        "Updated " + this.tableEvent.data.name,
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

}