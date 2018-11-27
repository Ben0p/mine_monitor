import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Components
import { HomeComponent } from './home/home.component';
import { SignsComponent } from './signs/signs.component';
import { SignDetailComponent } from './sign-detail/sign-detail.component';
import { TrucksComponent } from './trucks/trucks.component';
import { FleetDetailComponent } from './fleet-detail/fleet-detail.component';
import { LoginComponent } from './login/login.component';
import { EditComponent } from './edit/edit.component';

// Auth
import { AuthGuard } from './_guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'alerts',
    component: SignsComponent
  },
  {
    path: 'alerts/:ip',
    component: SignDetailComponent,
    canActivate: [AuthGuard]
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
    path: 'login',
    component: LoginComponent 
  },
  { 
    path: 'edit',
    component: EditComponent 
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
