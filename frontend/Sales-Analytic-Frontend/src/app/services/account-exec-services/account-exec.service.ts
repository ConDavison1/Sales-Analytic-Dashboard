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
interface Account_Executives {
  executive_id: number;
  first_name: string;
  last_name: string;
  email: string;
}

@Injectable({
  providedIn: 'root'
})
export class AccountExecService {

  private apiUrl = 'http://localhost:5000';
  constructor(private http: HttpClient) { }

  getAccountExecData(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/account-exec-table`);
  }
  getTopExecutivesChart(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/topExecutivesChart`);
  }
  addExecutive(account_executives: Account_Executives): Observable<Account_Executives> {
    return this.http.post<Account_Executives>(`${this.apiUrl}/account-exec-table`, account_executives);
  }
}
