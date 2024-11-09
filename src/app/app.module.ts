import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { PredictorComponent } from './predictor/predictor.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';  // Import FormsModule

@NgModule({
  declarations: [
    AppComponent,
    PredictorComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule  // Include FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }