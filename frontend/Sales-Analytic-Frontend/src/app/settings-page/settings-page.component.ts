import { Component, inject } from '@angular/core';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { HeaderComponent } from '../header/header.component';
import { ThemeService } from '../services/theme-service/theme.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings-page',
  imports: [SidebarComponent, HeaderComponent,  CommonModule],
  templateUrl: './settings-page.component.html',
  styleUrl: './settings-page.component.css'
})
export class SettingsPageComponent {
  // settings ideas, light / dark mode, change password, change email, high contrast mode, time zone, default export preference
  
  themeService = inject(ThemeService);
  theme = this.themeService.getTheme();

  toggleTheme() {
    this.themeService.toggleTheme();
  }
}
