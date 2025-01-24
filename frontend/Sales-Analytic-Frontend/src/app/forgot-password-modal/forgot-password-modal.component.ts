import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-forgot-password-modal',
  imports: [
    MatDialogModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    FormsModule
  ],
  templateUrl: './forgot-password-modal.component.html',
  standalone: true,
  styleUrl: './forgot-password-modal.component.css'
})
export class ForgotPasswordModalComponent {
  email: string = '';

  constructor(private dialogRef: MatDialogRef<ForgotPasswordModalComponent>) {}

  onSubmit(): void {
    console.log('Password reset email sent to: ', this.email);

    this.dialogRef.close();
  }

  onClose(): void {
    this.dialogRef.close();
  }
}
