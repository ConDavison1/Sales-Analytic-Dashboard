import { ClientService } from './../../services/client-services/client.service';
import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-clients-page',
  standalone: true,
  imports: [HeaderComponent, SidebarComponent, CommonModule],
  templateUrl: './clients-page.component.html',
  styleUrl: './clients-page.component.css'
})
export class ClientsPageComponent implements OnInit {


  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;
  
  constructor(private clientService: ClientService) { }
  
  ngOnInit(): void {
    this.fetchCardData();
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
      { title: 'Pipeline', value: `${this.pipelineCount}`, percentage: '+55%' },
      { title: 'Revenue', value: `${this.revenueCount}`, percentage: '+5%' },
      { title: 'Signings', value: `${this.signingsCount}`, percentage: '+89%' },
      { title: 'Count To Wins', value: `${this.winsCount}`, percentage: '-14%' }
    ];
  }


}
