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

interface Clients {
  client_id: number;
  executive_id: number;
  company_name: string;
  industry: string;
  location: string;
  email: string;
}

@Injectable({
  providedIn: 'root',
})
export class ClientService {
  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  getRevenueSum(): Observable<RevenueSumResponse> {
    return this.http.get<RevenueSumResponse>(`${this.baseUrl}/revenue-sum`);
  }

  getPipelineCount(): Observable<PipelineCountResponse> {
    return this.http.get<PipelineCountResponse>(
      `${this.baseUrl}/pipeline-count`
    );
  }

  getSigningsCount(): Observable<SigningsCountResponse> {
    return this.http.get<SigningsCountResponse>(
      `${this.baseUrl}/signings-count`
    );
  }

  getWinsCount(): Observable<WinsCountResponse> {
    return this.http.get<WinsCountResponse>(`${this.baseUrl}/wins-count`);
  }

  getClient(): Observable<Clients[]> {
    return this.http.get<Clients[]>(`${this.baseUrl}/clients`);
  }

  deleteClient(clientId: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/clients/${clientId}`);
  }

  addClient(client: Clients): Observable<Clients> {
    return this.http.post<Clients>(`${this.baseUrl}/clients`, client);
  }
}
