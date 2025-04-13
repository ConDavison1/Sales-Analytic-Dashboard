import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { WinsService } from '../../services/wins-services/wins.service';

@Component({
  standalone: true,
  selector: 'app-wins-page',
  templateUrl: './wins-page.component.html',
  styleUrls: ['./wins-page.component.css'],
  imports: [
    CommonModule,
    NgApexchartsModule,
    SidebarComponent,
    HeaderComponent,
  ],
})
export class WinsPageComponent implements OnInit {
  username = '';
  year = 2024;

  isDataLoaded = false;
  loadCount = 0;
  totalLoads = 4;

  cards: any[] = [];
  wins: any[] = [];

  chartOptionsOne: any = {}; 
  chartOptionsTwo: any = {}; 

  constructor(private winsService: WinsService) {}

  ngOnInit(): void {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    this.username = user.username || '';

    if (this.username) {
      this.loadWins();
      this.loadQuarterlyCards();
      this.loadCategoryChart();
      this.loadEvolutionChart();
    }
  }

  private markLoaded(): void {
    this.loadCount++;
    if (this.loadCount >= this.totalLoads) {
      this.isDataLoaded = true;
    }
  }

  loadWins(): void {
    this.winsService.getWins(this.username, this.year).subscribe({
      next: (res) => {
        this.wins = res.wins.map((w: any) => ({
          opportunity_id: w.win_id,
          client_name: w.client_name,
          client_industry: w.client_industry,
          win_level: w.win_level,
          forecast_category: w.win_category.toUpperCase(),
          win_date: `${w.fiscal_year} Q${w.fiscal_quarter}`,
        }));
        this.markLoaded();
      },
      error: (err) => {
        console.error('Wins fetch error:', err);
        this.markLoaded();
      },
    });
  }

  loadQuarterlyCards(): void {
    this.winsService.getWinsQuarterlyTargets(this.username, this.year).subscribe({
      next: (res) => {
        const quarters = res.quarterly_targets || [];
        this.cards = quarters.map((q: any) => ({
          title: `Q${q.quarter} Wins`,
          value: q.accumulated_value,
          percentage: `${q.achievement_percentage.toFixed(1)}% Achieved`,
        }));
        this.markLoaded();
      },
      error: (err) => {
        console.error('Quarterly target error:', err);
        this.markLoaded();
      },
    });
  }

  loadCategoryChart(): void {
    this.winsService.getWinsCategoryDistribution(this.username, this.year).subscribe({
      next: (res) => {
        this.chartOptionsOne = {
          chart: {
            type: 'line',
            height: 350,
            stacked: true,
            toolbar: {
              show: false,
            },
          },
          series: res.series,
          colors: ['#4285F4', '#34A853', '#FBBC05', '#EA4335', '#A142F4', '#00ACC1'],
          xaxis: {
            categories: res.quarters,
          },
          stroke: {
            curve: 'smooth',
            width: 2,
          },
          tooltip: {
            shared: true,
            intersect: false,
          },
          legend: {
            position: 'bottom',
          },
        };
        this.markLoaded();
      },
      error: (err) => {
        console.error('Category distribution error:', err);
        this.markLoaded();
      },
    });
  }
  
  loadEvolutionChart(): void {
    this.winsService.getWinsOverTime(this.username, this.year).subscribe({
      next: (res) => {
        this.chartOptionsTwo = {
          chart: {
            type: 'line',
            height: 350,
            toolbar: {
              show: false,
            },
          },
          colors: ['#4285F4'], // Google blue for Total Wins line
          series: [
            {
              name: 'Total Wins',
              data: res.win_evolution.map((e: any) => e.win_count),
            },
          ],
          xaxis: {
            categories: res.categories,
          },
          stroke: {
            curve: 'smooth',
          },
          tooltip: {
            shared: true,
            intersect: false,
          },
          legend: {
            position: 'bottom',
          },
        };
        this.markLoaded();
      },
      error: (err) => {
        console.error('Wins evolution error:', err);
        this.markLoaded();
      },
    });
  }
  
  
}
