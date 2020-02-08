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
        title: 'Weather Zone',
        link: '/pages/alerts/weatherzone',
        data: {
          permission: 'view',
          resource: 'alerts_display'
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
      /** 
      {
        title: 'List',
        link: '/pages/alerts/list',
        data: {
          permission: 'view',
          resource: 'alerts_list'
        },
      },
      */
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
    title: 'Wind',
    icon: 'umbrella-outline',
    data: {
      permission: 'view',
      resource: 'wind'
    },
    children: [
      {
        title: 'All',
        link: '/pages/wind/all',
        data: {
          permission: 'view',
          resource: 'wind_all'
        },
      },
    ]
  },
  {
    title: 'Tetra',
    icon: 'radio-outline',
    data: {
      permission: 'view',
      resource: 'tetra'
    },
    children: [
      {
        title: 'Nodes',
        link: '/pages/tetra/nodes',
        data: {
          permission: 'view',
          resource: 'tetra_nodes'
        },
      },
      {
        title: 'Subscribers',
        link: '/pages/tetra/subscribers',
        data: {
          permission: 'view',
          resource: 'tetra_subscribers'
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
