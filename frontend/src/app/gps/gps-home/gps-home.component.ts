import { Component, OnInit, OnDestroy } from "@angular/core";
import { DataService } from "../../data.service";

@Component({
  selector: "app-gps-home",
  templateUrl: "./gps-home.component.html",
  styleUrls: ["./gps-home.component.scss"]
})
export class GpsHomeComponent implements OnInit, OnDestroy {
  gps: any = [];
  interval: any;

  constructor(private data: DataService) {}

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 1000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.data.getCorrections().subscribe((data: {}) => {
      this.gps = data;
    });
  }
}
