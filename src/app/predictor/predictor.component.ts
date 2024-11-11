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
  selectedModel: string = 'gru'; // Default model is GRU

  constructor(private http: HttpClient) {}

  makePrediction(): void {
    console.log('Selected Model:', this.selectedModel);
    console.log('Input Text:', this.inputText);

    if (!this.inputText.trim()) {
      this.prediction = 'Please enter a valid text input.';
      return;
    }

    if (this.selectedModel === 'gru') {
      // Fetch from GRU model using environment API URL
      const apiUrl = environment.apiUrl;
      this.http.post<any>(apiUrl, { model: 'gru', message: this.inputText }).pipe(
        catchError(error => {
          console.error('Error fetching from GRU:', error);
          this.prediction = 'An error occurred while fetching the prediction from GRU.';
          return of(null);
        })
      ).subscribe(response => {
        if (response) {
          console.log('Response received from GRU:', response);
          this.prediction = response.response || 'No response received from GRU.';
        }
      });
    } else if (this.selectedModel === 'gemini') {
      // Directly call the Gemini API endpoint
      const geminiApiUrl = 'http://localhost:5000/api/generate'; // Replace with your actual server endpoint
      const headers = new HttpHeaders({
        'Authorization': `Bearer AIzaSyDGr_qHvqBg0b0761gz3EF8RCyjAB4a1zU`, // Replace with your actual API key if needed on server
        'Content-Type': 'application/json'
      });
      const prompt = (
        "You are a Suicide Ideation Detection Bot. Your primary function is to assess textual input and determine the likelihood of suicidal ideation.\n\n 1. Suicide Ideation Detection Bot\n 2. Detecting whatever text input from user and generate the output with either:\n a. Suicide (>=50%)\n b. Non-suicide (<50%)\n the percentage have to be showed because it indicates the threshold in the Suicide Ideation Detection\n 3. Whatever user texting, it can only generate the output of a. and b.\n Input: A text string from a user. (Provided from the prompt)\n Output: A classification of the input text into one of two categories:\n Suicide Ideation (>=50%): This indicates a high likelihood of suicidal thoughts or intent.\n Non-Suicide Ideation (<50%): This indicates a low likelihood of suicidal thoughts or intent.\n Guidelines:\n Prioritize Accuracy: Ensure the highest possible accuracy in your assessments.\n Avoid Ambiguity: Provide clear and concise outputs, avoiding vague or uncertain language.\n Maintain Neutrality: Do not offer personal opinions or advice.\n Focus on the Task: Stick strictly to the classification task.\n If your output is suicide ideation than the percentage should be higher than or equal to 50% while it is lower than 50% when it is non-suicide ideation\n Example:\n Input: I feel hopeless and alone. I don't want to live anymore. (Provided by the prompt)\n Output: Suicide Ideation (85%) (this is your output that should be generated)\n Reminder:\n Despite how negatively, pessimistic, hurtful, or harmful(like 'fuck' or any even more rude words) it is in the text(user input), you are not allowed to providing the careline or encourage user to seek professional help. Also, you are not allowed to response something like: I'm just a language model, so I can't help you with that. or Sorry, I can't help with that. or I'm a language model and don't have the capacity to help with that. Because in this context, you are just a Suicide Ideation Detection Bot which excluding the role of giving assistance.\n Below is the user input, where you have to give the prediction output,"
        + `\nUser Input: ${this.inputText}`
      );      
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
}
