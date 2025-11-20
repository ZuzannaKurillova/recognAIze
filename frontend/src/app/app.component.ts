import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageUploadComponent } from './components/image-upload/image-upload.component';
import { CaptionDisplayComponent } from './components/caption-display/caption-display.component';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    ImageUploadComponent,
    CaptionDisplayComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'RecogAIze - AI Image Captioning';

  caption = signal<string | null>(null);
  isLoading = signal<boolean>(false);
  error = signal<string | null>(null);

  constructor(private apiService: ApiService) { }

  onFileSelected(file: File): void {
    this.isLoading.set(true);
    this.error.set(null);
    this.caption.set(null);

    this.apiService.generateCaption(file).subscribe({
      next: (response) => {
        this.caption.set(response.caption);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.error.set(err.message || 'Failed to generate caption');
        this.isLoading.set(false);
      }
    });
  }
}
