import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrailersDetailComponent } from './trailers-detail.component';

describe('TrailersDetailComponent', () => {
  let component: TrailersDetailComponent;
  let fixture: ComponentFixture<TrailersDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrailersDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrailersDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
