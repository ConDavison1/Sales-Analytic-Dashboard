import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { appRoutes } from './app.routes';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { BrowserModule } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(appRoutes), provideAnimationsAsync('noop'),
    importProvidersFrom(
      MatDialogModule,
      MatButtonModule,
      MatInputModule,
      MatFormFieldModule,
      BrowserModule
    ), provideAnimationsAsync('noop'),
  ],
};