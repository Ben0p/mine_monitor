import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';
import { FmService } from '../../../@core/data/fm.service'
import { NbDialogService, NbToastrService } from '@nebular/theme';

@Component({
  selector: 'fm-edit',
  templateUrl: './fm-edit.component.html',
  styleUrls: ['./fm-edit.component.scss']
})
export class FmEditComponent implements OnDestroy, OnInit {

  submitted = false;
  types = [
    {
      'title': 'Odroid',
      'value': 'Odroid'
    },
    {
      'title': 'Barix',
      'value': 'Barix'
    }
  ];

  moduleSettings: Object = {
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
        station: {
          title: 'Station',
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
        url: {
          title: 'URL',
          type: 'string',
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

  moduleSource: Object
  tableEvent: any
  modifyType: string
  dialogMessage: string
  private index: number = 0;
  postResult: object
  ipPattern = new RegExp("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
  whiteSpace = new RegExp("([^\\s]*)")

  constructor(
    private fm: FmService,
    private dialogService: NbDialogService,
    private toastrService: NbToastrService,
  ) { }

  refreshData(){
    this.fm.getFmModules().subscribe(
      (
        data: {}
      ) => {
          this.moduleSource = data;
          this.moduleSettings = this.loadModuleTableSettings();
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
      this.dialogMessage = 'Are you sure you want to ' + crud + ' ' + this.tableEvent.newData.station + '?'
    } else {
      this.dialogMessage = 'Are you sure you want to ' + crud + ' ' + this.tableEvent.data.station + '?'
    }
    this.dialogService.open(dialog, {
      context: this.dialogMessage
    });
  }

  onModifyConfirm(confirmation): void {
    var invalidData = false
    if (confirmation) {
      if (this.modifyType == 'delete') {
        this.fm.deleteFmModule(this.tableEvent.data.uid).subscribe(
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

        if (this.tableEvent.newData.station === "") {
          this.dangerToast('top-right', 'danger', 'Station name invalid.')
          invalidData = true
        }

        if (this.tableEvent.newData.location === "") {
          this.dangerToast('top-right', 'danger', 'Location invalid.')
          invalidData = true
        }

        if (this.tableEvent.newData.type === "") {
          this.dangerToast('top-right', 'danger', 'Type invalid.')
          invalidData = true
        }

        
        if (invalidData == false){
          this.fm.updateFmModule(this.tableEvent.newData).subscribe(
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
          this.fm.createFmModule(this.tableEvent.newData).subscribe(
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
