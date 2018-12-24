import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrailersHomeComponent } from './trailers-home.component';

describe('TrailersHomeComponent', () => {
  let component: TrailersHomeComponent;
  let fixture: ComponentFixture<TrailersHomeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrailersHomeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrailersHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
