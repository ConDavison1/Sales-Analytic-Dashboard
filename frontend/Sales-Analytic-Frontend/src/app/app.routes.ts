import { LandingPageComponent } from './landing-page/landing-page/landing-page.component';
import { RevenuePageFullComponent } from './revenue-page/revenue-page-full/revenue-page-full.component';
import { DashboardComponent } from './landing-page/dashboard/dashboard.component';
import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { ClientsPageComponent } from './clients-page/clients-page/clients-page.component';
import { SigningsPageComponent } from './signings-page/signings-page/signings-page.component';
import { WinsPageComponent } from './wins-page/wins-page/wins-page.component';

export const appRoutes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'landing-page', component: LandingPageComponent },
  { path: 'revenue-page', component: RevenuePageFullComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'clients-page', component: ClientsPageComponent },
  { path: 'signings', component: SigningsPageComponent },
  { path: 'count-to-wins', component: WinsPageComponent },
];
