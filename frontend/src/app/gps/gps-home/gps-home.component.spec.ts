import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GpsHomeComponent } from './gps-home.component';

describe('GpsHomeComponent', () => {
  let component: GpsHomeComponent;
  let fixture: ComponentFixture<GpsHomeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GpsHomeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GpsHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
