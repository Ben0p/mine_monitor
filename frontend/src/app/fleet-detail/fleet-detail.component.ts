import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { DataService } from '../data.service';

@Component({
  selector: 'app-fleet-detail',
  templateUrl: './fleet-detail.component.html',
  styleUrls: ['./fleet-detail.component.scss']
})


export class FleetDetailComponent implements OnInit, OnDestroy {

  fleet$: Object;
  interval: any;
  count: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private data: DataService
  ) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 1000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  name = this.route.snapshot.paramMap.get('name');

  refreshData() {

    this.data.fleetDetail(this.name)
      .subscribe((data: {}) => {
        this.fleet$ = data;
      })
  }

  somethingOffline(xim, two, screen) {
    this.count = [xim, two, screen].filter(Boolean).length
    if (this.count > 0 && this.count < 3) {
      return (true);
    } else {
      return (false)
    }
  }

  externalLink(device, ip, online) {
    if (device === "tropos" && online) {
      window.open("https://"+ip, "_blank");
    } else if (device === "xim" && online) {
      window.open("http://"+ip+':3785/getinfocore', "_blank");
    } else if (device === "ms352" && online) {
      window.open("http://"+ip, "_blank");
    }
    
  }

}
