import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import { HeaderComponent } from '../header/header.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { ApexChart } from 'ng-apexcharts';

@Component({
  selector: 'app-revenue-page',
  imports: [HeaderComponent, SidebarComponent, NgApexchartsModule, CommonModule],
  standalone: true,
  templateUrl: './revenue-page.component.html',
  styleUrl: './revenue-page.component.css'
})
export class RevenuePageComponent {

  revenueData = [
    { accountName: "Client 7", revenueType: "GCP", totalRevenue: 1200000, arr: 480000, timePeriod: 2024 },
    { accountName: "Client 40", revenueType: "Workplace", totalRevenue: 3200000, arr: 1200000, timePeriod: 2024 },
    { accountName: "Client 32", revenueType: "GCP", totalRevenue: 480000, arr: 100000, timePeriod: 2024 },
    { accountName: "Client 3", revenueType: "DA", totalRevenue: 600000, arr: 230000, timePeriod: 2024 },
    { accountName: "Client 12", revenueType: "GCP", totalRevenue: 980000, arr: 120000, timePeriod: 2024 },
    { accountName: "Client 70", revenueType: "GCP", totalRevenue: 880000, arr: 220000, timePeriod: 2024 },
  ];

  barChart = {
    chart: { 
      type: 'bar' as ApexChart["type"], 
      height: 350 
    },
    series: [
      { 
        name: "Clients", 
        data: [50, 120, 75]
      }
    ],
    xaxis: { 
      categories: ["GCP", "Workplace", "DA"]
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "50%",
        distributed: true
      }
    },
    dataLabels: { enabled: true },
    colors: ["#008FFB", "#00E396", "#FEB019", "#FF4560"],
    tooltip: {
      enabled: true,
      y: {
        formatter: (val: number) => `${val} Clients`
      }
    }
  };

  gaugeChart = {
    series: [81],
    chart: { 
      type: 'radialBar' as ApexChart["type"], 
      height: 350 
    },
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        track: {
          background: '#e7e7e7',
          strokeWidth: '97%'
        },
        dataLabels: {
          name: { 
            show: true,
            fontSize: '16px',
            offsetY: 20,
            color: '#333',
            formatter: () => "Revenue Target Score" 
          }, 
          value: { 
            fontSize: '24px', 
            show: true,
            offsetY: -10,
            formatter: (val: number) => `${Math.round((val / 100) * 60)}M`
          }
        }
      }
    },
    fill: { colors: ['#4CAF50'] },
    stroke: { lineCap: 'round' as ApexStroke["lineCap"] },
    yaxis: {
      min: 0,
      max: 60
    }
  }
  
  
}
