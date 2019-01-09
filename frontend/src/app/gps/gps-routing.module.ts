
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Componenets
import { GpsHomeComponent } from './gps-home/gps-home.component';

const routes: Routes = [
    { path: '', component: GpsHomeComponent }
  ];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class GpsRoutingModule { }