import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Components
import { HomeComponent } from './home/home.component';
import { SignsComponent } from './signs/signs.component';
import { SignDetailComponent } from './sign-detail/sign-detail.component';
import { TrucksComponent } from './trucks/trucks.component';
import { FleetDetailComponent } from './fleet-detail/fleet-detail.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'signs',
    component: SignsComponent
  },
  {
    path: 'signs/:ip',
    component: SignDetailComponent
  },
  {
    path: 'fleet',
    component: TrucksComponent
  },
  {
    path: 'fleet/:name',
    component: FleetDetailComponent
  },
  { 
    path: '**', 
    component: HomeComponent 
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
