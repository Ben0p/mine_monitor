import { Component } from '@angular/core';

@Component({
  selector: 'ngx-footer',
  styleUrls: ['./footer.component.scss'],
  template: `
    <span style="float:left;">Created by <b>Ben Gorham</b> 2019</span>
    <span style="float:right;">Ver. <b>2019.12.29</b></span>
  `,
})
export class FooterComponent {
}
