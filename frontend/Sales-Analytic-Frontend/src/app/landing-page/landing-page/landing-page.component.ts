import { Component } from '@angular/core';
import { HeaderComponent } from "../header/header.component";
import { SidebarComponent } from "../sidebar/sidebar.component";
import { DashboardComponent } from "../dashboard/dashboard.component";


@Component({
  selector: 'app-landing-page',
  imports: [HeaderComponent, SidebarComponent, DashboardComponent],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.css'
})
export class LandingPageComponent {

}
