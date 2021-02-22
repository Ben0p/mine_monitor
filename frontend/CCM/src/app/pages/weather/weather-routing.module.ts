import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { WeatherComponent } from './weather.component';
import { WeatherWindComponent } from './weather-wind/weather-wind.component';


const routes: Routes = [{
  path: '',
  component: WeatherComponent,
  children: [
    {
      path: 'wind',
      component: WeatherWindComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WindRoutingModule { }
export const routedComponents = [
  WeatherComponent,
  WeatherWindComponent
];