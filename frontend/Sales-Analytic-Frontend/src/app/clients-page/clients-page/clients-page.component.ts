import { ClientService } from './../../services/client-services/client.service';
import { Component, OnInit, ViewChild } from '@angular/core';
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
export class ClientsPageComponent implements OnInit {
  @ViewChild('chart') chart?: ChartComponent;

  public chartOptions: ChartOptions = {
    series: [],
    chart: {
      type: 'polarArea',
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
    labels: [],
    responsive: [],
  };

  Clients: any[] = [];
  isLoadingClients: boolean = true;

  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;
  addClientForm: any;

  constructor(private clientService: ClientService, private fb: FormBuilder) {
    this.addClientForm = this.fb.group({
      executive_id: ['', Validators.required],
      company_name: ['', Validators.required],
      industry: ['', Validators.required],
      location: ['', Validators.required],
      email: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.initializeChart();
    this.fetchCardData();
    this.fetchClients();
  }

  initializeChart(): void {
    this.chartOptions = {
      series: [14, 23, 21, 17, 15, 10],
      chart: {
        type: 'polarArea',
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
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
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
  }

  fetchCardData(): void {
    this.clientService.getPipelineCount().subscribe((response) => {
      this.pipelineCount = response.pipeline_count;
    });

    this.clientService.getRevenueSum().subscribe((response) => {
      this.revenueCount = response.revenue_sum;
    });

    this.clientService.getSigningsCount().subscribe((response) => {
      this.signingsCount = response.signings_count;
    });

    this.clientService.getWinsCount().subscribe((response) => {
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

  fetchClients(): void {
    this.clientService.getClient().subscribe((response) => {
      this.Clients = response;
    });
  }

  deleteClient(clientId: number): void {
    if (confirm('Are you sure you want to delete this client?')) {
      this.clientService.deleteClient(clientId).subscribe(() => {
        this.Clients = this.Clients.filter(
          (client) => client.client_id !== clientId
        );
      });
    }
  }

  addClient(): void {
    if (this.addClientForm.valid) {
      this.clientService.addClient(this.addClientForm.value).subscribe(
        (response) => {
          alert('Client added successfully');
          this.Clients.push(response);
          this.addClientForm.reset();
        },
        (error) => {
          console.error('Error adding client', error);
        }
      );
    } else {
      alert('Please fill in all required fields');
    }
  }
}
