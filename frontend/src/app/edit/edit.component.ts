import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, FormBuilder } from '@angular/forms';
import { DataService } from '../data.service';


export interface Type {
  value: string;
  viewValue: string;
}

export interface alertType {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.scss']
})
export class EditComponent implements OnInit {

  selectedType: string;
  alertType: string;

  editForm = new FormGroup({
    type: new FormControl(''),
    fleet_name: new FormControl(''),
    fleet_xim: new FormControl(''),
    fleet_screen: new FormControl(''),
    fleet_other: new FormControl(''),
    fleet_2: new FormControl(''),
    fleet_5: new FormControl(''),
    alert_location: new FormControl(''),
    alert_ip: new FormControl(''),
    alert_type: new FormControl(''),
  });

  types: Type[] = [
    {value: 'fleet', viewValue: 'Fleet'},
    {value: 'alert', viewValue: 'Alert'}
  ];

  alertTypes: alertType[] = [
    {value: 'sign', viewValue: 'Sign'},
    {value: 'calert', viewValue: 'C-Alert'},
    {value: 'trailer', viewValue: 'Trailer'}
  ];

  constructor(
    private data: DataService
  ) { }

  ngOnInit() {
  }

  onSubmit() {
    // TODO: Use EventEmitter with form value
    console.warn(this.editForm.value);
    this.data.edit(this.editForm.value).subscribe((results) => {
      console.log(results)
    })
  
  }

}
