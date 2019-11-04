import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss'],

})

export class DetailComponent implements OnInit {

  name: any;

  constructor(
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    this.name = this.route.snapshot.paramMap.get('name');
  }

}
