import { Component, OnInit } from "@angular/core";
import { FormControl, FormGroup, FormBuilder, Validators } from "@angular/forms";
import { DataService } from "../data.service";
import { Router } from "@angular/router";

export interface Type {
  value: string;
  viewValue: string;
}

export interface alertType {
  value: string;
  viewValue: string;
}

const ipPattern = 
    "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)";
@Component({
  selector: "app-edit",
  templateUrl: "./edit.component.html",
  styleUrls: ["./edit.component.scss"]
})
export class EditComponent implements OnInit {
  selectedType: string;
  alertType: string;

  editForm = new FormGroup({
    type: new FormControl("", Validators.required),
    fleet_name: new FormControl(""),
    fleet_xim: new FormControl(""),
    fleet_screen: new FormControl(""),
    fleet_other: new FormControl("", Validators.pattern(ipPattern)),
    fleet_2: new FormControl(""),
    fleet_5: new FormControl("", Validators.pattern(ipPattern)),
    alert_location: new FormControl(""),
    alert_ip: new FormControl("", Validators.pattern(ipPattern)),
    alert_type: new FormControl(""),
    trailer_number: new FormControl(""),
    west_ip: new FormControl("", Validators.pattern(ipPattern)),
    central_ip: new FormControl("", Validators.pattern(ipPattern)),
    east_ip: new FormControl("", Validators.pattern(ipPattern)),
    parent: new FormControl(""),
    tristar: new FormControl("", Validators.pattern(ipPattern)),
    tropos2: new FormControl("", Validators.pattern(ipPattern)),
    tropos5: new FormControl("", Validators.pattern(ipPattern)),
    troposLAN: new FormControl("", Validators.pattern(ipPattern)),
    cisco1572: new FormControl("", Validators.pattern(ipPattern)),
    ubi: new FormControl("", Validators.pattern(ipPattern)),
    issi: new FormControl(""),
    correction_ip: new FormControl("", Validators.pattern(ipPattern))
  });

  types: Type[] = [
    { value: "fleet", viewValue: "Fleet" },
    { value: "alert", viewValue: "Alert" },
    { value: "trailer", viewValue: "Trailer" },
    { value: "corrections", viewValue: "Correction" }
  ];

  alertTypes: alertType[] = [
    { value: "sign", viewValue: "Sign" },
    { value: "calert", viewValue: "C-Alert" },
    { value: "trailer", viewValue: "Trailer" }
  ];


  constructor(private data: DataService, public router: Router) {}

  ngOnInit() {
    this.onChanges()
  }

  // Set validators dynamically depending on slected type
  onChanges(): void {
    this.editForm.get('type').valueChanges.subscribe(val => {
      console.log(`Type is ${val}.`);
      if (val == 'fleet'){
        this.editForm.controls["fleet_name"].setValidators(Validators.required);
        this.editForm.controls["fleet_name"].updateValueAndValidity();
        this.editForm.controls["fleet_xim"].setValidators([Validators.required, Validators.pattern(ipPattern)]);
        this.editForm.controls["fleet_xim"].updateValueAndValidity();
        this.editForm.controls["fleet_screen"].setValidators([Validators.required, Validators.pattern(ipPattern)]);
        this.editForm.controls["fleet_screen"].updateValueAndValidity();
        this.editForm.controls["fleet_2"].setValidators([Validators.required, Validators.pattern(ipPattern)]);
        this.editForm.controls["fleet_2"].updateValueAndValidity();
      } else if (val == 'alert') {
        this.editForm.controls["alert_location"].setValidators(Validators.required);
        this.editForm.controls["alert_location"].updateValueAndValidity();
        this.editForm.controls["alert_type"].setValidators(Validators.required);
        this.editForm.controls["alert_type"].updateValueAndValidity();
        this.editForm.get('alert_type').valueChanges.subscribe(alertType => {
          if (alertType == 'sign' || alertType == 'calert') {
            this.editForm.controls["alert_ip"].setValidators(Validators.required);
            this.editForm.controls["alert_ip"].updateValueAndValidity();
          } else if (alertType == 'trailer') {
            this.editForm.controls["trailer_number"].setValidators(Validators.required);
            this.editForm.controls["trailer_number"].updateValueAndValidity();
            this.editForm.controls["west_ip"].setValidators(Validators.required);
            this.editForm.controls["west_ip"].updateValueAndValidity();
            this.editForm.controls["central_ip"].setValidators(Validators.required);
            this.editForm.controls["central_ip"].updateValueAndValidity();
            this.editForm.controls["east_ip"].setValidators(Validators.required);
            this.editForm.controls["east_ip"].updateValueAndValidity();
          }
        })
      } else if (val == 'trailer') {
        this.editForm.controls["parent"].setValidators(Validators.required);
        this.editForm.controls["parent"].updateValueAndValidity();
      } else if (val == 'corrections') {
        this.editForm.controls["parent"].setValidators(Validators.required);
        this.editForm.controls["parent"].updateValueAndValidity();
        this.editForm.controls["correction_ip"].setValidators(Validators.required);
        this.editForm.controls["correction_ip"].updateValueAndValidity();
      }
    });
  }

  onSubmit(operation) {
    // TODO: Use EventEmitter with form value
    console.warn(this.editForm.value);
    if (operation == "submit") {
      this.data.edit(this.editForm.value).subscribe(results => {
        console.log(results);
      });
    } else if (operation == "delete") {
      if (this.editForm.value.type == "alert") {
        if (this.editForm.value.alertType == "trailer") {
          this.data
            .delete(
              this.editForm.value.type,
              this.editForm.value.trailer_number
            )
            .subscribe(results => {
              console.log(results);
            });
        } else {
          this.data
            .delete(
              this.editForm.value.type,
              this.editForm.value.alert_location
            )
            .subscribe(results => {
              console.log(results);
            });
        }
      } else if (this.editForm.value.type == "fleet") {
        this.data
          .delete(this.editForm.value.type, this.editForm.value.fleet_name)
          .subscribe(results => {
            console.log(results);
          });
      } else if (this.editForm.value.type == "corrections") {
        this.data
          .delete(this.editForm.value.type, this.editForm.value.correction_ip)
          .subscribe(results => {
            console.log(results);
          });
      } else if (this.editForm.value.type == "trailer") {
        this.data
          .delete(this.editForm.value.type, this.editForm.value.parent)
          .subscribe(results => {
            console.log(results);
          });
      }
    }

    // Rest all exept type
    this.editForm.setValue(
      {
        'type' : this.editForm.value.type,
        'fleet_name' : "",
        'fleet_xim' : "",
        'fleet_screen' : "",
        'fleet_other' : "",
        'fleet_2' : "",
        'fleet_5' : '',
        'alert_location' : '',
        'alert_ip' : "",
        'alert_type' : "",
        'trailer_number' : "",
        'west_ip' : "",
        'central_ip' : "",
        'east_ip' : "",
        'parent' :"",
        'tristar' : "",
        'tropos2' : "",
        'tropos5' : "",
        'troposLAN' : "",
        'cisco1572' : "",
        'ubi' : "",
        'issi' : "",
        'correction_ip' : ""
      }
    )

    // this.router.navigateByUrl('/alerts');
    
  }
}
