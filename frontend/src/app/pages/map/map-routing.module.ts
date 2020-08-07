import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { MapComponent } from './map.component';
import { MapBaseComponent } from './map-base/map-base.component';


const routes: Routes = [{
  path: '',
  component: MapComponent,
  children: [
    {
      path: 'base',
      component: MapBaseComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GenRoutingModule { }
export const routedComponents = [
  MapComponent,
  MapBaseComponent,
];