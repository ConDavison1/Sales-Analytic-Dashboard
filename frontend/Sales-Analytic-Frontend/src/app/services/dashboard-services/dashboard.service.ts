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
  providedIn: 'root',
})
export class DashboardService {
  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

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

  getAccountExecutives(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/account-executives`);
  }
}
