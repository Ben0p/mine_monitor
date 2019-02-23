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
  resultsLength = 0;

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

  downloadCorrectionsFile(): void {
    this.data.getCorrectionsFile()
        .subscribe(x => {
            // It is necessary to create a new blob object with mime-type explicitly set
            // otherwise only Chrome works like it should
            var newBlob = new Blob([x], { type: "application/octet-stream" });

            // IE doesn't allow using a blob object directly as link href
            // instead it is necessary to use msSaveOrOpenBlob
            if (window.navigator && window.navigator.msSaveOrOpenBlob) {
                window.navigator.msSaveOrOpenBlob(newBlob);
                return;
            }

            // For other browsers: 
            // Create a link pointing to the ObjectURL containing the blob.
            const data = window.URL.createObjectURL(newBlob);

            var link = document.createElement('a');
            link.href = data;
            link.download = "final.conf";
            // this is necessary as link.click() does not work on the latest firefox
            link.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));

            setTimeout(function () {
                // For Firefox it is necessary to delay revoking the ObjectURL
                window.URL.revokeObjectURL(data);
                link.remove();
            }, 100);
        });
}



}
