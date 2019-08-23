import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'

@Component({
  selector: 'all',
  templateUrl: './all.component.html',
  styleUrls: ['./all.component.scss']
})
export class AllComponent implements OnInit, OnDestroy {
  alerts$: Object;
  interval: any;

  constructor(
    private alerts: AlertService,
  ) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
        this.refreshData();
    }, 2000);
  }

  ngOnDestroy(){
    clearInterval(this.interval);
  }

  refreshData() {
    this.alerts.getAlerts().subscribe(
        (data: {}) => {
            this.alerts$ = data;
        }
    );
  }

  getStatus(alert){
    var status
    if(alert.all_clear){
      status = 'success'
    }
    console.log(status)
    return status
  }

}
