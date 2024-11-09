import { Component } from '@angular/core';
import { PredictionService } from '../prediction.service';

@Component({
  selector: 'app-predictor',
  templateUrl: './predictor.component.html',
  styleUrls: ['./predictor.component.css']
})
export class PredictorComponent {
  inputText: string = '';
  prediction: string = '';

  constructor(private predictionService: PredictionService) {}

  makePrediction(): void {
    if (this.inputText.trim()) {
      this.predictionService.getPrediction(this.inputText).subscribe(
        response => {
          this.prediction = response.response;  // Display prediction
        },
        error => {
          console.error('Error:', error);
          this.prediction = 'An error occurred while fetching the prediction.';
        }
      );
      this.inputText = '';  // Clear the input field after submitting
    }
  }
}