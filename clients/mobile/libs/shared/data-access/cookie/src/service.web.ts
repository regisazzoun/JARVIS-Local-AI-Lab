// Browser sessions are owned by the server/browser, not the native cookie bridge.
// Bearer authentication remains in the existing storage/interceptor. Never copy
// bearer tokens into frontend cookies or pretend to clear HttpOnly cookies.
class BrowserCookieService {
  public setToken(_token: string): Promise<void> { return Promise.resolve(); }
  public clearAll(): Promise<void> { return Promise.resolve(); }
}
export const cookieService = new BrowserCookieService();
