import { LandingPageComponent } from './landing-page/landing-page/landing-page.component';
import { RevenuePageFullComponent } from './revenue-page/revenue-page-full/revenue-page-full.component';
import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { ClientsPageComponent } from './clients-page/clients-page/clients-page.component';
import { SigningsPageComponent } from './signings-page/signings-page/signings-page.component';
import { PipelinePageComponent } from './pipeline-page/pipeline-page/pipeline-page.component';

export const appRoutes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'landing-page', component: LandingPageComponent },
  { path: 'revenue-page', component: RevenuePageFullComponent },
  { path: 'clients-page', component: ClientsPageComponent },
  { path: 'signings', component: SigningsPageComponent },
  { path: 'pipeline', component: PipelinePageComponent },
];
