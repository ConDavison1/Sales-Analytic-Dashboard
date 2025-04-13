import {
  Component,
  OnInit,
  AfterViewInit,
  ViewChild,
  OnDestroy,
  ViewEncapsulation,
  AfterViewChecked,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { NgApexchartsModule, ChartComponent } from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { RevenueService } from '../../services/revenue-services/revenue.service';

@Component({
  selector: 'app-revenue-page',
  imports: [
    NgApexchartsModule,
    CommonModule,
    SidebarComponent,
    HeaderComponent,
  ],
  standalone: true,
  templateUrl: './revenue-page.component.html',
  styleUrls: ['./revenue-page.component.css'],
  encapsulation: ViewEncapsulation.Emulated,
})
export class RevenuePageComponent
  implements OnInit, AfterViewInit, AfterViewChecked, OnDestroy
{
  @ViewChild('barChartRef') barChartRef!: ChartComponent;
  @ViewChild('areaChartRef') areaChartRef!: ChartComponent;

  revenueData: any[] = [];
  revenueChartData: any[] = [];
  cards: any[] = [];
  isDataLoaded: boolean = false;

  private username: string = '';
  private loadCount = 0;
  private totalLoadsNeeded = 4;

  // MutationObserver to monitor dark-mode changes.
  private themeObserver!: MutationObserver;

  constructor(private revenueService: RevenueService) {}

  ngOnInit(): void {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    this.username = user.username;
    if (!this.username) return;

    this.fetchRevenueClients();
    this.fetchRevenueChart();
    this.fetchQuarterlyTargets();
    this.fetchIndustryRevenueAreaChart();

    // Set up MutationObserver to detect dark mode changes.
    this.themeObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (
          mutation.type === 'attributes' &&
          mutation.attributeName === 'class'
        ) {
          console.log('[RevenuePageComponent] Theme change detected.');
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
    // Delay updating theme so that the "dark-mode" class (if any) is applied.
    setTimeout(() => {
      this.toggleChartTheme();
    }, 500);
  }

  ngAfterViewChecked(): void {
    this.toggleChartTheme();
  }

  ngOnDestroy(): void {
    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
  }

  /**
   * toggleChartTheme updates the charts' styling.
   * Here, the tooltip is forced to always use the "dark" theme so that
   * tooltips are rendered consistently with dark styling, regardless of the page's mode.
   */
  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';
    console.log(
      `[RevenuePageComponent] toggleChartTheme: isDark=${isDark}, foreColor=${foreColor}`
    );

    if (this.barChartRef) {
      this.barChartRef.updateOptions(
        {
          theme: { mode: isDark ? 'dark' : 'light' },
          chart: { foreColor: foreColor },
          grid: {
            borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
          },
          xaxis: { labels: { style: { colors: [foreColor] } } },
          yaxis: {
            labels: { style: { colors: [foreColor] } },
            title: { text: 'Revenue ($)', style: { color: foreColor } },
          },
          // **Force tooltip to ALWAYS use dark theme** (so tooltips have a dark background with white text)
          tooltip: { theme: 'dark' },
        },
        false,
        true
      );
    }

    if (this.areaChartRef) {
      this.areaChartRef.updateOptions(
        {
          theme: { mode: 'dark' },
          chart: { foreColor: foreColor },
          xaxis: { labels: { style: { colors: [foreColor] } } },
          // **Force tooltip to ALWAYS use dark theme**
          tooltip: { theme: 'dark' },
        },
        false,
        true
      );
    }
  }

  private markLoaded(): void {
    this.loadCount++;
    if (this.loadCount >= this.totalLoadsNeeded) {
      this.isDataLoaded = true;
    }
  }

  fetchRevenueClients(): void {
    this.revenueService.getRevenue(this.username).subscribe({
      next: (res) => {
        this.revenueData = res.revenue;
        this.markLoaded();
      },
      error: (err) => {
        console.error('Revenue fetch error:', err);
        this.markLoaded();
      },
    });
  }

  fetchRevenueChart(): void {
    this.revenueService.getRevenueProductDistribution(this.username).subscribe({
      next: (res) => {
        this.revenueChartData = res.bubble_data.map((item: any) => ({
          category: item.product_category,
          data: item.data,
        }));

        const categories = ['Q1', 'Q2', 'Q3', 'Q4'];
        const series = this.revenueChartData.map((item) => ({
          name: item.category,
          data: item.data.map((entry: number[]) => entry[1]),
        }));

        this.barChart.series = series;
        this.barChart.xaxis.categories = categories;
        this.markLoaded();
      },
      error: (err) => {
        console.error('Revenue chart error:', err);
        this.markLoaded();
      },
    });
  }

  fetchQuarterlyTargets(): void {
    this.revenueService.getRevenueQuarterlyTargets(this.username).subscribe({
      next: (res) => {
        const quarters = res.quarterly_targets;
        this.cards = quarters.map((q: any) => ({
          title: `Q${q.quarter} Target`,
          value: `$${q.accumulated_value.toLocaleString()}`,
          percentage: `${q.achievement_percentage.toFixed(1)}% Achieved`,
        }));
        this.markLoaded();
      },
      error: (err) => {
        console.error('Quarterly targets error:', err);
        this.markLoaded();
      },
    });
  }

  fetchIndustryRevenueAreaChart(): void {
    this.revenueService.getIndustryRevenueAreaChart(this.username).subscribe({
      next: (res) => {
        this.areaChart.series = res.industry_data.map((item: any) => ({
          name: item.industry,
          data: item.data,
        }));
        this.areaChart.xaxis.categories = res.quarters.map(
          (q: number) => `Q${q}`
        );
        this.markLoaded();
      },
      error: (err) => {
        console.error('Industry Revenue area chart error:', err);
        this.markLoaded();
      },
    });
  }

  barChart = {
    chart: {
      type: 'bar' as const,
      height: 350,
      background: 'transparent',
      foreColor: 'var(--text-color)',
    },
    series: [] as { name: string; data: number[] }[],
    xaxis: {
      title: { text: 'Quarters' },
      categories: [] as string[],
    },
    plotOptions: {
      bar: { horizontal: false, columnWidth: '50%', distributed: true },
    },
    dataLabels: { enabled: false },
    colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560'],
    tooltip: {
      enabled: true,
      theme: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
      y: { formatter: (val: number) => `${val} Clients` },
    },
    theme: {
      mode: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
  };

  areaChart = {
    series: [] as any[],
    chart: {
      toolbar: { show: false },
      type: 'area' as const,
      height: 350,
      background: 'transparent',
      foreColor: 'var(--text-color)',
    },
    dataLabels: { enabled: false },
    stroke: { curve: 'smooth' as const },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.4,
        opacityTo: 0.1,
      },
    },
    xaxis: {
      categories: [] as string[],
      title: { text: 'Quarters' },
    },
    colors: ['#4285F4', '#DB4437', '#F4B400', '#0F9D58'],
    tooltip: {
      theme: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
    theme: {
      mode: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
  };
}
