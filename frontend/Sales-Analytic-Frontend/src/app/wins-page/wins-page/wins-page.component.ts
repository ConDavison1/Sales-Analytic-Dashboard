import {
  Component,
  OnInit,
  AfterViewInit,
  OnDestroy,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule, ChartComponent } from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { WinsService } from '../../services/wins-services/wins.service';
import { FormsModule } from '@angular/forms';

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
    FormsModule
  ],
})
export class WinsPageComponent implements OnInit, AfterViewInit, OnDestroy {
  username = '';
  year = 2024;

  isDataLoaded = false;
  loadCount = 0;
  totalLoads = 4;

  cards: any[] = [];
  wins: any[] = [];
  winsUnfiltered: any[] = [];

  showFilterOverlay: boolean = false;
  searchTerm: string = '';

  selectedFilters: {
    win_category: Set<string>;
    client_industry: Set<string>;
  } = {
    win_category: new Set<string>(),
    client_industry: new Set<string>()
  };

  uniqueCategories: string[] = [];
  uniqueIndustries: string[] = [];

  chartOptionsOne: any = {};
  chartOptionsTwo: any = {};

  // Ensure these match your template references (e.g., #categoryChartRef in your template)
  @ViewChild('categoryChartRef') categoryChartRef!: ChartComponent;
  @ViewChild('evolutionChartRef') evolutionChartRef!: ChartComponent;

  // MutationObserver to detect dark-mode changes.
  private themeObserver!: MutationObserver;

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

    // Set up a MutationObserver to watch for changes to the body's class attribute.
    this.themeObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (
          mutation.type === 'attributes' &&
          mutation.attributeName === 'class'
        ) {
          console.log('Theme change detected in WinsPage.');
          this.toggleChartTheme();
        }
      });
    });
    this.themeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['class'],
    });
  }

  ngAfterViewInit(): void {
    // Immediately update charts with current theme.
    this.toggleChartTheme();

    // Use multiple delays to re-check the theme in case the dark-mode class is applied late.
    setTimeout(() => {
      this.toggleChartTheme();
    }, 500);

    setTimeout(() => {
      this.toggleChartTheme();
    }, 1000);
  }

  ngOnDestroy(): void {
    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
  }

  /**
   * Updates chart options to reflect the active theme.
   * When dark mode is active (body has "dark-mode"), sets foreColor to white (#fff) and uses ApexCharts' theme.
   */
  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';

    // Update Category Distribution Chart (chartOptionsOne)
    if (this.categoryChartRef) {
      this.categoryChartRef.updateOptions(
        {
          chart: {
            foreColor: foreColor,
            theme: { mode: isDark ? 'dark' : 'light' }, // use ApexCharts' theme feature
          },
          xaxis: { labels: { style: { colors: [foreColor] } } },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }

    // Update Evolution Chart (chartOptionsTwo)
    if (this.evolutionChartRef) {
      this.evolutionChartRef.updateOptions(
        {
          chart: {
            foreColor: foreColor,
            theme: { mode: isDark ? 'dark' : 'light' }, // use ApexCharts' theme feature
          },
          xaxis: { labels: { style: { colors: [foreColor] } } },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
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
        const formattedData = res.wins.map((w: any) => ({
          opportunity_id: w.win_id,
          client_name: w.client_name,
          client_industry: w.client_industry,
          win_level: w.win_level,
          win_category: w.win_category.toUpperCase(),
          win_date: `${w.fiscal_year} Q${w.fiscal_quarter}`,
          fiscal_year: w.fiscal_year,
          fiscal_quarter: w.fiscal_quarter
        }));
  
        this.winsUnfiltered = formattedData;
        this.wins = [...formattedData];
  
        this.uniqueIndustries = [...new Set<string>(
          formattedData.map((row: any) => row.client_industry)
        )];
  
        this.uniqueCategories = [...new Set<string>(
          formattedData.map((row: any) => row.win_category)
        )];
  
  
        this.markLoaded();
      },
      error: (err) => {
        console.error('Wins fetch error:', err);
        this.markLoaded();
      },
    });
  }

  toggleFilter(category: keyof typeof this.selectedFilters, value: string, event: Event): void {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
      this.selectedFilters[category].add(value);
    } else {
      this.selectedFilters[category].delete(value);
    }
  }

  applyFilters(): void {
    this.wins = this.winsUnfiltered.filter(row =>
    (!this.selectedFilters.win_category.size || this.selectedFilters.win_category.has(row.win_category)) &&
    (!this.selectedFilters.client_industry.size || this.selectedFilters.client_industry.has(row.client_industry)) &&
    (!this.searchTerm || row.client_name.toLowerCase().includes(this.searchTerm.toLowerCase()))
    );
    this.showFilterOverlay = false;
  }

  clearFilters(): void {
    this.selectedFilters.win_category.clear();
    this.selectedFilters.client_industry.clear();
    this.searchTerm = '';
    this.wins = [...this.winsUnfiltered];
    this.showFilterOverlay = false;
  }

  onOverlayClick(event: MouseEvent): void {
    this.showFilterOverlay = false;
  }

  loadQuarterlyCards(): void {
    this.winsService
      .getWinsQuarterlyTargets(this.username, this.year)
      .subscribe({
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
    // Check the active theme when initializing the chart.
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';

    this.winsService
      .getWinsCategoryDistribution(this.username, this.year)
      .subscribe({
        next: (res) => {
          this.chartOptionsOne = {
            chart: {
              type: 'line',
              height: 350,
              stacked: true,
              toolbar: { show: false },
              foreColor: foreColor,
              theme: { mode: isDark ? 'dark' : 'light' },
            },
            series: res.series,
            colors: [
              '#4285F4',
              '#34A853',
              '#FBBC05',
              '#EA4335',
              '#A142F4',
              '#00ACC1',
            ],
            xaxis: {
              title: {
                text: 'Quarter',
              },
              categories: res.quarters,
              labels: { style: { colors: [foreColor] } },
            },
            stroke: {
              curve: 'smooth',
              width: 2,
            },
            tooltip: {
              shared: true,
              intersect: false,
              theme: isDark ? 'dark' : 'light',
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
    // Check the active theme when initializing the chart.
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';

    this.winsService.getWinsOverTime(this.username, this.year).subscribe({
      next: (res) => {
        this.chartOptionsTwo = {
          chart: {
            type: 'line',
            height: 350,
            toolbar: { show: false },
            foreColor: foreColor,
            theme: { mode: isDark ? 'dark' : 'light' },
          },
          colors: ['#4285F4'],
          series: [
            {
              name: 'Total Wins',
              data: res.win_evolution.map((e: any) => e.win_count),
            },
          ],
          xaxis: {
            categories: res.categories,
            title: { text: 'Quarter' },
            labels: { style: { colors: [foreColor] } },
          },
          stroke: {
            curve: 'smooth',
          },
          tooltip: {
            shared: true,
            intersect: false,
            theme: isDark ? 'dark' : 'light',
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
