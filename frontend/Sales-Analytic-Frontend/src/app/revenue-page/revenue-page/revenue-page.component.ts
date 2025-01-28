import { Component } from '@angular/core';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { HeaderComponent } from '../header/header.component';

@Component({
  selector: 'app-revenue-page',
  imports: [HeaderComponent, SidebarComponent],
  standalone: true,
  templateUrl: './revenue-page.component.html',
  styleUrl: './revenue-page.component.css'
})
export class RevenuePageComponent {

}
