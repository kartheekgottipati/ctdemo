import React from "react";
import { Route, Routes } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Layout from "./components/Layout";
import Home from "./components/Home";
import RequireAuth from "./components/RequireAuth";
import "./App.css";
import { LogIn } from "./features/auth/Login";
import { WalletList } from "./features/wallets/WalletList";
import { TransactionList } from "./features/transactions/TransactionList";
import { AddWallet } from "./features/wallets/AddWallet";

const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="login" element={<LogIn />} />
          <Route
            path=""
            element={
              <RequireAuth>
                <Home />
              </RequireAuth>
            }
          />
          <Route
            path="wallets"
            element={
              <RequireAuth>
                <WalletList />
              </RequireAuth>
            }
          />
          <Route
            path="transactions/:address"
            element={
              <RequireAuth>
                <TransactionList />
              </RequireAuth>
            }
          />
          <Route
            path="add-wallet"
            element={
              <RequireAuth>
                <AddWallet />
              </RequireAuth>
            }
          ></Route>
        </Route>
      </Routes>
    </ThemeProvider>
  );
}

export default App;
