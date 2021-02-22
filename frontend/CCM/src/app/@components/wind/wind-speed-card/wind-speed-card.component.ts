import { Component, Input } from '@angular/core';
import { NbThemeService } from '@nebular/theme';

@Component({
  selector: 'ngx-wind-speed-card',
  styleUrls: ['./wind-speed-card.component.scss'],
  templateUrl: './wind-speed-card.component.html',
})

export class WindSpeedCardComponent {

  @Input() location: string;
  @Input() speed: any;
  @Input() status: string;
  @Input() on = true;
  @Input() info: string;

  theme: string = 'dark';


  constructor(
    private themeService: NbThemeService
  ) {

    this.theme = this.themeService.currentTheme

    console.log(this.speed)

    if (this.theme == 'cosmic') {
      this.theme = 'dark'
    } else if (this.theme == 'dark') {
      this.theme = 'dark'
    } else {
      this.theme = 'light'
    }
  }

}