import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StageViewerComponent } from './stage-viewer.component';

describe('StageViewerComponent', () => {
  let component: StageViewerComponent;
  let fixture: ComponentFixture<StageViewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StageViewerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StageViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
