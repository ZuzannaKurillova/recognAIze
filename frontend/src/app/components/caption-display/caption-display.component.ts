import { Component, input, signal, effect } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface CaptionItem {
  caption: string;
  timestamp: Date;
}

@Component({
  selector: 'app-caption-display',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './caption-display.component.html',
  styleUrl: './caption-display.component.css'
})
export class CaptionDisplayComponent {
  caption = input<string | null>(null);
  isLoading = input<boolean>(false);
  error = input<string | null>(null);

  captionHistory = signal<CaptionItem[]>([]);
  private lastProcessedCaption: string | null = null;

  constructor() {
    effect(() => {
      const currentCaption = this.caption();
      const loading = this.isLoading();
      const currentError = this.error();

      if (currentCaption && !loading && !currentError && currentCaption !== this.lastProcessedCaption) {
        this.lastProcessedCaption = currentCaption;

        const newHistory = [
          {
            caption: currentCaption,
            timestamp: new Date()
          },
          ...this.captionHistory()
        ];

        this.captionHistory.set(newHistory.slice(0, 5));
      }
    }, { allowSignalWrites: true });
  }

  clearHistory(): void {
    this.captionHistory.set([]);
    this.lastProcessedCaption = null;
  }
}
