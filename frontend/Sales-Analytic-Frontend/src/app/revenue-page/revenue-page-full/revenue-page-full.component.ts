import { Component } from '@angular/core';
import { HeaderComponent } from '../header/header.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { RevenuePageComponent } from '../revenue-page/revenue-page.component';

@Component({
  selector: 'app-revenue-page-full',
  imports: [HeaderComponent, SidebarComponent, RevenuePageComponent],
  templateUrl: './revenue-page-full.component.html',
  styleUrl: './revenue-page-full.component.css'
})
export class RevenuePageFullComponent {

}
