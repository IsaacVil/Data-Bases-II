import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { TournamentPageComponent } from "./components/tournament-page/tournament-page.component";
import dataset from './data';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, TournamentPageComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'tournament-manager-ui';
  public dataset = dataset.filter(x => x.roster.length > 1);

  constructor() {
  }
}
