import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StyleComponent } from './style/style.component';
import { SettingsComponent } from './settings.component'


const routes: Routes = [{
  path: '',
  component: SettingsComponent,
  children: [
    {
      path: 'style',
      component: StyleComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class SettingsRoutingModule {
}
export const routedComponents = [
    StyleComponent,
  ];