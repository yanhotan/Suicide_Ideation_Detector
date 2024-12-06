import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-predictor',
  templateUrl: './predictor.component.html',
  styleUrls: ['./predictor.component.css']
})
export class PredictorComponent {
  inputText: string = '';
  prediction: string = '';
  selectedModel: string = 'gru';
  promptTemplate: string = '';

  constructor(private http: HttpClient) {
    this.loadPrompt();
  }

  loadPrompt(): void {
    this.http.get('assets/prompt.txt', { responseType: 'text' })
      .pipe(
        catchError(error => {
          console.error('Error loading prompt file:', error);
          return of(''); // Return empty string on error
        })
      )
      .subscribe(data => {
        this.promptTemplate = data || '';
        console.log('Prompt loaded successfully:', this.promptTemplate);
      });
  }

  makePrediction(): void {
    console.log('Selected Model:', this.selectedModel);
    console.log('Input Text:', this.inputText);

    if (!this.inputText.trim()) {
      this.prediction = 'Please enter a valid text input.';
      return;
    }

    if (this.selectedModel === 'gru' || this.selectedModel === 'lr') {
      this.fetchPredictionFromBackend(this.selectedModel);
    } else if (this.selectedModel === 'gemini') {
      this.fetchPredictionFromGemini();
    }
  }

  private fetchPredictionFromBackend(model: string): void {
    const apiUrl = `${environment.apiUrl}/${model}`; // Assuming separate endpoints per model
    const payload = { message: this.inputText };

    this.http.post<any>(apiUrl, payload).pipe(
      catchError(error => {
        console.error(`Error fetching from ${model}:`, error);
        this.prediction = `An error occurred while fetching the prediction from ${model}.`;
        return of(null);
      })
    ).subscribe(response => {
      if (response) {
        console.log(`Response received from ${model}:`, response);
        this.prediction = response.response || `No response received from ${model}.`;
      }
    });
  }

  private fetchPredictionFromGemini(): void {
    const geminiApiUrl = 'http://localhost:5000/api/generate'; // Replace with the actual Gemini server endpoint
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${environment.geminiApiKey}`, // API key from environment
      'Content-Type': 'application/json'
    });

    // Construct the prompt with the template and input text
    const prompt = `${this.promptTemplate}\nUser Input: ${this.inputText}`;
    const payload = { prompt };

    this.http.post<any>(geminiApiUrl, payload, { headers }).pipe(
      catchError(error => {
        console.error('Error fetching from Gemini:', error);
        this.prediction = 'An error occurred while fetching the prediction from Gemini.';
        return of(null);
      })
    ).subscribe(response => {
      if (response) {
        console.log('Response received from Gemini:', response);
        this.prediction = response.response || 'No response received from Gemini.';
      }
    });
  }
}
