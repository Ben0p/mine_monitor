import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signs',
  templateUrl: './signs.component.html',
  styleUrls: ['./signs.component.scss']
})

export class SignsComponent implements OnInit {

  signs$: Object;

  interval: any;

  constructor(private data: DataService, private router: Router) { }
  toggle (content) {
    window.open("http://root:00000000@"+content, "_blank");
  }


  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => { 
      this.refreshData(); 
    }, 5000);

  }

  refreshData() {
    this.data.getSigns().subscribe(
      data => this.signs$ = data
    );
  }

}
