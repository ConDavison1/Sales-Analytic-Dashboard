import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

interface AccountExecutive {
  user_id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
}

@Injectable({
  providedIn: 'root',
})
export class AccountExecService {
  private apiUrl = `${environment.apiUrl}/api/executives`;

  constructor(private http: HttpClient) {}

  getAccountExecData(): Observable<{ account_executives: any[], count: number }> {
    return this.http.get<{ account_executives: any[], count: number }>(
      `${this.apiUrl}/account-executives`
    );
  }

  getAEPerformance(username: string, year: number = 2024): Observable<any> {
    return this.http.get(`${this.apiUrl}/ae-performance`, {
      params: {
        username,
        year: year.toString(),
      },
    });
  }
}
