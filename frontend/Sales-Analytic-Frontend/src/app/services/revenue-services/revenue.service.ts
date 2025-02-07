import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RevenueService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  getRevenueClients(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/revenue-client`);
  }
  getRevenueChart(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/revenue-chart-data`);
  }
}
