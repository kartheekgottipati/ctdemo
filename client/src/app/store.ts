import { configureStore, ThunkAction, Action } from "@reduxjs/toolkit";
import { api as authAPI } from "./services/auth";
import { api as walletAPI } from "./services/wallet";
import { api as transactionAPI } from "./services/transaction";
import authReducer from "../features/auth/authSlice";

export const store = configureStore({
  reducer: {
    [authAPI.reducerPath]: authAPI.reducer,
    [walletAPI.reducerPath]: walletAPI.reducer,
    [transactionAPI.reducerPath]: transactionAPI.reducer,
    auth: authReducer,
  },
  devTools: process.env.NODE_ENV === "development",
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat([
      authAPI.middleware,
      walletAPI.middleware,
      transactionAPI.middleware,
    ]),
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
