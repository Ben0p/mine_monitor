
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Componenets
import { TrailersHomeComponent } from './trailers-home/trailers-home.component';

const routes: Routes = [
    { path: '', component: TrailersHomeComponent }
  ];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class TrailersRoutingModule { }