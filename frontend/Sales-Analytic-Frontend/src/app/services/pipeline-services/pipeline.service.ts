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
export class PipelineService {
  private apiUrl = 'http://localhost:5000';
  constructor(private http: HttpClient) { }

  getPipelineData(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pipeline-data`);
  }
  getPipelineChart(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pipeline-chart-data`);
  }
}
