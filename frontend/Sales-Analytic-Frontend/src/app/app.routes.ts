import { LandingPageComponent } from './landing-page/landing-page/landing-page.component';
import { RevenuePageComponent } from './revenue-page/revenue-page/revenue-page.component';
import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { ClientsPageComponent } from './clients-page/clients-page/clients-page.component';

export const appRoutes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' }, 
  { path: 'landing-page', component: LandingPageComponent},
  { path: 'revenue-page', component: RevenuePageComponent},
  { path: 'clients-page', component: ClientsPageComponent}
];