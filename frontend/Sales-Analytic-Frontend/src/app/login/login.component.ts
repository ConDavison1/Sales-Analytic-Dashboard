import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { ForgotPasswordModalComponent } from '../forgot-password-modal/forgot-password-modal.component';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule,
    HttpClientModule,
    MatDialogModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    NgIf,
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  message: string = '';

  constructor(private http: HttpClient, private router: Router, private dialog: MatDialog) {}

  openForgotPasswordModal(): void {
    this.dialog.open(ForgotPasswordModalComponent, {
      width: '60%'
    });
  }

  showPassword = false;

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onLogin() {
    const payload = { username: this.username, password: this.password };
  
    console.log('Sending login request with payload:', payload);
  
    this.http.post('http://localhost:5000/api/auth/login', payload).subscribe({
      next: (response: any) => {
        console.log('Login response:', response);
  
        if (!response.user || !response.token) {
          this.message = "Login failed: Missing user or token in response!";
          console.log(this.message);
          return;
        }
  
        
        localStorage.setItem('token', response.token); 
        localStorage.setItem('user', JSON.stringify(response.user));
        localStorage.setItem('username', response.user.username.trim().toLowerCase());
  
        console.log('User Info:', response.user);
  
        this.router.navigate(['/landing-page']);
      },
      error: (error) => {
        console.error("Login Error:", error);
        this.message = error.error.error || 'Login failed!';
      }
    });
  }
  

  
  
}
