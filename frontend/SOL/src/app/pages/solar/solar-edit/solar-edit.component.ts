import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';
import { FormGroup} from '@angular/forms';
import { SolarService } from '../../../@core/data/solar.service'
import { NbDialogService, NbToastrService } from '@nebular/theme';

@Component({
  selector: 'solar-edit',
  templateUrl: './solar-edit.component.html',
  styleUrls: ['./solar-edit.component.scss'],
})

export class SolarEditComponent implements OnDestroy, OnInit {

  alertForm: FormGroup;
  submitted = false;
  alertZones: Object;
  models = [
    {
      'title': 'Tristar-60 MPPT',
      'value': 'Tristar-60 MPPT'
    },
    {
      'title': 'Tristar MPPT 600V',
      'value': 'Tristar MPPT 600V'
    }
  ];

  controllerSettings: Object = {
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
        model: {
          title: 'Model',
          type: 'string',
          editor: {
            type: 'list',
            config: {
              list: this.models
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


  controllerSource: Object
  tableEvent: any
  modifyType: string
  dialogMessage: string
  private index: number = 0;
  postResult: object
  alertsArray: Object
  ipPattern = new RegExp("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
  whiteSpace = new RegExp("([^\\s]*)")


  constructor(
    private solar: SolarService,
    private dialogService: NbDialogService,
    private toastrService: NbToastrService,
  ) {}

    refreshData(){
      this.solar.getSolarControllers().subscribe(
        (
          data: {}) => {
          this.controllerSource = data;
          this.controllerSettings = this.loadModuleTableSettings();
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
        this.solar.deleteSolarController(this.tableEvent.data.uid).subscribe(
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
          this.solar.updateSolarController(this.tableEvent.newData).subscribe(
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
          this.solar.createSolarController(this.tableEvent.newData).subscribe(
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