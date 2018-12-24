import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TrailersRoutingModule } from './trailers-routing.module';

import { TrailersHomeComponent } from './trailers-home/trailers-home.component';

@NgModule({
  declarations: [TrailersHomeComponent],
  imports: [
    TrailersRoutingModule,
    CommonModule
  ]
})
export class TrailersModule { }
