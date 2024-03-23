import { Authenticator, KeycloakAuthenticator, StubAuthenticator } from 'rsv-auth';
// import ResourceManager from './managers/resource-manager';
import { BasePath } from './utils/url';

export interface AppConfig {
  authenticator: Authenticator;
  rsvServerUrl: string;
}

export const appConfig: AppConfig = (() => {
  const authenticator = (() => {
    if (!process.env.REACT_APP_AUTH_PROVIDER) {
      return new StubAuthenticator();
    }
    // it is important that we do not do any processing on REACT_APP_AUTH_PROVIDER so that webpack
    // can remove dead code, we DO NOT want the output to have the stub authenticator even if
    // it is not used.
    const provider = process.env.REACT_APP_AUTH_PROVIDER;
    switch (provider) {
      case 'keycloak':
        if (!process.env.REACT_APP_KEYCLOAK_CONFIG) {
          throw new Error('missing REACT_APP_KEYCLOAK_CONFIG');
        }
        return new KeycloakAuthenticator(
          JSON.parse(process.env.REACT_APP_KEYCLOAK_CONFIG),
          `${window.location.origin}${BasePath}/silent-check-sso.html`
        );
      case 'stub':
        return new StubAuthenticator();
      default:
        throw new Error(`unknown auth provider "${provider}"`);
    }
  })();

  if (!process.env.REACT_APP_RMF_SERVER) {
    throw new Error('REACT_APP_RMF_SERVER is required');
  }

  return {
    authenticator,
    rsvServerUrl: process.env.REACT_APP_RMF_SERVER,
  } as AppConfig;
})();

export default appConfig;
