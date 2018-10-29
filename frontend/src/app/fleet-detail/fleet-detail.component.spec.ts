import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FleetDetailComponent } from './fleet-detail.component';

describe('FleetDetailComponent', () => {
  let component: FleetDetailComponent;
  let fixture: ComponentFixture<FleetDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FleetDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FleetDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
