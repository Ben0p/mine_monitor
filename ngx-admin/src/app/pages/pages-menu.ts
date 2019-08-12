import { NbMenuItem } from '@nebular/theme';

export const MENU_ITEMS: NbMenuItem[] = [
  {
    title: 'Dashboard',
    icon: 'home-outline',
    link: '/pages/dashboard',
    home: true,
  },
  {
    title: 'Alerts',
    icon: 'bulb-outline',
    children: [
      {
        title: 'Overview',
        link: '/pages/alerts/overview'
      },
      {
        title: 'All',
      },
      {
        title: 'List',
        link: '/pages/alerts/list'
      },
    ]
  },
  {
    title: 'Auth',
    icon: 'lock-outline',
    children: [
      {
        title: 'Login',
        link: '/auth/login',
      },
      {
        title: 'Register',
        link: '/auth/register',
      },
      {
        title: 'Request Password',
        link: '/auth/request-password',
      },
      {
        title: 'Reset Password',
        link: '/auth/reset-password',
      },
    ],
  },
  {
    title: 'Settings',
    icon: 'options-2-outline',
    children: [
      {
        title: 'Style',
        link: '/pages/settings/style',
      },
    ]
  },
];
