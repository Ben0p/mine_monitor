
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Componenets
import { ServicesHomeComponent } from './services-home/services-home.component';

const routes: Routes = [
    { path: '', component: ServicesHomeComponent }
  ];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class ServicesRoutingModule { }