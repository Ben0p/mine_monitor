import { Component, OnDestroy, OnInit, TemplateRef } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AlertService } from '../../../@core/data/alerts.service'
import { NbDialogService, NbToastrService } from '@nebular/theme';

@Component({
  selector: 'ngx-alert-table-zones',
  templateUrl: './alert-table-zones.component.html',
  styleUrls: ['./alert-table-zones.component.scss'],
})

export class AlertTableZonesComponent implements OnDestroy, OnInit {

  alertForm: FormGroup;
  submitted = false;
  alertZones: Object;
  alertTypes: Object;

  zoneSettings: Object = {
    add: {
      addButtonContent: '<i class="nb-plus"></i>',
      createButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmCreate: true,
    },
  }


  loadZoneTableSettings() {
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
          title: 'Zone Name',
          type: 'string',
        },
        uid: {
          title: 'UID',
          type: 'string',
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
    private formBuilder: FormBuilder,
    private router: Router
  ) {

  }

    refreshData(){
      this.alerts.getAlertZonesList().subscribe(
        ( data: {} ) => {
          this.source = data;
          this.zoneSettings = this.loadZoneTableSettings();
        }
      )

    }

  ngOnDestroy(): void { }

  ngOnInit() {
    this.refreshData()
  }

  refreshPage(){
    this.router.navigateByUrl('/', {skipLocationChange: true}).then(()=>
    this.router.navigate(['/pages/alerts/edit']));
  }


  onDialog(dialog: TemplateRef<any>, crud, event) {
    this.tableEvent = event;
    this.modifyType = crud;
    if (crud == 'create') {
      this.dialogMessage = 'Are you sure you want to ' + crud + ' ' + this.tableEvent.newData.name + '?'
    } else {
      this.dialogMessage = 'Are you sure you want to ' + crud + ' ' + this.tableEvent.data.name + '?'
    }
    console.log(this.dialogMessage)
    this.dialogService.open(dialog, {
      context: this.dialogMessage
    });
  }

  onModifyConfirm(confirmation): void {
    var invalidData = false
    if (confirmation) {
      if (this.modifyType == 'delete') {
        this.alerts.deleteAlertZone(this.tableEvent.data).subscribe(
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

        if (this.tableEvent.newData.name === "") {
          this.dangerToast('top-right', 'danger', 'Name invalid.')
          invalidData = true
        }
        
        if (invalidData == false){
          this.alerts.updateAlertZone(this.tableEvent.newData).subscribe(
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

        if (this.tableEvent.newData.name === "") {
          this.dangerToast('top-right', 'danger', 'Name invalid.')
          invalidData = true
        }
        
        if (invalidData == false){
          this.alerts.createAlertZone(this.tableEvent.newData).subscribe(
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
    this.refreshPage()
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