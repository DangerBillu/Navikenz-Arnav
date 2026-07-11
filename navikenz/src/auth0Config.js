export const auth0Config = {
  domain: import.meta.env.VITE_AUTH0_DOMAIN,
  clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
}

export const isAuth0Configured = Boolean(
  auth0Config.domain && auth0Config.clientId,
)
