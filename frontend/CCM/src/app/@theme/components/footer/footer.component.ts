import { Component } from '@angular/core';

@Component({
  selector: 'ngx-footer',
  styleUrls: ['./footer.component.scss'],
  template: `
    <span style="float:left;">Created by <b>Ben Gorham</b></span>
    <span style="float:right;">Ver. <b>2021.01.21 - 69.420</b></span>
  `,
})
export class FooterComponent {
}
