import { Component, HostListener, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule], // Import required modules
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  isSidebarCollapsed = false; // Track sidebar state
  activeLink: string = 'dashboard'; // Track active link

  // Initialize margin on component load
  ngOnInit(): void {
    this.adjustMainContentMargin(); // Set initial margin
  }

  // Toggle sidebar collapse
  toggleSidebar(): void {
    this.isSidebarCollapsed = !this.isSidebarCollapsed;
    this.adjustMainContentMargin(); // Adjust main content margin dynamically
  }

  // Check if a link is active
  isActive(link: string): boolean {
    return this.activeLink === link;
  }

  // Set the active link
  setActive(link: string): void {
    this.activeLink = link;
  }

  // Adjust main content margin based on sidebar state
  private adjustMainContentMargin(): void {
    const mainContent = document.querySelector('.main-content') as HTMLElement;
    if (mainContent) {
      if (this.isSidebarCollapsed) {
        mainContent.style.marginLeft = '70px'; // Collapsed width
      } else {
        mainContent.style.marginLeft = '250px'; // Expanded width
      }
    }
  }

  // Optional: Handle window resize for responsiveness
  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    this.adjustMainContentMargin(); // Re-adjust margin on window resize
  }
}