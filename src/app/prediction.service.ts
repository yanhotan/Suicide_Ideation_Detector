// prediction.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private apiUrl = environment.apiUrl;  // Ensure this matches the correct URL

  constructor(private http: HttpClient) { }

  getPrediction(text: string): Observable<any> {
    return this.http.post<any>(this.apiUrl, { message: text }).pipe(
      catchError(error => {
        console.error('Error occurred while fetching the prediction:', error);
        return throwError('An error occurred while fetching the prediction.');
      })
    );
  }
}
