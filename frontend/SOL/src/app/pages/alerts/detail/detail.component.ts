import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})

export class DetailComponent implements OnInit, OnDestroy {
  alert: {};
  interval: any;
  uid: any;
  dataAvailable: boolean = false;
  authenticated: boolean = true;
  payload: {};

  constructor(
    private alerts: AlertService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    this.uid = this.route.snapshot.paramMap.get('uid');
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 5000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  
  refreshData() {
    this.alerts.getAlertDetail(this.uid).subscribe(
      (data: {}) => {
        this.alert = data;
        this.dataAvailable = true;
      }
    );
  }

  stateChange(p) {
    if (this.alert['type'] == 'Trailer'){
      this.payload = {
        'ips' : [
          this.alert['modules'][0]['ip'],
          this.alert['modules'][1]['ip'],
          this.alert['modules'][2]['ip'],
        ],
        'type' : p.type,
        'output' : p.output,
        'state' : p.state
      }
    } else {
      this.payload = {
        'ips' : [
          this.alert['ip'],
        ],
        'type' : p.type,
        'output' : p.output,
        'state' : p.state
      }
    }

    this.alerts.postAlertDetail(this.uid, this.payload).subscribe(
      (data: {}) => {
        this.refreshData();
        console.log(data)
      }
    )
  }

}
