import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import {
  NgApexchartsModule,
  ApexResponsive,
  ChartComponent,
} from 'ng-apexcharts';
import { CommonModule } from '@angular/common';

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
  selector: 'app-landing-page',
  standalone: true,
  imports: [
    HeaderComponent,
    SidebarComponent,
    CommonModule,
    NgApexchartsModule,
  ],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.css',
})
export class LandingPageComponent implements OnInit, AfterViewInit {
  @ViewChild('chartOneRef') chartOne!: ChartComponent;
  @ViewChild('chartTwoRef') chartTwo!: ChartComponent;
  @ViewChild('chartThreeRef') chartThree!: ChartComponent;
  @ViewChild('chartFourRef') chartFour!: ChartComponent;

  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  accountExecutives: any[] = [];
  isLoadingAccountExecutives: boolean = true;
  isLoadingChartData: boolean = true;

  chartOptionsOne!: Partial<ChartOptions>;
  chartOptionsTwo!: Partial<ChartOptions>;
  chartOptionsThree!: Partial<ChartOptions>;
  chartOptionsFour!: Partial<ChartOptions>;

  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.chartOptionsOne = this.getBaseChartOptions('Pipeline', '#1E88E5');
    this.chartOptionsTwo = this.getBaseChartOptions('Revenue', '#F4511E');
    this.chartOptionsThree = this.getBaseChartOptions('Signings', '#43A047');
    this.chartOptionsFour = this.getBaseChartOptions(
      'Count To Wins',
      '#FDD835'
    );

    this.fetchCardData();
    this.fetchAccountExecutives();
    this.fetchChartData();
  }

  ngAfterViewInit(): void {
    const observer = new MutationObserver(() => {
      this.toggleChartThemes();
    });

    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['class'],
    });
  }

  toggleChartThemes(): void {
    const isDark = document.body.classList.contains('dark-mode');

    const newTheme = {
      theme: {
        mode: isDark ? 'dark' : 'light',
      },
    };

    this.chartOne?.updateOptions(newTheme, false, true);
    this.chartTwo?.updateOptions(newTheme, false, true);
    this.chartThree?.updateOptions(newTheme, false, true);
    this.chartFour?.updateOptions(newTheme, false, true);
  }

  getBaseChartOptions(title: string, color: string): Partial<ChartOptions> {
    return {
      series: [{ name: title, data: [] }],
      chart: {
        type: 'bar',
        height: 350,
        background: 'transparent',
        foreColor: 'var(--text-color)',
      },
      theme: {
        mode: 'light',
      },
      colors: [color],
      fill: {
        opacity: 1,
        colors: [color],
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          borderRadius: 8,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent'],
      },
      xaxis: {
        title: {
          text: title,
          style: {
            color: 'var(--text-color)',
            fontFamily: 'Arial, sans-serif',
          },
        },
        labels: {
          style: {
            colors: 'var(--text-color)',
            fontFamily: 'Arial, sans-serif',
          },
        },
        categories: [
          'J',
          'F',
          'M',
          'A',
          'M',
          'J',
          'J',
          'A',
          'S',
          'O',
          'N',
          'D',
        ],
      },
      yaxis: {
        title: {
          text: 'Amount ($)',
          style: {
            color: 'var(--text-color)',
            fontFamily: 'Arial, sans-serif',
          },
        },
        labels: {
          style: {
            colors: 'var(--text-color)',
            fontFamily: 'Arial, sans-serif',
          },
        },
      },
      legend: {
        labels: {
          colors: 'var(--text-color)',
        },
      },
      tooltip: {
        theme: 'dark',
        y: {
          formatter: (val: number) => '$ ' + val,
        },
      },
      responsive: [
        {
          breakpoint: 768,
          options: {
            chart: { width: '100%' },
          },
        },
      ],
    };
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

  fetchAccountExecutives(): void {
    this.dashboardService.getAccountExecutives().subscribe(
      (response) => {
        this.accountExecutives = response;
        this.isLoadingAccountExecutives = false;
      },
      (error) => {
        console.error('Error fetching account executives:', error);
        this.isLoadingAccountExecutives = false;
      }
    );
  }

  fetchChartData(): void {
    this.dashboardService.getChartData().subscribe(
      (response) => {
        this.chartOptionsOne.series = [
          { name: 'Pipeline', data: response.pipeline },
        ];
        this.chartOptionsTwo.series = [
          { name: 'Revenue', data: response.revenue },
        ];
        this.chartOptionsThree.series = [
          { name: 'Signings', data: response.signings },
        ];
        this.chartOptionsFour.series = [{ name: 'Wins', data: response.wins }];
        this.isLoadingChartData = false;
      },
      (error) => {
        console.error('Error fetching chart data:', error);
        this.isLoadingChartData = false;
      }
    );
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
