import { Component } from '@angular/core';

@Component({
  selector: 'ngx-footer',
  styleUrls: ['./footer.component.scss'],
  template: `
    <span class="created-by">Created by <b>Ben Gorham</b> 2019 using <b>Nebular</b>.</span>
    <div class="socials">
    </div>
  `,
})
export class FooterComponent {
}
