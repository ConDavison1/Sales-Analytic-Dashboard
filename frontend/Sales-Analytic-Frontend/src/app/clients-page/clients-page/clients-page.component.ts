import { Component } from '@angular/core';
import { HeaderComponent } from '../header/header.component';
import { SidebarComponent } from '../sidebar/sidebar.component';

@Component({
  selector: 'app-clients-page',
  imports: [HeaderComponent, SidebarComponent],
  templateUrl: './clients-page.component.html',
  styleUrl: './clients-page.component.css'
})
export class ClientsPageComponent {

}
