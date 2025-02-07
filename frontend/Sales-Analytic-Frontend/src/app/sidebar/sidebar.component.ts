import { Component, HostListener, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute } from '@angular/router'; 
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule], 
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  isSidebarCollapsed = false; 
  activeLink: string = ''; 

  constructor(private router: Router, private activatedRoute: ActivatedRoute) { }

  
  ngOnInit(): void {
    this.adjustMainContentMargin(); 

    
    this.router.events.subscribe(() => {
      const currentRoute = this.activatedRoute.snapshot.firstChild?.routeConfig?.path;
      if (currentRoute) {
        this.setActive(currentRoute); 
      }
    });
  }

  
  toggleSidebar(): void {
    this.isSidebarCollapsed = !this.isSidebarCollapsed;
    this.adjustMainContentMargin(); 
  }

  
  setActive(link: string): void {
    this.activeLink = link;
  }

  
  private adjustMainContentMargin(): void {
    const mainContent = document.querySelector('.main-content') as HTMLElement;
    if (mainContent) {
      if (this.isSidebarCollapsed) {
        mainContent.style.marginLeft = '70px'; 
      } else {
        mainContent.style.marginLeft = '250px'; 
      }
    }
  }

  
  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    this.adjustMainContentMargin(); 
  }
}
