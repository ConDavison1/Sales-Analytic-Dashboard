import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent implements OnInit {
  isDarkMode = false;

  ngOnInit(): void {
    const savedMode = localStorage.getItem('dark-mode');
    this.isDarkMode = savedMode === 'true';
    document.body.classList.toggle('dark-mode', this.isDarkMode);
  }

  toggleDarkMode(): void {
    this.isDarkMode = !this.isDarkMode;
    document.body.classList.toggle('dark-mode', this.isDarkMode);
    localStorage.setItem('dark-mode', this.isDarkMode.toString());
  }
}
