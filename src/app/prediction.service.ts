import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private apiUrl = environment.apiUrl; // Endpoint for the GRU model

  constructor(private http: HttpClient) { }

  getPrediction(text: string): Observable<any> {
    const payload = {
      message: text,
      model: 'gru'  // Only use the GRU model
    };

    return this.http.post<any>(this.apiUrl, payload).pipe(
      catchError(error => {
        console.error('Error occurred while fetching the prediction:', error);
        return throwError('An error occurred while fetching the prediction.');
      })
    );
  }
}