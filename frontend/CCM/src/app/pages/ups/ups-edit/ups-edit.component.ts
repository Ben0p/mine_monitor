import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { UpsEditService } from './ups-edit.service'
import { NbDialogService, NbToastrService } from '@nebular/theme';

@Component({
  selector: 'ups-edit',
  templateUrl: './ups-edit.component.html',
  styleUrls: ['./ups-edit.component.scss']
})
export class UpsEditComponent implements OnDestroy, OnInit {

  alertForm: FormGroup;
  submitted = false;
  types = [
    {
      'title': 'Management Card',
      'value': 'NMC'
    },
    {
      'title': 'Power Xpert',
      'value': 'PXGX'
    }
  ];

  upsSettings: Object = {
    add: {
      addButtonContent: '<i class="nb-plus"></i>',
      createButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmCreate: true,
    },
  }

  loadModuleTableSettings() {
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
              list: this.types
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

  upsSource: Object
  tableEvent: any
  modifyType: string
  dialogMessage: string
  private index: number = 0;
  postResult: object
  upsArray: Object
  ipPattern = new RegExp("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
  whiteSpace = new RegExp("([^\\s]*)")

  constructor(
    private ups: UpsEditService,
    private dialogService: NbDialogService,
    private toastrService: NbToastrService,
  ) { }

  refreshData(){
    this.ups.getUpsList().subscribe(
      (
        data: {}) => {
        this.upsSource = data;
        this.upsSettings = this.loadModuleTableSettings();
      }
    )

  }

  ngOnDestroy(): void { }

  ngOnInit() {
    this.refreshData()
  }

  onDialog(dialog: TemplateRef<any>, crud, event) {
    this.tableEvent = event;
    this.modifyType = crud;
    if (crud == 'create') {
      this.dialogMessage = 'Are you sure you want to ' + crud + ' ' + this.tableEvent.newData.name + '?'
    } else {
      this.dialogMessage = 'Are you sure you want to ' + crud + ' ' + this.tableEvent.data.name + '?'
    }
    this.dialogService.open(dialog, {
      context: this.dialogMessage
    });
  }

  onModifyConfirm(confirmation): void {
    var invalidData = false
    if (confirmation) {
      if (this.modifyType == 'delete') {
        this.ups.deleteUpsModule(this.tableEvent.data.uid).subscribe(
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
      } else if (this.modifyType == 'edit') {
        if (this.ipPattern.test(this.tableEvent.newData.ip) == false) {
          this.dangerToast('top-right', 'danger', 'IP Address invalid.')
          invalidData = true
        }

        if (this.tableEvent.newData.name === "") {
          this.dangerToast('top-right', 'danger', 'Name invalid.')
          invalidData = true
        }

        if (this.tableEvent.newData.location === "") {
          this.dangerToast('top-right', 'danger', 'Location invalid.')
          invalidData = true
        }

        if (this.tableEvent.newData.model === "") {
          this.dangerToast('top-right', 'danger', 'Model invalid.')
          invalidData = true
        }

        
        if (invalidData == false){
          this.ups.updateUpsModule(this.tableEvent.newData).subscribe(
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

      } else if (this.modifyType == 'create') {
        if (this.ipPattern.test(this.tableEvent.newData.ip) == false) {
          this.dangerToast('top-right', 'danger', 'IP Address invalid.')
          invalidData = true
        }

        if (this.tableEvent.newData.name === "") {
          this.dangerToast('top-right', 'danger', 'Name invalid.')
          invalidData = true
        }

        if (this.tableEvent.newData.location === "") {
          this.dangerToast('top-right', 'danger', 'Location invalid.')
          invalidData = true
        }

        if (this.tableEvent.newData.model === "") {
          this.dangerToast('top-right', 'danger', 'Model invalid.')
          invalidData = true
        }

        
        if (invalidData == false){
          this.ups.createUpsModule(this.tableEvent.newData).subscribe(
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

}
