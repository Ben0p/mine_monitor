/**
 * @license
 * Copyright Akveo. All Rights Reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 */
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { CoreModule } from './@core/core.module';
import { ThemeModule } from './@theme/theme.module';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import {
  NbChatModule,
  NbDatepickerModule,
  NbDialogModule,
  NbMenuModule,
  NbSidebarModule,
  NbToastrModule,
  NbWindowModule,
} from '@nebular/theme';
import { NbEvaIconsModule } from '@nebular/eva-icons';
import { ComponentsModule } from './@components/components.module';
import { AuthGuard } from './@auth/auth-guard.service';
import { RoleProvider } from './@auth/role.provider';
import { NbSecurityModule, NbRoleProvider } from '@nebular/security';


@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    NbSidebarModule.forRoot(),
    NbMenuModule.forRoot(),
    NbDatepickerModule.forRoot(),
    NbDialogModule.forRoot(),
    NbWindowModule.forRoot(),
    NbToastrModule.forRoot(),
    NbChatModule.forRoot(),
    CoreModule.forRoot(),
    ThemeModule.forRoot(),
    NbEvaIconsModule,
    ComponentsModule,
    NbSecurityModule.forRoot({
      accessControl: {
        view: {
          view: [
            'alerts',
            'dashboards',
            'alerts_overview',
            'alerts_all',
            'alerts_display',
            'settings',
            'settings_style',
            'wind',
            'wind_all',
            'tetra',
            'tetra_nodes',
            'power',
            'tetra_subscribers',
            'solar',
            'solar_controllers',
            'gen',
            'gen_status',
            'fm',
            'fm_status',
            'map',
            'ups',
            'ups_status',
            'weather',
            'weather_wind',
            'inspections',
            'inspections_list'
          ],
        },
        admin: {
          parent: 'view',
          view: [
            'alerts_list',
            'alerts_controls',
            'alerts_info',
            'alerts_edit',
            'fm_edit',
            'solar_edit',
            'ups_edit',
            'inspections_upload',
          ],
        },
        generators: {
          view: [
            'power',
            'gen',
            'gen_status',
            'settings',
            'settings_style',

          ],
        },
      },
    }),
  ],
  bootstrap: [
    AppComponent
  ],
  providers: [
    AuthGuard,
    { 
      provide: NbRoleProvider,
      useClass: RoleProvider
    },
  ]
})
export class AppModule {
}
