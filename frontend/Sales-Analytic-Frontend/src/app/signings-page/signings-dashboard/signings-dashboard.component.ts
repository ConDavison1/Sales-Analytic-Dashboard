import {
  Component,
  OnInit,
  ViewChild,
  AfterViewInit,
  OnDestroy,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent, NgApexchartsModule } from 'ng-apexcharts';
import {
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexYAxis,
  ApexDataLabels,
  ApexPlotOptions,
  ApexTooltip,
  ApexFill,
  ApexNonAxisChartSeries,
  ApexResponsive,
  ApexChart as ApexNonAxisChart,
} from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { SigningsService } from '../../services/signings-page/signings.service';
import { FormsModule } from '@angular/forms';

export type BarChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  yaxis: ApexYAxis;
  dataLabels: ApexDataLabels;
  plotOptions: ApexPlotOptions;
  tooltip: ApexTooltip;
  colors: string[];
};

export type PolarChartOptions = {
  series: ApexNonAxisChartSeries;
  chart: ApexNonAxisChart;
  labels: string[];
  colors: string[];
  responsive: ApexResponsive[];
};

@Component({
  selector: 'app-signings-dashboard',
  standalone: true,
  templateUrl: './signings-dashboard.component.html',
  styleUrls: ['./signings-dashboard.component.css'],
  imports: [
    CommonModule,
    NgApexchartsModule,
    HeaderComponent,
    SidebarComponent,
    FormsModule,
  ],
})
export class SigningsDashboardComponent
  implements OnInit, AfterViewInit, OnDestroy
{
  @ViewChild('barChartRef') barChartRef!: ChartComponent;
  @ViewChild('polarChartRef') polarChartRef!: ChartComponent;

  username = localStorage.getItem('username') || '';
  year = 2024;

  signingsData: any[] = [];
  signingsDataUnfiltered: any[] = [];
  quarterlyCards: any[] = [];

  showFilterOverlay: boolean = false;
  searchTerm: string = '';

  selectedFilters: {
    product_category: Set<string>;
    fiscal_quarter: Set<string>;
  } = {
    product_category: new Set<string>(),
    fiscal_quarter: new Set<string>(),
  };

  uniqueProductCategories: string[] = [];
  uniqueQuarters: string[] = [];

  showFilterOverlay: boolean = false;
  searchTerm: string = '';

  selectedFilters: {
    product_category: Set<string>;
    fiscal_quarter: Set<string>;
  } = {
    product_category: new Set<string>(),
    fiscal_quarter: new Set<string>(),
  };

  uniqueProductCategories: string[] = [];
  uniqueQuarters: string[] = [];

  // Initial bar chart options. We'll update the foreColor based on dark mode.
  barChart: BarChartOptions = {
    series: [{ name: 'iACV', data: [] }],
    chart: {
      type: 'bar',
      height: 350,
      background: 'transparent',
      foreColor: '#000', // default; will be updated below
    },
    xaxis: {
      categories: [],
      title: { text: 'Industry' },
    },
    yaxis: {
      title: { text: 'Incremental iACV ($)' },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: { columnWidth: '60%', distributed: false },
    },
    tooltip: {
      enabled: true,
      y: { formatter: (val: number) => `$${val.toLocaleString()}` },
    },
    colors: ['#008FFB'],
  };

  // Initial polar chart options.
  polarChart: PolarChartOptions = {
    series: [],
    chart: {
      type: 'polarArea',
      height: 300,
      foreColor: '#000', // default; will be updated below
    },
    labels: [],
    colors: [
      '#1E90FF',
      '#FF8C00',
      '#32CD32',
      '#FF69B4',
      '#8A2BE2',
      '#00CED1',
      '#FFD700',
      '#FF6347',
      '#40E0D0',
      '#DA70D6',
    ],
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: { height: 300 },
          legend: { position: 'bottom' },
        },
      },
    ],
  };

  // MutationObserver to track theme changes.
  private themeObserver!: MutationObserver;

  constructor(private signingsService: SigningsService) {}

  ngOnInit(): void {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    this.username = user.username || '';

    if (!this.username) {
      console.warn('[SigningsDashboard] No username found in localStorage.');
      return;
    }

    console.log('[SigningsDashboard] Username:', this.username);
    this.loadSignings();
    this.loadIndustryChart();
    this.loadProvincialDistributionChart();
    this.loadQuarterlyTargets();

    // Set up MutationObserver to detect dark mode changes.
    this.themeObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (
          mutation.type === 'attributes' &&
          mutation.attributeName === 'class'
        ) {
          console.log('[SigningsDashboard] Theme change detected.');
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
    // Delay updating theme to allow "dark-mode" class to be applied.
    setTimeout(() => {
      this.toggleChartTheme();
    }, 500);
  }

  ngOnDestroy(): void {
    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
  }

  /**
   * toggleChartTheme updates the chart text colors (foreColor) and tooltip theme based on dark mode.
   * If dark mode is active (document.body has 'dark-mode'), chart text turns white (#fff); otherwise, black (#000).
   */
  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';
    console.log(
      `[SigningsDashboard] toggleChartTheme: isDark=${isDark}, foreColor=${foreColor}`
    );

    if (this.barChartRef) {
      this.barChartRef.updateOptions(
        {
          chart: { foreColor: foreColor },
          xaxis: { labels: { style: { colors: [foreColor] } } },
          yaxis: {
            labels: { style: { colors: [foreColor] } },
            // Include the title text and style here so it isn't removed
            title: { text: 'Incremental ACV ($)', style: { color: foreColor } },
          },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }

    if (this.polarChartRef) {
      this.polarChartRef.updateOptions(
        {
          chart: { foreColor: foreColor },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }
  }

  loadSignings(): void {
    this.signingsService.getSignings(this.username, this.year).subscribe({
      next: (res) => {
        const formattedData = res.signings.map((s: any) => ({
          client_name: s.client_name,
          product_name: s.product_name,
          product_category: s.product_category,
          total_contract_value: s.total_contract_value,
          incremental_acv: s.incremental_acv,
          start_date: s.start_date,
          end_date: s.end_date,
          signing_date: s.signing_date,
          fiscal_year: s.fiscal_year,
          fiscal_quarter: s.fiscal_quarter,
        }));
        this.signingsDataUnfiltered = formattedData;
        this.signingsData = [...formattedData];

        this.uniqueProductCategories = [
          ...new Set<string>(
            formattedData.map((row: any) => row.product_category as string)
          ),
        ];
        this.uniqueQuarters = [
          ...new Set<string>(
            formattedData.map((row: any) => row.fiscal_quarter as string)
          ),
        ];
      },
      error: (err) => console.error('Signings error:', err),
    });
  }

  toggleFilter(
    category: keyof typeof this.selectedFilters,
    value: string,
    event: Event
  ): void {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
      this.selectedFilters[category].add(value);
    } else {
      this.selectedFilters[category].delete(value);
    }
  }

  applyFilters(): void {
    this.signingsData = this.signingsDataUnfiltered.filter(
      (row) =>
        (!this.selectedFilters.product_category.size ||
          this.selectedFilters.product_category.has(row.product_category)) &&
        (!this.selectedFilters.fiscal_quarter.size ||
          this.selectedFilters.fiscal_quarter.has(row.fiscal_quarter)) &&
        (!this.searchTerm ||
          row.client_name.toLowerCase().includes(this.searchTerm.toLowerCase()))
    );
    this.showFilterOverlay = false;
  }

  clearFilters(): void {
    this.selectedFilters.product_category.clear();
    this.selectedFilters.fiscal_quarter.clear();
    this.searchTerm = '';
    this.signingsData = [...this.signingsDataUnfiltered];
    this.showFilterOverlay = false;
  }

  onOverlayClick(event: MouseEvent): void {
    this.showFilterOverlay = false;
  }

  loadIndustryChart(): void {
    this.signingsService.getIndustryACV(this.username, this.year).subscribe({
      next: (res) => {
        const chartData = res.industry_acv_data;
        const industries = chartData.map((item: any) => item.industry);
        const values = chartData.map((item: any) => item.incremental_acv);

        // Check current theme for initial foreColor.
        const isDark = document.body.classList.contains('dark-mode');
        const foreColor = isDark ? '#fff' : '#000';

        // Update barChart options.
        this.barChart.series = [{ name: 'iACV', data: values }];
        this.barChart = {
          ...this.barChart,
          series: [{ name: 'iACV', data: values }],
          xaxis: {
            ...this.barChart.xaxis,
            categories: industries,
            title: { text: 'Industry' },
          },
          chart: { ...this.barChart.chart, foreColor: foreColor },
        };
      },
      error: (err) => console.error('Industry ACV error:', err),
    });
  }

  loadProvincialDistributionChart(): void {
    this.signingsService
      .getProvincialDistribution(this.username, this.year)
      .subscribe({
        next: (res) => {
          const data = res.provincial_data;
          // Check current theme for initial foreColor.
          const isDark = document.body.classList.contains('dark-mode');
          const foreColor = isDark ? '#fff' : '#000';

          this.polarChart.series = data.map((item: any) => item.count);
          this.polarChart.labels = data.map(
            (item: any) =>
              `${item.province} - $${item.avg_value.toLocaleString()}`
          );
          // Update polar chart foreColor.
          this.polarChart = {
            ...this.polarChart,
            chart: { ...this.polarChart.chart, foreColor: foreColor },
          };
        },
        error: (err) => console.error('Provincial Distribution error:', err),
      });
  }

  loadQuarterlyTargets(): void {
    this.signingsService
      .getQuarterlyTargets(this.username, this.year)
      .subscribe({
        next: (res) => {
          this.quarterlyCards = res.quarterly_targets.map((q: any) => ({
            title: `Q${q.quarter} Target`,
            value: `$${q.accumulated_value.toLocaleString()}`,
            percentage: `${q.achievement_percentage.toFixed(1)}% Achieved`,
          }));
        },
        error: (err) => console.error('Quarterly targets error:', err),
      });
  }
}
