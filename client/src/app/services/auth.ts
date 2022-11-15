import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export interface User {
  first_name: string;
  last_name: string;
  email: string;
}

export interface UserResponse {
  token: string;
}

export interface LoginResponse {
  username: string;
  password: string;
}

const BASE_URL = "http://localhost:8000";

export const api = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: `${BASE_URL}/api/`,
    prepareHeaders: (headers, { getState }) => {
      const token = localStorage.getItem("CoinTrackerDemoToken");
      if (token) {
        headers.set("Authorization", `token ${token}`);
      }
      return headers;
    },
  }),
  endpoints: (builder) => ({
    login: builder.mutation<UserResponse, LoginResponse>({
      query: (credentials) => ({
        url: "login/",
        method: "POST",
        body: credentials,
      }),
    }),
    logout: builder.mutation<void, void>({
      query: () => ({
        url: "logout/",
        method: "POST",
      }),
    }),
  }),
});

export const { useLoginMutation, useLogoutMutation } = api;
