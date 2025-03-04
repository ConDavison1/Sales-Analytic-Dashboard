import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface Wins {
  opportunity_id: number;
  account_name: string;
  industry: string;
  deal_value: number;
  forecast_category: string;
  win_date: string;
}

@Injectable({
  providedIn: 'root',
})
export class WinsService {
  baseUrl = 'http://localhost:5000';
  constructor(private http: HttpClient) {}

  getWins(): Observable<Wins[]> {
    return this.http.get<Wins[]>(`${this.baseUrl}/wins-rows`);
  }
}
