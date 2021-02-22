import { Component, OnInit } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'

@Component({
  selector: 'ngx-alert-list-infinite',
  templateUrl: './alert-list-infinite.component.html',
  styleUrls: ['./alert-list-infinite.component.scss']
})
export class AlertListInfiniteComponent implements OnInit {

  firstCard = {
    news: [],
    placeholders: [],
    loading: false,
    pageToLoadNext: 1,
  };
  secondCard = {
    news: [],
    placeholders: [],
    loading: false,
    pageToLoadNext: 1,
  };
  pageSize = 5;

  constructor(
    private alerts: AlertService,
    ) {}

  loadNext(cardData) {
    if (cardData.loading) { return; }

    cardData.loading = true;
    cardData.placeholders = new Array(this.pageSize);
    this.alerts.loadAlertList(cardData.pageToLoadNext, this.pageSize)
      .subscribe(nextNews => {
        cardData.placeholders = [];
        cardData.news.push(...nextNews);
        cardData.loading = false;
        cardData.pageToLoadNext++;
      });
  }

  ngOnInit() {
  }

}
