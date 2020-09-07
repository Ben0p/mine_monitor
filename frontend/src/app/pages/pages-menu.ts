import { NbMenuItem } from '@nebular/theme';


export const MENU_ITEMS: NbMenuItem[] = [
  {
    title: 'Dashboards',
    icon: 'home-outline',
    link: '/pages/dashboards',
    home: true,
    data: {
      permission: 'view',
      resource: 'dashboards'
    },
    children: [
      {
        title: 'Alerts / Tetra',
        icon: 'keypad-outline',
        link: '/pages/dashboards/alerts-tetra',
        data: {
          permission: 'view',
          resource: 'dashboards'
        },
      },
      {
        title: 'Power',
        icon: 'keypad-outline',
        link: '/pages/dashboards/power',
        data: {
          permission: 'view',
          resource: 'dashboards'
        },
      },
    ]
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
        icon: 'pie-chart-outline',
        link: '/pages/alerts/overview',
        data: {
          permission: 'view',
          resource: 'alerts_overview'
        },
      },
      {
        title: 'All',
        icon: 'keypad-outline',
        link: '/pages/alerts/all',
        data: {
          permission: 'view',
          resource: 'alerts_all'
        },
      },
      {
        title: 'Weather Zone',
        icon: 'flash-outline',
        link: '/pages/alerts/weatherzone',
        data: {
          permission: 'view',
          resource: 'alerts_display'
        },
      },
      {
        title: 'Display',
        icon: 'loader-outline',
        link: '/pages/alerts/display',
        data: {
          permission: 'view',
          resource: 'alerts_display'
        },
      },
      {
        title: 'Edit',
        icon: 'edit-outline',
        link: '/pages/alerts/edit',
        data: {
          permission: 'view',
          resource: 'alerts_edit'
        },
      },
    ]
  },
  {
    title: 'Power',
    icon: 'power-outline',
    data: {
      permission: 'view',
      resource: 'settings'
    },
    children: [
      {
        title: 'Generators',
        icon: 'settings-2-outline',
        data: {
          permission: 'view',
          resource: 'gen'
        },
        children: [
          {
            title: 'Status',
            icon: 'pie-chart-outline',
            link: '/pages/gen/status',
            data: {
              permission: 'view',
              resource: 'gen_status'
            },
          },
        ]
      },
      {
        title: 'Solar',
        icon: 'sun-outline',
        data: {
          permission: 'view',
          resource: 'solar'
        },
        children: [
          {
            title: 'Controllers',
            icon: 'pie-chart-outline',
            link: '/pages/solar/controllers',
            data: {
              permission: 'view',
              resource: 'solar_controllers'
            },
          },
          {
            title: 'Edit',
            icon: 'edit-outline',
            link: '/pages/solar/edit',
            data: {
              permission: 'view',
              resource: 'solar_edit'
            },
          },
        ]
      },
      {
        title: 'UPS',
        icon: 'battery-outline',
        data: {
          permission: 'view',
          resource: 'ups'
        },
        children: [
          {
            title: 'Status',
            icon: 'pie-chart-outline',
            link: '/pages/ups/status',
            data: {
              permission: 'view',
              resource: 'ups_status'
            },
          },
          {
            title: 'Edit',
            icon: 'edit-outline',
            link: '/pages/ups/edit',
            data: {
              permission: 'admin',
              resource: 'ups_edit'
            },
          },
        ]
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
        icon: 'keypad-outline',
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
        icon: 'shake-outline',
        link: '/pages/tetra/nodes',
        data: {
          permission: 'view',
          resource: 'tetra_nodes'
        },
      },
      {
        title: 'Subscribers',
        icon: 'person-outline',
        link: '/pages/tetra/subscribers',
        data: {
          permission: 'view',
          resource: 'tetra_subscribers'
        },
      },
    ]
  },
  {
    title: 'FM',
    icon: 'music-outline',
    data: {
      permission: 'view',
      resource: 'gen'
    },
    children: [
      {
        title: 'Status',
        icon: 'keypad-outline',
        link: '/pages/fm/status',
        data: {
          permission: 'view',
          resource: 'fm_status'
        },
      },
      {
        title: 'Edit',
        icon: 'edit-outline',
        link: '/pages/fm/edit',
        data: {
          permission: 'view',
          resource: 'fm_edit'
        },
      },
    ]
  },
  {
    title: 'Map',
    icon: 'map-outline',
    link: '/pages/map',
    data: {
      permission: 'view',
      resource: 'map'
    },
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
        icon: 'color-palette-outline',
        link: '/pages/settings/style',
        data: {
          permission: 'view',
          resource: 'settings_style'
        },
      },
    ]
  },
];
