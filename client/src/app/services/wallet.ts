import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export interface Wallet {
  id: number;
  address: string;
  transaction_count: number;
  final_balance: number;
  last_successfull_sync: Date;
  sync_status: string;
  user: number;
}

type WalletsResponse = Wallet[];

const BASE_URL = "http://localhost:8000";

export const api = createApi({
  reducerPath: "walletsApi",
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
  tagTypes: ["Wallet"],
  endpoints: (builder) => ({
    getWallets: builder.query<WalletsResponse, void>({
      query: () => "addresses/",
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Wallet" as const, id })),
              { type: "Wallet", id: "LIST" },
            ]
          : [{ type: "Wallet", id: "LIST" }],
    }),
    addWallet: builder.mutation<Wallet, Partial<Wallet>>({
      query: (body) => ({
        url: "addresses/",
        method: "POST",
        body,
      }),
      invalidatesTags: [{ type: "Wallet", id: "LIST" }],
    }),
    syncWallet: builder.mutation<{ task_id: string }, string>({
      query: (address) => ({
        url: `/addresses/${address}/sync_transactions/`,
        method: "POST",
      }),
    }),
    deleteWallet: builder.mutation<void, string>({
      query(address) {
        return {
          url: `addresses/${address}`,
          method: "DELETE",
        };
      },
      invalidatesTags: (result, error, address) => [
        { type: "Wallet", address },
      ],
    }),
  }),
});

export const {
  useAddWalletMutation,
  useGetWalletsQuery,
  useDeleteWalletMutation,
  useSyncWalletMutation,
} = api;
