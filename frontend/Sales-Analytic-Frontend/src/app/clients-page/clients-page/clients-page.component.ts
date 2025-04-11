import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { ClientService } from './../../services/client-services/client.service';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { CommonModule } from '@angular/common';
import { ChartComponent, NgApexchartsModule } from 'ng-apexcharts';
import {
  FormGroup,
  FormBuilder,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';

import {
  ApexNonAxisChartSeries,
  ApexResponsive,
  ApexChart,
  ApexStroke,
  ApexFill,
} from 'ng-apexcharts';

export type ChartOptions = {
  series: ApexNonAxisChartSeries;
  chart: ApexChart;
  labels: string[];
  stroke: ApexStroke;
  fill: ApexFill;
  responsive: ApexResponsive[];
  theme?: any;
};

@Component({
  selector: 'app-clients-page',
  standalone: true,
  imports: [
    HeaderComponent,
    SidebarComponent,
    CommonModule,
    NgApexchartsModule,
    ReactiveFormsModule,
  ],
  templateUrl: './clients-page.component.html',
  styleUrl: './clients-page.component.css',
})
export class ClientsPageComponent implements OnInit, AfterViewInit {
  @ViewChild('chart') chart?: ChartComponent;

  public chartOptions: ChartOptions = {
    series: [8, 6, 10, 9, 7, 11, 10],
    chart: {
      type: 'polarArea',
      foreColor: 'var(--text-color)',
      background: 'transparent',
    },
    theme: {
      mode: 'light',
    },
    stroke: {
      show: true,
      width: 2,
      colors: ['#fff'],
    },
    fill: {
      opacity: 0.8,
      type: 'solid',
    },
    labels: ['Emily', 'Michael', 'Sophia', 'David', 'Olivia', 'James', 'Ava'],
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: {
            width: 200,
          },
          legend: {
            position: 'bottom',
          },
        },
      },
    ],
  };

  clients: any[] = [];
  isLoadingClients: boolean = true;

  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;
  addClientForm: FormGroup;

  constructor(
    private clientService: ClientService,
    private fb: FormBuilder,
    private router: Router
  ) {
    this.addClientForm = this.fb.group({
      executive_id: ['', Validators.required],
      company_name: ['', Validators.required],
      industry: ['', Validators.required],
      location: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  ngOnInit(): void {
    this.initializeChart();
    // this.fetchCardData();
    // this.fetchClients();
  }

  ngAfterViewInit(): void {
    const observer = new MutationObserver(() => {
      this.toggleChartTheme();
    });

    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['class'],
    });
  }

  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');

    this.chart?.updateOptions(
      {
        theme: {
          mode: isDark ? 'dark' : 'light',
        },
        chart: {
          foreColor: 'var(--text-color)',
        },
      },
      false,
      true
    );
  }

  // fetchCardData(): void {
  //   this.clientService.getPipelineCount().subscribe((response) => {
  //     this.pipelineCount = response.pipeline_count;
  //   });

  //   this.clientService.getRevenueSum().subscribe((response) => {
  //     this.revenueCount = response.revenue_sum;
  //   });

  //   this.clientService.getSigningsCount().subscribe((response) => {
  //     this.signingsCount = response.signings_count;
  //   });

  //   this.clientService.getWinsCount().subscribe((response) => {
  //     this.winsCount = response.wins_count;
  //   });
  // }

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

  // fetchClients(): void {
  //   this.clientService.getClients().subscribe({
  //     next: (data) => {
  //       this.clients = data;
  //     },
  //     error: (err) => {
  //       console.error('Error fetching clients:', err);
  //       if (err.status === 401) {
  //         alert('Unauthorized! Redirecting to login...');
  //         this.router.navigate(['/login']);
  //       }
  //     },
  //   });
  // }

  // deleteClient(clientId: number): void {
  //   if (confirm('Are you sure you want to delete this client?')) {
  //     this.clientService.deleteClient(clientId).subscribe({
  //       next: () => {
  //         this.clients = this.clients.filter(
  //           (client) => client.client_id !== clientId
  //         );
  //       },
  //       error: (err) => {
  //         console.error('Error deleting client:', err);
  //         alert('Error deleting client. Please try again.');
  //       },
  //     });
  //   }
  // }

  // addClient(): void {
  //   if (this.addClientForm.valid) {
  //     this.clientService.addClient(this.addClientForm.value).subscribe({
  //       next: (response) => {
  //         alert('Client added successfully');
  //         this.clients.push(response);
  //         this.addClientForm.reset();
  //       },
  //       error: (err) => {
  //         console.error('Error adding client', err);
  //         alert('Failed to add client. Please check your input.');
  //       },
  //     });
  //   } else {
  //     alert('Please fill in all required fields');
  //   }
  // }
}
