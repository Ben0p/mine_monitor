// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { TrailersRoutingModule } from './trailers-routing.module';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

// Material
import { MaterialModule } from '../material';

// Components
import { TrailersHomeComponent } from './trailers-home/trailers-home.component';

@NgModule({
  declarations: [
    TrailersHomeComponent
  ],
  imports: [
    TrailersRoutingModule,
    MaterialModule,
    FlexLayoutModule,
    FormsModule,
    ReactiveFormsModule,
    CommonModule
  ]
})
export class TrailersModule { }
