const TOKEN_KEY = "access_token";

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export const isAuthenticated = () => {
  return !!getToken();
};

export const loginUser = (token: string) => {
  localStorage.setItem(TOKEN_KEY, token);
};

export const logoutUser = () => {
  localStorage.removeItem(TOKEN_KEY);
};
