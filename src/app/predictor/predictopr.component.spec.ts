import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { PredictorComponent } from './predictor.component';
import { PredictionService } from '../prediction.service';
import { of } from 'rxjs'; // Import 'of' for creating observable responses

describe('PredictorComponent', () => {
  let component: PredictorComponent;
  let fixture: ComponentFixture<PredictorComponent>;
  let predictionService: PredictionService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PredictorComponent ],
      imports: [ FormsModule, HttpClientTestingModule ],
      providers: [ PredictionService ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictorComponent);
    component = fixture.componentInstance;
    predictionService = TestBed.inject(PredictionService); // Inject the service
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should display a prediction when makePrediction is called', () => {
    // Properly use 'of()' to return an observable with a mock response
    spyOn(predictionService, 'getPrediction').and.returnValue(of({ response: 'Non-suicide (45%)' }));

    component.inputText = 'Test input';
    component.makePrediction();
    fixture.detectChanges(); // Ensure change detection is triggered

    // Verify that the prediction property is updated with the mock response
    expect(component.prediction).toBe('Non-suicide (45%)');
  });

  it('should handle empty input gracefully', () => {
    component.inputText = '';
    component.makePrediction();
    expect(component.prediction).toBe('');
  });

  it('should call the prediction service with the correct input', () => {
    const predictionSpy = spyOn(predictionService, 'getPrediction').and.returnValue(of({ response: 'Non-suicide (45%)' }));
  
    component.inputText = 'Test input';
    component.makePrediction();
    expect(predictionSpy).toHaveBeenCalledWith('Test input'); // Remove the 'gru' argument
  });
});
