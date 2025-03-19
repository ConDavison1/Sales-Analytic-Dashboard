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

interface AccountExecutive {
  executive_id: number;
  first_name: string;
  last_name: string;
}

interface ChartDataResponse {
  wins_count: any;
  pipeline: number[];
  revenue: number[];
  wins: number[];
  signings: number[];
}

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  private baseUrl = 'https://sales-analytics-backend-jcggzuuyxq-uc.a.run.app';

  constructor(private http: HttpClient) {}

  getRevenueSum(): Observable<RevenueSumResponse> {
    return this.http.get<RevenueSumResponse>(`${this.baseUrl}/revenue-sum`);
  }

  getPipelineCount(): Observable<PipelineCountResponse> {
    return this.http.get<PipelineCountResponse>(`${this.baseUrl}/pipeline-count`);
  }

  getSigningsCount(): Observable<SigningsCountResponse> {
    return this.http.get<SigningsCountResponse>(`${this.baseUrl}/signings-count`);
  }

  getWinsCount(): Observable<WinsCountResponse> {
    return this.http.get<WinsCountResponse>(`${this.baseUrl}/wins-count`);
  }

  getAccountExecutives(): Observable<AccountExecutive[]> {
    return this.http.get<AccountExecutive[]>(`${this.baseUrl}/account_executives`); 
  }

  getChartData(): Observable<ChartDataResponse> {
    return this.http.get<ChartDataResponse>(`${this.baseUrl}/chart-data`);
  }
}
