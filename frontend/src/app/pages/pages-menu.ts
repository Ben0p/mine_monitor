import { NbMenuItem } from '@nebular/theme';


export const MENU_ITEMS: NbMenuItem[] = [
  {
    title: 'Dashboard',
    icon: 'home-outline',
    link: '/pages/dashboard',
    home: true,
    data: {
      permission: 'view',
      resource: 'dashboard'
    },
  },
  {
    title: 'Alerts',
    icon: 'bulb-outline',
    data: {
      permission: 'view',
      resource: 'alerts'
    },
    children: [
      {
        title: 'Overview',
        link: '/pages/alerts/overview',
        data: {
          permission: 'view',
          resource: 'alerts_overview'
        },
      },
      {
        title: 'All',
        link: '/pages/alerts/all',
        data: {
          permission: 'view',
          resource: 'alerts_all'
        },
      },
      {
        title: 'Display',
        link: '/pages/alerts/display',
        data: {
          permission: 'view',
          resource: 'alerts_display'
        },
      },
      {
        title: 'List',
        link: '/pages/alerts/list',
        data: {
          permission: 'view',
          resource: 'alerts_list'
        },
      },
      {
        title: 'Edit',
        link: '/pages/alerts/edit',
        data: {
          permission: 'view',
          resource: 'alerts_edit'
        },
      },
    ]
  },
  {
    title: 'Settings',
    icon: 'options-2-outline',
    data: {
      permission: 'view',
      resource: 'settings'
    },
    children: [
      {
        title: 'Style',
        link: '/pages/settings/style',
        data: {
          permission: 'view',
          resource: 'settings_style'
        },
      },
    ]
  },
];
