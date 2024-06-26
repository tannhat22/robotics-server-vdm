import { useContext } from 'react';

// auth provider
import AuthContext from './Auth0Context';

// ==============================|| AUTH HOOKS ||============================== //

const useAuthContext = () => {
  const context = useContext(AuthContext);

  if (!context) throw new Error('context must be use inside provider');

  return context;
};

export default useAuthContext;
