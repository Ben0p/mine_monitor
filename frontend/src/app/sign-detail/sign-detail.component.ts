import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { DataService } from '../data.service';
import { Sign } from '../sign.model';

@Component({
  selector: 'app-sign-detail',
  templateUrl: './sign-detail.component.html',
  styleUrls: ['./sign-detail.component.scss']
})


export class SignDetailComponent implements OnInit, OnDestroy {

  @Input() outputStates = {
    ip: '',
    all_clear: '',
    emergency: '',
    lightning: '',
    a: '',
    b: '',
    c: ''
  };

  outputs: any = [];
  alert$: Object;
  interval: any;
  dataLoaded: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private data: DataService
  ) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 5000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  name = this.route.snapshot.paramMap.get('name');

  refreshData() {

    this.data.alertDetail(this.name)
      .subscribe((data: {}) => {
        this.alert$ = data;
        this.dataLoaded = true
        this.outputStates['all_clear'] = this.alert$['all_clear']
        this.outputStates['emergency'] = this.alert$['emergency']
        this.outputStates['lightning'] = this.alert$['lightning']
        this.outputStates['a'] = this.alert$['a']
        this.outputStates['b'] = this.alert$['b']
        this.outputStates['c'] = this.alert$['c']
        this.outputStates['ip'] = this.alert$['ip']
      })

  }

  setOutputs() {
    this.data.setOutputs(this.name, this.outputStates).subscribe((results) => {
      this.outputStates['all_clear'] = this.alert$['all_clear'] = results[0]
      this.outputStates['emergency'] = this.alert$['emergency'] = results[1]
      this.outputStates['lightning'] = this.alert$['lightning'] = results[2]
      this.outputStates['a'] = this.alert$['a'] = results[3]
      this.outputStates['b'] = this.alert$['b'] = results[4]
      this.outputStates['c'] = this.alert$['c'] = results[5]
    })
  }

  onChange(event, output) {
    if (event.checked == true) {
      this.outputStates[output] = true
      this.setOutputs()
    } else {
      this.outputStates[output] = false
      this.setOutputs()
    }
  }

}
