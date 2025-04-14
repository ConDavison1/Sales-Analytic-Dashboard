import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  console.log('[AuthInterceptor] Running...');

  if (token) {
    console.log('[AuthInterceptor] Token attached:', token);
    const cloned = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next(cloned);
  } else {
    console.warn('[AuthInterceptor] No token found. Request sent without auth header.');
  }

  return next(req);
};
