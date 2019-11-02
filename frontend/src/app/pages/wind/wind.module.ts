import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WindComponent } from './wind.component';
import { AllComponent } from './all/all.component';
import { WindRoutingModule, routedComponents } from './wind-routing.module';

@NgModule({
  declarations: [
    ...routedComponents,
    AllComponent,
    WindComponent,

  ],
  imports: [
    WindRoutingModule,
    CommonModule,
  ]
})
export class WindModule { }
