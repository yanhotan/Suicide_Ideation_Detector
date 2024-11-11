import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private backendUrl = 'http://localhost:5000/api/generate';  // Ensure this matches your Node.js server

  constructor(private http: HttpClient) {}

  getGeminiPrediction(message: string): Observable<any> {
    return this.http.post<any>(this.backendUrl, { prompt: message });
  }
}
