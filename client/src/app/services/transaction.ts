import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export interface Transaction {
  id: number;
  hash: string;
  inputs: any;
  out: any;
  fee: number;
  date: Date;
  address: number;
}

type TransactionsResponse = {
  count: number;
  next: string;
  previous: string;
  results: Transaction[];
};

const BASE_URL = "http://localhost:8000";

export const api = createApi({
  reducerPath: "transactionsApi",
  baseQuery: fetchBaseQuery({
    baseUrl: `${BASE_URL}/`,
    prepareHeaders: (headers, { getState }) => {
      const token = localStorage.getItem("CoinTrackerDemoToken");
      if (token) {
        headers.set("Authorization", `token ${token}`);
      }
      return headers;
    },
  }),
  endpoints: (builder) => ({
    getTransactions: builder.query<
      TransactionsResponse,
      { address: string; limit: number; offset: number }
    >({
      query: ({ address, limit, offset }) =>
        `transactions/?search=${address}&limit=${limit}&offset=${offset}`,
    }),
  }),
});

export const { useGetTransactionsQuery } = api;
