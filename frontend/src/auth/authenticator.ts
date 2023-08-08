// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import {
  AppAuthError,
  AuthorizationNotifier,
  AuthorizationRequest,
  AuthorizationRequestHandler,
  AuthorizationResponse,
  AuthorizationServiceConfiguration,
  BaseTokenRequestHandler,
  BasicQueryStringUtils,
  FetchRequestor,
  GRANT_TYPE_AUTHORIZATION_CODE,
  GRANT_TYPE_REFRESH_TOKEN,
  LocalStorageBackend,
  RedirectRequestHandler,
  RevokeTokenRequest,
  TokenRequest,
  TokenResponse,
  type LocationLike,
  type StringMap,
  type TokenRequestHandler,
} from "@openid/appauth";
import {
  UserInfoRequest,
  UserInfoRequestHandler,
  type UserInfoResponseJson,
} from "./userinfo_request";

export class NoHashQueryStringUtils extends BasicQueryStringUtils {
  parse(input: LocationLike) {
    return super.parse(input, false /* never use hash */);
  }
}

const requestor = new FetchRequestor();

export default class Authenticator {
  private openIdConnectUrl: string;
  private clientId: string;
  private redirectUri: string;
  private notifier: AuthorizationNotifier;
  private authorizationHandler: AuthorizationRequestHandler;
  private tokenHandler: TokenRequestHandler;
  private storage: LocalStorageBackend;

  // state
  private configuration: AuthorizationServiceConfiguration | undefined;

  constructor(openIdConnectUrl: string, clientId: string, redirectUri: string) {
    this.openIdConnectUrl = openIdConnectUrl;
    this.clientId = clientId;
    this.redirectUri = redirectUri;
    this.storage = new LocalStorageBackend();
    this.notifier = new AuthorizationNotifier();
    this.authorizationHandler = new RedirectRequestHandler(
      this.storage,
      new NoHashQueryStringUtils(),
    );
    this.tokenHandler = new BaseTokenRequestHandler(requestor);
    // set notifier to deliver responses
    this.authorizationHandler.setAuthorizationNotifier(this.notifier);
  }

  fetchServiceConfiguration(
    force = false,
  ): Promise<AuthorizationServiceConfiguration> {
    if (this.configuration && !force) {
      return Promise.resolve(this.configuration);
    }
    return AuthorizationServiceConfiguration.fetchFromIssuer(
      this.openIdConnectUrl,
      requestor,
    ).then((response) => {
      console.log("Fetched service configuration", response);
      this.configuration = response;
      return response;
    });
  }

  makeAuthorizationRequest(scope: string) {
    if (!this.configuration) {
      throw new AppAuthError("Configuration is not initialized");
    }
    // create a request
    const request = new AuthorizationRequest({
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      scope: scope,
      response_type: AuthorizationRequest.RESPONSE_TYPE_CODE,
      state: undefined,
    });

    console.log("Making authorization request ", this.configuration, request);
    this.authorizationHandler.performAuthorizationRequest(
      this.configuration,
      request,
    );
  }

  makeRefreshTokenRequest(
    request: AuthorizationRequest,
    response: AuthorizationResponse,
  ) {
    if (!this.configuration) {
      throw new AppAuthError("Configuration is not initialized");
    }
    let extras: StringMap | undefined = undefined;
    if (request && request.internal) {
      extras = {};
      extras["code_verifier"] = request.internal["code_verifier"];
    }

    const tokenRequest = new TokenRequest({
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      grant_type: GRANT_TYPE_AUTHORIZATION_CODE,
      code: response.code,
      refresh_token: undefined,
      extras: extras,
    });

    return this.tokenHandler
      .performTokenRequest(this.configuration, tokenRequest)
      .then((response) => {
        if (!response.refreshToken) {
          throw "No refresh_token in response";
        }
        return response;
      });
  }

  makeAccessTokenRequest(refreshToken: string) {
    if (!this.configuration) {
      throw new AppAuthError("Configuration is not initialized");
    }

    const request = new TokenRequest({
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      grant_type: GRANT_TYPE_REFRESH_TOKEN,
      code: undefined,
      refresh_token: refreshToken,
      extras: undefined,
    });

    return this.tokenHandler
      .performTokenRequest(this.configuration, request)
      .then((response) => {
        if (!response.accessToken) {
          return Promise.reject("No access_token in response");
        }
        return response;
      });
  }

  makeRevokeTokenRequest(refreshToken: string) {
    if (!this.configuration) {
      throw new AppAuthError("Configuration is not initialized");
    }

    const request = new RevokeTokenRequest({ token: refreshToken });

    return this.tokenHandler.performRevokeTokenRequest(
      this.configuration,
      request,
    );
  }

  handleAuthorizationRedirect(): Promise<TokenResponse> {
    return new Promise((resolve, reject) => {
      this.notifier.setAuthorizationListener((request, response, error) => {
        console.log(
          "Authorization request complete ",
          request,
          response,
          error,
        );
        if (response) {
          return this.makeRefreshTokenRequest(request, response).then(
            (result) => {
              resolve(result);
            },
            (error) => {
              reject(error);
            },
          );
        } else {
          // Either response is defined or error is defined, no other possibility
          // See @openid/appauth/src/redirect_based_handler.ts
          let content = error ? error.error : "Error";
          if (error?.errorDescription) {
            content =
              error.errorDescription.replace(/\+/g, " ") + ` (${error.error})`;
          }
          reject(content);
        }
      });
      return this.authorizationHandler.completeAuthorizationRequestIfPossible();
    });
  }

  makeUserInfoRequest(accessToken: string): Promise<UserInfoResponseJson> {
    if (!this.configuration) {
      throw new AppAuthError("Configuration is not initialized");
    }
    const request = new UserInfoRequest({
      access_token: accessToken,
    });
    const userInfoHandler = new UserInfoRequestHandler(requestor);
    return userInfoHandler.performUserInfoRequest(this.configuration, request);
  }
}
