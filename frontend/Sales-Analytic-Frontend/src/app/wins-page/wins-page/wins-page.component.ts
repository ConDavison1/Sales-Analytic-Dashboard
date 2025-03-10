import { Component, OnInit, ViewChild } from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { WinsService } from '../../services/wins-services/wins.service';
import { NgApexchartsModule, ApexAxisChartSeries } from 'ng-apexcharts';

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: any;
  xaxis: any;
  stroke: any;
  dataLabels: any;
  markers: any;
  plotOptions: any;
  yaxis: any;
  fill: any;
  tooltip: any;
  legend: any;
  grid: any;
  title: any;
};

@Component({
  selector: 'app-wins-page',
  standalone: true,
  imports: [
    HeaderComponent,
    SidebarComponent,
    CommonModule,
    NgApexchartsModule,
  ],
  templateUrl: './wins-page.component.html',
  styleUrl: './wins-page.component.css',
})
export class WinsPageComponent implements OnInit {
  wins: any[] = [];
  isLoadingWins: boolean = true;
  winsChartData: any;
  isWinsDataLoaded: boolean = false;

  chartOptionsOne: Partial<ChartOptions> = {
    series: [
      { name: 'Wins', data: [] },
      { name: 'Opportunities', data: [] },
    ],
  };

  chartOptionsTwo: Partial<ChartOptions> = {
    series: [],
  };

  sortColumn: string = '';
  sortDirection: 'asc' | 'desc' = 'asc';

  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  constructor(
    private winsService: WinsService,
    private dashboardService: DashboardService
  ) {
    this.chartOptionsOne = {
      series: [
        { name: 'Wins', data: [] },
        { name: 'Opportunities', data: [] },
      ],
      chart: {
        type: 'bar',
        height: 350,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          endingShape: 'rounded',
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
          text: 'Industry',
        },
        categories: [],
      },
      yaxis: {
        title: {
          text: 'Count of Wins & Opportunities',
        },
      },
      fill: {
        opacity: 1,
        colors: ['#1E88E5', '#43A047'], // Add colors for your bars
      },
      tooltip: {
        y: {
          formatter: function (val: number) {
            return val + ' Count';
          },
        },
      },
      legend: {
        show: true,
      },
    };

    this.chartOptionsTwo = {
      series: [
        {
          name: 'Confirmed Wins',
          data: [22, 12, 21, 9, 15, 3, 8, 16, 9, 18, 15, 20],
        },
        {
          name: 'Potential Wins',
          data: [9, 6, 12, 3, 21, 5, 13, 3, 18, 3, 12, 8],
        },
      ],
      chart: {
        height: 350,
        type: 'line',
        zoom: {
          enabled: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        width: 5,
        curve: 'straight',
        dashArray: [0, 8, 5],
      },
      title: {
        text: 'Wins Over Time',
        align: 'left',
      },
      legend: {
        tooltipHoverFormatter: function (
          val: string,
          opts: {
            w: {
              globals: { series: { [x: string]: { [x: string]: string } } };
            };
            seriesIndex: string | number;
            dataPointIndex: string | number;
          }
        ) {
          return (
            val +
            ' - <strong>' +
            opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] +
            '</strong>'
          );
        },
      },
      markers: {
        size: 0,
        hover: {
          sizeOffset: 6,
        },
      },
      xaxis: {
        title: {
          text: 'Month',
        },
        labels: {
          trim: false,
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
      tooltip: {
        y: [
          {
            title: {
              formatter: function (val: string) {
                return val;
              },
            },
          },
          {
            title: {
              formatter: function (val: string) {
                return val;
              },
            },
          },
          {
            title: {
              formatter: function (val: any) {
                return val;
              },
            },
          },
        ],
      },
      grid: {
        borderColor: '#f1f1f1',
      },
    };
  }

  ngOnInit(): void {
    this.fetchCardData();
    this.fetchWins();
    this.fetchBarChart();
  }

  fetchBarChart(): void {
    this.winsService.getWinsBarChart().subscribe(
      (response) => {
        console.log('Chart data received:', response);
        this.chartOptionsOne.series = [
          {
            name: 'Wins',
            data: response.map((item: any) => item.wins),
          },
          {
            name: 'Opportunities',
            data: response.map((item: any) => item.opportunities),
          },
        ];
        this.chartOptionsOne.xaxis.categories = response.map(
          (item: any) => item.industry
        );
        this.isWinsDataLoaded = true;
      },
      (error) => {
        console.error('Error loading chart data:', error);
        this.isWinsDataLoaded = false;
      }
    );
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
