import {
  Component,
  OnInit,
  AfterViewInit,
  ViewChild,
  OnDestroy,
} from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { Title } from '@angular/platform-browser';
import {
  NgApexchartsModule,
  ApexResponsive,
  ChartComponent,
} from 'ng-apexcharts';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

export type ChartOptions = {
  series: any[];
  chart: any;
  plotOptions: any;
  dataLabels: any;
  stroke: any;
  xaxis: any;
  yaxis: any;
  fill: any;
  tooltip: any;
  legend: any;
  colors: any;
  responsive: ApexResponsive[];
  theme: any;
};

@Component({
  standalone: true,
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css'],
  imports: [
    CommonModule,
    NgApexchartsModule,
    HeaderComponent,
    SidebarComponent,
  ],
})
export class LandingPageComponent implements OnInit, AfterViewInit, OnDestroy {
  username: string = '';
  year: number = 2024;
  isLoadingChartData = true;

  cards: any[] = [];
  chartOptionsOne: any = {};
  chartOptionsTwo: any = {};
  chartOptionsThree: any = {};
  chartOptionsFour: any = {};

  // ViewChild references—ensure your HTML template uses these template reference names!
  @ViewChild('revenueChartRef') revenueChartRef!: ChartComponent;
  @ViewChild('winChartRef') winChartRef!: ChartComponent;
  @ViewChild('pipelineChartRef') pipelineChartRef!: ChartComponent;
  @ViewChild('signingsChartRef') signingsChartRef!: ChartComponent;

  // MutationObserver to monitor theme (body class) changes.
  private themeObserver!: MutationObserver;

  constructor(
    private dashboardService: DashboardService,
    private route: ActivatedRoute,
    private router: Router,
    private titleService: Title
  ) {}

  ngOnInit(): void {
    this.titleService.setTitle('Dashboard | Sales Analytics');
    const userData = localStorage.getItem('user');
    if (userData) {
      const user = JSON.parse(userData);
      this.username = user.username;
      console.log('Logged in as:', this.username);

      this.loadKpiCards();
      this.loadRevenueChart();
      this.loadWinChart();
      this.loadPipelineChart();
      this.loadSigningsChart();
    } else {
      console.error('No user found in localStorage. Redirecting to login.');
      this.router.navigate(['/login']);
    }

    // Set up a MutationObserver to watch for changes in the body's class list.
    this.themeObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (
          mutation.type === 'attributes' &&
          mutation.attributeName === 'class'
        ) {
          console.log('Theme change detected.');
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
    // Update chart text colors after view initialization.
    this.toggleChartTheme();
  }

  ngOnDestroy(): void {
    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
  }

  /**
   * Updates the text color (foreColor) and tooltip theme on each chart based on the current mode.
   */
  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';
    console.log(
      `toggleChartTheme called. isDark=${isDark}, foreColor=${foreColor}`
    );

    // Update Revenue (bar) chart.
    if (this.revenueChartRef) {
      this.revenueChartRef.updateOptions(
        {
          chart: { foreColor: foreColor },
          xaxis: { labels: { style: { colors: [foreColor] } } },
          yaxis: { labels: { style: { colors: [foreColor] } } },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }

    // Update Win (bar) chart.
    if (this.winChartRef) {
      this.winChartRef.updateOptions(
        {
          chart: { foreColor: foreColor },
          xaxis: { labels: { style: { colors: [foreColor] } } },
          yaxis: { labels: { style: { colors: [foreColor] } } },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }

    // Update Pipeline (pie) chart.
    if (this.pipelineChartRef) {
      this.pipelineChartRef.updateOptions(
        {
          chart: { foreColor: foreColor },
          legend: { labels: { colors: [foreColor] } },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }

    // Update Signings (pie) chart.
    if (this.signingsChartRef) {
      this.signingsChartRef.updateOptions(
        {
          chart: { foreColor: foreColor },
          legend: { labels: { colors: [foreColor] } },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }
  }

  loadKpiCards(): void {
    this.dashboardService
      .getKpiCards(this.username, this.year)
      .subscribe((data) => {
        this.cards = [
          { title: 'Pipeline', value: `$${Number(data.pipeline).toLocaleString()}`, percentage: '' },
          { title: 'Revenue', value: `$${Number(data.revenue).toLocaleString()}`, percentage: '' },
          { title: 'Signings', value: `$${Math.round(data.signings).toLocaleString()}`, percentage: '' },
          { title: 'Wins', value: `${Number(data.wins).toLocaleString()}`, percentage: '' },
        ];
      });
  }
  
  

  loadRevenueChart(): void {
    this.dashboardService
      .getRevenueChartData(this.username, this.year)
      .subscribe((data) => {
        const isDark = document.body.classList.contains('dark-mode');
        const foreColor = isDark ? '#fff' : '#000';
        this.chartOptionsOne = {
          series: [
            {
              name: 'Revenue',
              data: data.revenue_chart_data.map((d: any) => d.revenue),
            },
          ],
          chart: { type: 'bar', height: 350, foreColor: foreColor },
          xaxis: {
            title: { text: 'Month' },
            categories: data.revenue_chart_data.map((d: any) => `${d.month}`),
            labels: { style: { colors: [foreColor] } },
          },
          yaxis: {
            title: { text: 'Revenue ($)' },
            labels: { style: { colors: [foreColor] } },
          },
          plotOptions: { bar: { horizontal: false, columnWidth: '55%' } },
          dataLabels: { enabled: false },
          fill: { opacity: 1 },
          tooltip: {
            y: {
              formatter: function (val: any) {
                return `$${val}`;
              },
            },
            theme: isDark ? 'dark' : 'light',
          },
          theme: { mode: isDark ? 'dark' : 'light' },
        };
        this.isLoadingChartData = false;
      });
  }

  loadWinChart(): void {
    this.dashboardService
      .getWinChartData(this.username, this.year)
      .subscribe((data) => {
        const isDark = document.body.classList.contains('dark-mode');
        const foreColor = isDark ? '#fff' : '#000';
        this.chartOptionsTwo = {
          series: [
            {
              name: 'Wins',
              data: data.win_chart_data.map((d: any) => d.win_count),
            },
          ],
          chart: { type: 'bar', height: 350, foreColor: foreColor },
          xaxis: {
            title: { text: 'Quarter' },
            categories: data.win_chart_data.map((d: any) => `Q${d.quarter}`),
            labels: { style: { colors: [foreColor] } },
          },
          yaxis: {
            title: { text: 'Wins' },
            labels: { style: { colors: [foreColor] } },
          },
          plotOptions: { bar: { horizontal: false, columnWidth: '55%' } },
          dataLabels: { enabled: true },
          fill: { opacity: 1 },
          tooltip: {
            y: {
              formatter: function (val: any) {
                return val;
              },
            },
            theme: isDark ? 'dark' : 'light',
          },
          theme: { mode: isDark ? 'dark' : 'light' },
        };
      });
  }

  loadPipelineChart(): void {
    this.dashboardService
      .getPipelineChartData(this.username, this.year)
      .subscribe((data) => {
        const isDark = document.body.classList.contains('dark-mode');
        const foreColor = isDark ? '#fff' : '#000';
        this.chartOptionsThree = {
          series: data.pipeline_chart_data.map((d: any) => d.count),
          chart: { type: 'pie', height: 300, foreColor: foreColor },
          labels: data.pipeline_chart_data.map((d: any) => d.forecast_category),
          theme: { mode: isDark ? 'dark' : 'light' },
          legend: { position: 'bottom', labels: { colors: [foreColor] } },
          // In this version, we keep the formatter unchanged (displaying the label) so that only text color is affected.
          dataLabels: { enabled: true, style: { colors: ['#fff'] } },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        };
      });
  }

  loadSigningsChart(): void {
    this.dashboardService
      .getSigningsChartData(this.username, this.year)
      .subscribe((data) => {
        const isDark = document.body.classList.contains('dark-mode');
        const foreColor = isDark ? '#fff' : '#000';
        this.chartOptionsFour = {
          series: data.signings_chart_data.map((d: any) => d.count),
          chart: { type: 'pie', height: 300, foreColor: foreColor },
          labels: data.signings_chart_data.map((d: any) => d.product_category),
          theme: { mode: isDark ? 'dark' : 'light' },
          legend: { position: 'bottom', labels: { colors: [foreColor] } },
          dataLabels: { enabled: true, style: { colors: ['#fff'] } },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        };
      });
  }
}
