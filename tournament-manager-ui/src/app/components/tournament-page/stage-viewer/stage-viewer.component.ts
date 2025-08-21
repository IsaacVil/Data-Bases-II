import { AfterViewInit, Component, Input } from '@angular/core';

declare global {
  interface Window {
    bracketsViewer?: any | undefined;
  }
}

@Component({
  selector: 'app-stage-viewer',
  standalone: true,
  imports: [],
  templateUrl: './stage-viewer.component.html',
  styleUrl: './stage-viewer.component.scss'
})
export class StageViewerComponent implements AfterViewInit {
  @Input('bracketsId') bracketsId!: string;
  @Input('stageData') stageData!: any;

  async ngAfterViewInit(): Promise<void> {
    (window as any).bracketsViewer.addLocale('en', {
      common: {
        'group-name-winner-bracket': '{{stage.name}}',
        'group-name-loser-bracket': '{{stage.name}} - Repechage',
      },
      'origin-hint': {
        'winner-bracket': 'WB {{round}}.{{position}}',
        'winner-bracket-semi-final': 'WB Semi {{position}}',
        'winner-bracket-final': 'WB Final',
        'consolation-final': 'Semi {{position}}',
      },
    });
    console.log('Brackets data loaded:', this.stageData);
    window.bracketsViewer.render(this.stageData, {
      selector: `#${this.bracketsId}`,
    });
  }
}
