import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { useNavigate } from "react-router-dom";
import CurrencyBitcoinIcon from "@mui/icons-material/CurrencyBitcoin";
import Box from "@mui/material/Box";
import React from "react";
import { LoadingButton as _LoadingButton } from "@mui/lab";
import { styled } from "@mui/material/styles";
import { useLogoutMutation } from "../app/services/auth";
import { removeToken } from "../features/auth/authSlice";
import { useDispatch } from "react-redux";

const LoadingButton = styled(_LoadingButton)`
  padding: 0.4rem;
  background-color: #f9d13e;
  color: #2363eb;
  font-weight: 500;
  &:hover {
    background-color: #ebc22c;
    transform: translateY(-2px);
  }
`;

export function Header() {
  const token = localStorage.getItem("CoinTrackerDemoToken");
  const logged_in = token ? true : false;
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [logout] = useLogoutMutation();

  const onLogout = async () => {
    try {
      await logout().unwrap();
      navigate("/login");
    } catch (err) {
      console.error((err as any).message);
    }
    dispatch(removeToken());
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <CurrencyBitcoinIcon sx={{ mr: 2 }} />
        <Typography
          variant="h6"
          onClick={() => navigate("/")}
          sx={{ cursor: "pointer" }}
        >
          Coin Tracker Demo
        </Typography>
        <Box display="flex" sx={{ ml: "auto" }}>
          {!logged_in && (
            <React.Fragment>
              <LoadingButton sx={{ mr: 2 }} onClick={onLogout}>
                Register
              </LoadingButton>
              <LoadingButton onClick={() => navigate("/login")}>
                Login
              </LoadingButton>
            </React.Fragment>
          )}
          {logged_in && (
            <React.Fragment>
              <LoadingButton
                sx={{ backgroundColor: "#eee" }}
                onClick={onLogout}
              >
                Logout
              </LoadingButton>
              <LoadingButton
                sx={{ backgroundColor: "#eee", ml: 2 }}
                onClick={() => navigate("/")}
              >
                Home
              </LoadingButton>
            </React.Fragment>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}
