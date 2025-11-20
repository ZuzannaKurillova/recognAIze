import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface CaptionResponse {
  caption: string;
  success: boolean;
  message?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  /**
   * Upload image and get caption
   * @param file Image file to upload
   * @returns Observable with caption response
   */
  generateCaption(file: File): Observable<CaptionResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<CaptionResponse>(`${this.apiUrl}/caption`, formData)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Check API health
   * @returns Observable with health status
   */
  checkHealth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Handle HTTP errors
   * @param error HTTP error response
   * @returns Observable error
   */
  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = error.error?.detail || `Server error: ${error.status}`;
    }

    return throwError(() => new Error(errorMessage));
  }
}
