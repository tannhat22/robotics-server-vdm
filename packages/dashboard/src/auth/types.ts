import { ReactElement } from 'react';
import { INITIAL, LOGIN, LOGOUT, REGISTER } from 'store/reducers/actions';

// ==============================|| AUTH TYPES  ||============================== //

export type GuardProps = {
  children: ReactElement | null;
};

export type UserProfile = {
  id?: string;
  email?: string;
  avatar?: string;
  image?: string;
  name?: string;
  role?: string;
  tier?: string;
};

export type AuthUserType = null | UserProfile;

export type ActionMapType<M extends { [index: string]: any }> = {
  [Key in keyof M]: M[Key] extends undefined
    ? {
        type: Key;
      }
    : {
        type: Key;
        payload: M[Key];
      };
};

type Payload = {
  [INITIAL]: {
    isLoggedIn: boolean;
    user: AuthUserType;
  };
  [LOGIN]: {
    user: AuthUserType;
  };
  [REGISTER]: {
    user: AuthUserType;
  };
  [LOGOUT]: undefined;
};

export type AuthProps = {
  isLoggedIn: boolean;
  isInitialized: boolean;
  user: AuthUserType;
};

export type AuthActionProps = ActionMapType<Payload>[keyof ActionMapType<Payload>];

export type JWTContextType = {
  isLoggedIn: boolean;
  isInitialized?: boolean;
  user?: AuthUserType;
  logout: () => void;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, firstName: string, lastName: string) => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  updateProfile: VoidFunction;
};
