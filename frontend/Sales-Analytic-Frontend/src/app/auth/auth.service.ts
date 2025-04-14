import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getUsername(): string | null {
    const username = localStorage.getItem('username');
    return username ? username.trim().toLowerCase() : null;
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  isShogg(): boolean {
    return this.getUsername() === 'shogg';
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('user'); 
  }
  
}
