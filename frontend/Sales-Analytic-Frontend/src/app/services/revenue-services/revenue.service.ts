import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface RevenueSumResponse {
  revenue_sum: number;
}

interface PipelineCountResponse {
  pipeline_count: number;
}

interface SigningsCountResponse {
  signings_count: number;
}

interface WinsCountResponse {
  wins_count: number;
}

@Injectable({
  providedIn: 'root'
})
export class RevenueService {
  private apiUrl = 'https://sales-analytics-backend-jcggzuuyxq-uc.a.run.app';

  constructor(private http: HttpClient) {}

  getRevenueClients(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/revenue-client`);
  }
  getRevenueChart(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/revenue-chart-data`);
  }
}
