import { Component, HostListener, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { RouterModule } from '@angular/router';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css'],
})
export class SidebarComponent implements OnInit, AfterViewInit {
  isSidebarCollapsed = false;
  isMobileSidebarVisible = false;
  activeLink: string = '';
  username: string | null = null;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService // ✅ Inject AuthService
  ) {}

  ngOnInit(): void {
    this.username = this.authService.getUsername(); // ✅ Get normalized username
    console.log('Sidebar username:', this.username);

    this.handleInitialSidebarState();

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        const currentRoute = this.activatedRoute.snapshot.firstChild?.routeConfig?.path;
        if (currentRoute) {
          this.setActive(currentRoute);
        }

        if (window.innerWidth <= 768) {
          this.isMobileSidebarVisible = false;
        }

        this.adjustMainContentMargin();
      }
    });
  }

  ngAfterViewInit(): void {
    setTimeout(() => this.adjustMainContentMargin(), 0);
  }

  toggleSidebar(): void {
    if (window.innerWidth <= 768) {
      this.isMobileSidebarVisible = !this.isMobileSidebarVisible;
    } else {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
      this.adjustMainContentMargin();
    }
  }

  setActive(link: string): void {
    this.activeLink = link;
  }

  private handleInitialSidebarState(): void {
    const width = window.innerWidth;

    if (width <= 768) {
      this.isSidebarCollapsed = false;
      this.isMobileSidebarVisible = false;
    } else {
      this.isSidebarCollapsed = false;
    }

    this.adjustMainContentMargin();
  }

  private adjustMainContentMargin(): void {
    const mainContent = document.querySelector('.main-content') as HTMLElement;

    if (mainContent) {
      if (window.innerWidth <= 768) {
        mainContent.style.marginLeft = '0px';
      } else {
        mainContent.style.marginLeft = this.isSidebarCollapsed ? '70px' : '250px';
      }
    }
  }

  @HostListener('window:resize', ['$event'])
  onResize(): void {
    if (window.innerWidth <= 768) {
      this.isMobileSidebarVisible = false;
    }

    this.adjustMainContentMargin();
  }

  onLogout(): void {
    this.authService.logout(); 
    this.router.navigate(['/login']);
  }
}
