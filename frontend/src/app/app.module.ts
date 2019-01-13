// Modules
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { FlexLayoutModule } from '@angular/flex-layout';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

// Material
import { MaterialModule } from './material';

// Components
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { SignsComponent } from './signs/signs.component';
import { SignDetailComponent } from './sign-detail/sign-detail.component';
import { TrucksComponent } from './trucks/trucks.component';
import { FleetDetailComponent } from './fleet-detail/fleet-detail.component';
import { LoginComponent } from './login/login.component';
import { PizzaPartyComponent } from './app.component';

// Helpers
import { BasicAuthInterceptor } from './_helpers/basic-auth.Interceptor';
import { ErrorInterceptor } from './_helpers/error.Interceptor';

// Fake backend for the login component
import { fakeBackendProvider } from './_helpers/fake-backend';
import { EditComponent } from './edit/edit.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    SignsComponent,
    SignDetailComponent,
    TrucksComponent,
    FleetDetailComponent,
    LoginComponent,
    EditComponent,
    PizzaPartyComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    FlexLayoutModule,
    HttpModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    ServiceWorkerModule.register('ngsw-worker.js', { enabled: environment.production })
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: BasicAuthInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    fakeBackendProvider
  ],
  entryComponents: [ 
    PizzaPartyComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
