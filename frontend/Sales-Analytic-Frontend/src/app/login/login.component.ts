import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  message: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  onLogin() {
    const payload = { username: this.username, password: this.password };

    this.http.post('http://localhost:5000/login', payload).subscribe(
      (response: any) => {
        
        localStorage.setItem('token', response.token);
        this.router.navigate(['/landing-page']);
      },
      (error) => {
        
        this.message = error.error.message || 'Login failed!';
      }
    );
  }
}
