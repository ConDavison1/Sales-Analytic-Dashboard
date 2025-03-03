import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface Wins {
  win_id: number;
  client_id: number;
  executive_id: number;
  win_date: string;
  revenue: number;
}

@Injectable({
  providedIn: 'root',
})
export class WinsService {
  baseUrl = 'http://localhost:5000';
  constructor(private http: HttpClient) {}

  getWins(): Observable<Wins[]> {
    return this.http.get<Wins[]>(`${this.baseUrl}/wins`);
  }
}
