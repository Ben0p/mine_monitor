import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WeatherzoneComponent } from './weatherzone.component';

describe('WeatherzoneComponent', () => {
  let component: WeatherzoneComponent;
  let fixture: ComponentFixture<WeatherzoneComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WeatherzoneComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WeatherzoneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
