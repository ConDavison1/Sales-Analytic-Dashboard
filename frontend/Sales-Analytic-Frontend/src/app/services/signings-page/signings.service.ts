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
export class SigningsService {
  getSignings() {
    throw new Error('Method not implemented.');
  }
  private apiUrl = 'https://sales-analytics-backend-jcggzuuyxq-uc.a.run.app';

  constructor(private http: HttpClient) {}


  getSigningsCount(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/signings-count`);
  }
  getSigningsChart(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/signingsChart`);
  }
  getSigningsData(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/signings-data`);
  }
}
