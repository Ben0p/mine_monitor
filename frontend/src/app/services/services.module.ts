// Modules
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServicesRoutingModule } from './services-routing.module';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

// Material
import { MaterialModule } from '../material';

// Components
import { ServicesHomeComponent } from './services-home/services-home.component';

@NgModule({
  declarations: [
    ServicesHomeComponent
  ],
  imports: [
    CommonModule,
    ServicesRoutingModule,
    MaterialModule,
    FlexLayoutModule,
    FormsModule,
    ReactiveFormsModule,
  ]
})
export class ServicesModule { }
