import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { AccountExecService } from '../../services/account-exec-services/account-exec.service';
import { first } from 'rxjs';
import { NgApexchartsModule } from 'ng-apexcharts';
import { ApexChart } from 'ng-apexcharts';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';

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
};
interface ChartData {
  category: string;
  count: number;
}
@Component({
  selector: 'app-account-exec-dashboard',
  imports: [CommonModule, NgApexchartsModule, ReactiveFormsModule],
  standalone: true,
  templateUrl: './account-exec-dashboard.component.html',
  styleUrl: './account-exec-dashboard.component.css',
  encapsulation: ViewEncapsulation.Emulated
})
export class AccountExecDashboardComponent {

  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;
  addExecutiveForm: FormGroup;

  accountExecData: any[] = [];
  selectedExecutive: any = null;
  topExecutivesChartData: ChartData[] = [];

  isDataLoaded: boolean = false;

  accountExecutives: any[] = [];
  isLoadingAccountExecutives: boolean = true;
  

  constructor(
    private dashboardService: DashboardService,
    private accountExecService: AccountExecService,
    private fb: FormBuilder
  ) {
    this.addExecutiveForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  ngOnInit(): void {
    this.fetchDashboardData();
    this.fetchAccountExecData();
    this.fetchTopExecutivesChart();

    // Static Testing Data for the account executives table
    this.accountExecData = [
      {
        executive_id: 1,
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        location: 'Calgary',
        performance: '$50000',
        status: 'Active',
        assigned_accounts: ["Sigma Strategies", "Beta Biotech", "Alpha Agencies"]
      },
      {
        executive_id: 2,
        first_name: 'Jane',
        last_name: 'Doe',
        email: 'jane.doe@example.com',
        location: 'Toronto',
        performance: '$70000',
        status: 'Active',
        assigned_accounts: [1, 2, 17, 67, 68, 71]
      }
    ]
    // Static Testing Data for the bar chart
    this.topExecutivesChartData = [
      { category: 'John Doe', count: 50000 },
      { category: 'Jane Doe', count: 70000 },
      { category: 'Emily Johnson', count: 80000 },
      { category: 'Michael Brown', count: 75000 },
      { category: 'Steven White', count: 100},
      { category: 'Sarah Black', count: 90000}
    ];

    this.updateBarChartData();
  }

  fetchDashboardData(): void {
    this.dashboardService
      .getPipelineCount()
      .subscribe((response: { pipeline_count: number }) => {
        this.pipelineCount = response.pipeline_count;
      });
    
    this.dashboardService
      .getRevenueSum()
      .subscribe((response: { revenue_sum: number }) => {
        this.revenueCount = response.revenue_sum;
      });
    
    this.dashboardService
      .getSigningsCount()
      .subscribe((response: { signings_count: number }) => {
        this.signingsCount = response.signings_count;
      });
    
    this.dashboardService
      .getWinsCount()
      .subscribe((response: { wins_count: number }) => {
        this.winsCount = response.wins_count;
      });
  }

  fetchAccountExecData(): void {
    this.accountExecService
      .getAccountExecData()
      .pipe(first())
      .subscribe((data: any[]) => {
        this.accountExecData = data;
        this.isDataLoaded = true;
      })
  }

  toggleExecutive(executive: any): void {
    this.selectedExecutive = this.selectedExecutive === executive ? null : executive;
  }

  fetchTopExecutivesChart(): void {
    this.accountExecService.getTopExecutivesChart().subscribe((data) => {
      this.topExecutivesChartData = data;
      this.isDataLoaded = true;
      this.updateBarChartData();
    });
  }
  updateBarChartData(): void {
    if (this.topExecutivesChartData.length > 0) {
      const top5Executives = this.topExecutivesChartData
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);
  
      this.barChart = {
        ...this.barChart,
        series: [
          {
            data: top5Executives.map((item) => item.count),
            name: '',
          },
        ],
        xaxis: {
          categories: top5Executives.map((item) => item.category),
        },
      };
    }
  }

  get cards() {
    return [
      {
        title: 'Pipeline',
        value: `$${this.pipelineCount}`,
        percentage: '+55%',
      },
      {
        title: 'Revenue',
        value: `$${this.revenueCount}`,
        percentage: '+5%',
      },
      {
        title: 'Signings',
        value: `$${this.signingsCount}`,
        percentage: '+8%',
      },
      {
        title: 'Count To Wins',
        value: `$${this.winsCount}`,
        percentage: '-14%',
      }
    ]
  }
  
  barChart = {
    chart: {
      type: 'bar' as ApexChart['type'],
      height: 350,
    },
    series: [
      {
        name: 'Top Executives by Sales',
        data: [] as number[],
      },
    ],
    plotOptions: {
      bar: {
        horizontal: true,
        columnWidth: '50%',
        distributed: true,
      },
    },
    dataLabels: { enabled: true },
    colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560'],
    tooltip: {
      enabled: true,
      y: { formatter: (val: number) => `${val} Sales` },
    },
    legend: {
      show: false,
    },
    xaxis: {
      categories: [] as string[],
    },
  };

  addExecutive(): void {
    if (this.addExecutiveForm.valid) {
      this.accountExecService.addExecutive(this.addExecutiveForm.value).subscribe({
        next: (response) => {
          alert('New Executive Added');
          this.accountExecutives.push(response);
          this.addExecutiveForm.reset();
        },
        error: (error) => {
          console.error('Error Adding new Executive:', error);
          alert('Failed to Add New Executive. Please check your input.');
        }
      })
    } else {
      alert('Please fill in all required fields');
    }
  }

  removeExecutive(executiveId: number): void {
    if (confirm('Are you sure you want to delete this executive?')) {
      this.accountExecService.removeExecutive(executiveId).subscribe({
        next: () => {
          this.accountExecutives = this.accountExecutives.filter(executive => executive.executive_id !== executiveId);
        },
        error: (error) => {
          console.error('Error Deleting Executive:', error);
          alert('Error Deleting Executive. Please try again.');
        }
      })
    }
  }
}
