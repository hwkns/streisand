
interface IAuthInfo {
    isAuthenticated: boolean;
    isAuthenticating: boolean;
    token?: string;
    authenticationError?: string;
}

export default IAuthInfo;