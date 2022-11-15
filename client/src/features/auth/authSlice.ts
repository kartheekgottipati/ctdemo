import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { UserResponse } from "../../app/services/auth";

const initialState = {};

export const authSlice = createSlice({
  initialState,
  name: "authSlice",
  reducers: {
    setToken: (state, { payload: { token } }: PayloadAction<UserResponse>) => {
      localStorage.setItem("CoinTrackerDemoToken", token);
    },
    removeToken: (state) => {
      localStorage.removeItem("CoinTrackerDemoToken");
    },
  },
});

export const { setToken, removeToken } = authSlice.actions;
export default authSlice.reducer;
