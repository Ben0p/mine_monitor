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
    all_clear: '',
    emergency: '',
    lightning: '',
    a: '',
    b: '',
    c: ''
  };

  outputs: any = [];
  signs$: Object;
  interval: any;

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

  ip = this.route.snapshot.paramMap.get('ip');

  refreshData() {
    this.outputs = [];

    this.data.getAlertDetail(this.ip)
      .subscribe((data: {}) => {
        this.outputs = data;

        if (this.outputs.all_clear == true) {
          this.outputStates.all_clear = '1'
        } else {
          this.outputStates.all_clear = ''
        }

        if (this.outputs.emergency == true) {
          this.outputStates.emergency = '1'
        } else {
          this.outputStates.emergency = ''
        }

        if (this.outputs.lightning == true) {
          this.outputStates.lightning = '1'
        } else {
          this.outputStates.lightning = ''
        }

        if (this.outputs.a == true) {
          this.outputStates.a = '1'
        } else {
          this.outputStates.a = ''
        }

        if (this.outputs.b == true) {
          this.outputStates.b = '1'
        } else {
          this.outputStates.b = ''
        }

        if (this.outputs.c == true) {
          this.outputStates.c = '1'
        } else {
          this.outputStates.c = ''
        }

      })

    this.data.getAlerts().subscribe(
      data => this.signs$ = data
    );

  }

  setOutputs() {
    this.data.setOutputs(this.ip, this.outputStates).subscribe((results) => {
      this.refreshData()
    })
  }

  onChange(event, output) {
    if (event.checked == true) {
      this.outputStates[output] = '1'
      this.setOutputs()
    } else {
      this.outputStates[output] = ''
      this.setOutputs()
    }
  }

}
