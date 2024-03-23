import { lazy } from 'react';

// project import
import GuestGuard from 'auth/GuestGuard';
import CommonLayout from 'layout/CommonLayout';
import Loadable from 'components/Loadable';
import { PATH_ROOT } from './paths';

// render - login
const AuthLogin = Loadable(lazy(() => import('pages/auth/login')));

// ==============================|| AUTH ROUTING ||============================== //

const LoginRoutes = {
  path: PATH_ROOT,
  children: [
    {
      path: PATH_ROOT,
      element: (
        <GuestGuard>
          <CommonLayout />
        </GuestGuard>
      ),
      children: [
        {
          path: PATH_ROOT,
          element: <AuthLogin />,
        },
        {
          path: 'login',
          element: <AuthLogin />,
        },
      ],
    },
  ],
};

export default LoginRoutes;
