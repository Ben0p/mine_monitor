
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Componenets
import { GpsHomeComponent } from './gps-home/gps-home.component';
import { GpsListComponent } from './gps-list/gps-list.component';

const routes: Routes = [
    { path: '', component: GpsHomeComponent },
    { path: 'list', component: GpsListComponent }
  ];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class GpsRoutingModule { }