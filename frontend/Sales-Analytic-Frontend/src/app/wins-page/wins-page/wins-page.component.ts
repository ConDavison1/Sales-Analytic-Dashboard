import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { WinsService } from '../../services/wins-services/wins.service';

@Component({
  selector: 'app-wins-page',
  standalone: true,
  imports: [HeaderComponent, SidebarComponent, CommonModule],
  templateUrl: './wins-page.component.html',
  styleUrl: './wins-page.component.css',
})
export class WinsPageComponent implements OnInit {
  constructor(
    private winsService: WinsService,
    private dashboardService: DashboardService
  ) {}

  wins: any[] = [];
  isLoadingWins: boolean = true;

  sortColumn: string = '';
  sortDirection: 'asc' | 'desc' = 'asc';

  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  ngOnInit(): void {
    this.fetchCardData();
    this.fetchWins();
  }

  fetchWins(): void {
    this.winsService.getWins().subscribe((response: any[]) => {
      this.wins = response;
    });
  }

  sortTable(column: string) {
    if (this.sortColumn === column) {
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortColumn = column;
      this.sortDirection = 'asc';
    }
  

  this.wins.sort((a, b) => {
    const valueA = a[column];
    const valueB = b[column];

    if (typeof valueA === 'number' && typeof valueB === 'number') {
      return this.sortDirection === 'asc' ? valueA - valueB : valueB - valueA;
    } else {
      return this.sortDirection === 'asc'
        ? valueA.toString().localeCompare(valueB.toString())
        : valueB.toString().localeCompare(valueA.toString());
    }
  });
}



  fetchCardData(): void {
    this.dashboardService.getPipelineCount().subscribe((response) => {
      this.pipelineCount = response.pipeline_count;
    });

    this.dashboardService.getRevenueSum().subscribe((response) => {
      this.revenueCount = response.revenue_sum;
    });

    this.dashboardService.getSigningsCount().subscribe((response) => {
      this.signingsCount = response.signings_count;
    });

    this.dashboardService.getWinsCount().subscribe((response) => {
      this.winsCount = response.wins_count;
    });
  }

  get cards() {
    return [
      {
        title: 'Pipeline',
        value: `$${this.pipelineCount}`,
        percentage: '+55%',
      },
      { title: 'Revenue', value: `$${this.revenueCount}`, percentage: '+5%' },
      {
        title: 'Signings',
        value: `$${this.signingsCount}`,
        percentage: '+89%',
      },
      {
        title: 'Count To Wins',
        value: `${this.winsCount}`,
        percentage: '-14%',
      },
    ];
  }
}
