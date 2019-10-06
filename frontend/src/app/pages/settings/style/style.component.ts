import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import {
  NbLayoutComponent,
  NbMediaBreakpoint,
  NbMediaBreakpointsService,
  NbMenuItem,
  NbMenuService,
  NbSidebarService,
  NbThemeService,
} from '@nebular/theme';

import { StateService } from '../../../@core/utils';

import { map, takeUntil, delay, withLatestFrom  } from 'rxjs/operators';
import { Subject } from 'rxjs';


@Component({
  selector: 'ngx-settings-style',
  templateUrl: './style.component.html',
  styleUrls: ['./style.component.scss'],
  providers: [StateService],
})


export class StyleComponent {

  layouts = [];
  sidebars = [];

  private destroy$: Subject<void> = new Subject<void>();
  userPictureOnly: boolean = false;
  user: any;

  themes = [
    {
      value: 'default',
      name: 'Light',
    },
    {
      value: 'dark',
      name: 'Dark',
    },
    {
      value: 'cosmic',
      name: 'Cosmic',
    },
    {
      value: 'corporate',
      name: 'Corporate',
    },
  ];

  currentTheme = 'default';
  layout: any = {};
  sidebar: any = {};

  @ViewChild(NbLayoutComponent, { static: false }) layoutComponent: NbLayoutComponent;

  constructor(
    private sidebarService: NbSidebarService,
    private menuService: NbMenuService,
    private themeService: NbThemeService,
    private breakpointService: NbMediaBreakpointsService,
    protected stateService: StateService,
    protected bpService: NbMediaBreakpointsService,
  ) {
    this.stateService.getLayoutStates()
      .subscribe((layouts: any[]) => this.layouts = layouts);

    this.stateService.getSidebarStates()
      .subscribe((sidebars: any[]) => this.sidebars = sidebars);
  }


  ngOnInit() {
    this.stateService.onLayoutState()
      .pipe(takeUntil(this.destroy$))
      .subscribe(layout => this.layout = layout);

    this.stateService.onSidebarState()
      .pipe(takeUntil(this.destroy$))
      .subscribe(sidebar => this.sidebar = sidebar);
    this.currentTheme = this.themeService.currentTheme;

    const { xl } = this.breakpointService.getBreakpointsMap();
    this.themeService.onMediaQueryChange()
      .pipe(
        map(([, currentBreakpoint]) => currentBreakpoint.width < xl),
        takeUntil(this.destroy$),
      )
      .subscribe((isLessThanXl: boolean) => this.userPictureOnly = isLessThanXl);

    this.themeService.onThemeChange()
      .pipe(
        map(({ name }) => name),
        takeUntil(this.destroy$),
      )
      .subscribe(themeName => this.currentTheme = themeName);
      const isBp = this.bpService.getByName('is');

      this.menuService.onItemSelect()
        .pipe(
          withLatestFrom(this.themeService.onMediaQueryChange()),
          delay(20),
          takeUntil(this.destroy$),
        )
        .subscribe(([item, [bpFrom, bpTo]]: [any, [NbMediaBreakpoint, NbMediaBreakpoint]]) => {
  
          if (bpTo.width <= isBp.width) {
            this.sidebarService.collapse('menu-sidebar');
          }
        });
  
      this.themeService.getJsTheme()
        .pipe(takeUntil(this.destroy$))
        .subscribe(theme => this.currentTheme = theme.name);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  changeTheme(themeName: string) {
    this.themeService.changeTheme(themeName);
  }

  toggleSidebar(): boolean {
    this.sidebarService.toggle(true, 'menu-sidebar');

    return false;
  }

  layoutSelect(layout: any): boolean {
    this.layouts = this.layouts.map((l: any) => {
      l.selected = false;
      return l;
    });

    layout.selected = true;
    this.stateService.setLayoutState(layout);
    return false;
  }

  sidebarSelect(sidebar: any): boolean {
    this.sidebars = this.sidebars.map((s: any) => {
      s.selected = false;
      return s;
    });

    sidebar.selected = true;
    this.stateService.setSidebarState(sidebar);
    return false;
  }
}
