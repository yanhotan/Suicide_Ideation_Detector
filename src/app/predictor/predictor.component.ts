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

  // Load the static prompt template from a local file
  loadPrompt(): void {
    this.http.get('assets/prompt.txt', { responseType: 'text' })
      .pipe(catchError(error => {
        console.error('Error loading prompt file:', error);
        return of(''); // Return empty string on error
      }))
      .subscribe(data => {
        this.promptTemplate = data || '';
        console.log('Prompt loaded successfully:', this.promptTemplate); // Log the prompt contents
      });
  }

  // Make predictions using the selected model
  async makePrediction(): Promise<void> {
    console.log('Selected Model:', this.selectedModel);
    console.log('Input Text:', this.inputText);

    if (!this.inputText.trim()) {
      this.prediction = 'Please enter a valid text input.';
      return;
    }

    if (this.selectedModel === 'gemini') {
      // try {
      //   // Use the Gemini API
      //   const { GoogleGenerativeAI } = await import('@google/generative-ai');
      //   const apiKey = 'YOUR_API_KEY'; // Replace with your Gemini API key
      //   const genAI = new GoogleGenerativeAI(apiKey);
      //   const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });

      //   const prompt = this.promptTemplate + `\nUser Input: ${this.inputText}`; // Append user input to the prompt
      //   const result = await model.generateContent(prompt);

      //   console.log('Response received from Gemini:', result);
      //   this.prediction = result.response.text || 'No response received from Gemini.';
      // } catch (error) {
      //   console.error('Error calling Gemini API:', error);
      //   this.prediction = 'An error occurred while fetching the prediction from Gemini.';
      // }
    } else {
      const apiUrl = environment.apiUrl; // Base API URL from environment

      const payload = { model: this.selectedModel, message: this.inputText };

      this.http.post<any>(apiUrl, payload).pipe(
        catchError(error => {
          console.error(`Error fetching from ${this.selectedModel.toUpperCase()}:`, error);
          this.prediction = `An error occurred while fetching the prediction from ${this.selectedModel.toUpperCase()}.`;
          return of(null);
        })
      ).subscribe(response => {
        if (response) {
          console.log(`Response received from ${this.selectedModel.toUpperCase()}:`, response);
          this.prediction = response.response || `No response received from ${this.selectedModel.toUpperCase()}.`;
        }
      });
    }
  }
}
