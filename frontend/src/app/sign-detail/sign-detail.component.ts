import { Component, OnInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { DataService } from '../data.service';
import { Sign } from '../sign.model';

@Component({
  selector: 'app-sign-detail',
  templateUrl: './sign-detail.component.html',
  styleUrls: ['./sign-detail.component.scss']
})


export class SignDetailComponent implements OnInit {

  @Input() outputStates = { 
    all_clear:'',
    emergency: '',
    lightning: '',
    a:'',
    b:'',
    c:''
  };

  outputs:any = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private data: DataService
  ) { }

  ngOnInit() {
    this.refreshData();
  }

  ip = this.route.snapshot.paramMap.get('ip');

  refreshData() {
    this.outputs = [];
    this.data.getSignDetail(this.ip)
      .subscribe((data: {}) => {
        console.log(data);
        this.outputs = data;
      })
  }

  setOutputs() {
    this.data.setOutputs(this.ip, this.outputStates).subscribe((results) => {
      console.log(results);
      this.refreshData()
    })
  }


}
