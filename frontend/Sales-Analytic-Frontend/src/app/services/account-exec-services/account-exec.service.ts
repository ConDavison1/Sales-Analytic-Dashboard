import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

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
  constructor(private http: HttpClient, private router: Router) { }

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    if (!token) {
      console.warn("No JWT token found Redirecting to login.");
      this.router.navigate(['/login']);
      return new HttpHeaders();
    }
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }

  getAccountExecData(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/account-exec-table`);
  }
  getTopExecutivesChart(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/topExecutivesChart`);
  }
  addExecutive(account_executives: Account_Executives): Observable<Account_Executives> {
    return this.http.post<Account_Executives>(`${this.apiUrl}/account-exec-table`, account_executives);
  }
  removeExecutive(executiveId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/clients/${executiveId}`, { headers: this.getAuthHeaders() })
      .pipe(catchError(this.handleError));
  }

  private handleError(error: any): Observable<never> {
    console.error("API Error:", error);
    return throwError(error);
  }
}
