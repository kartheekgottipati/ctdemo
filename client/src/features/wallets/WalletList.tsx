import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import React from "react";
import { useNavigate } from "react-router-dom";
import { useGetWalletsQuery } from "../../app/services/wallet";
import { Wallet } from "./Wallet";

export function WalletList() {
  const { data: wallets, isLoading } = useGetWalletsQuery();
  const navigate = useNavigate();

  if (!wallets) {
    return <div>No Wallets</div>;
  }

  if (isLoading) {
    return <div>Loading</div>;
  }

  return (
    <React.Fragment>
      <Box
        sx={{
          margin: 6,
          display: "flex",
          justifyContent: "flex-end",
          alignItems: "center",
        }}
      >
        <Button variant="contained" onClick={() => navigate("/add-wallet")}>
          Add Wallet
        </Button>
      </Box>
      <Box
        sx={{
          margin: 4,
          display: "flex",
          justifyContent: "flex-end",
          alignItems: "center",
        }}
      >
        <List dense sx={{ width: "100%" }}>
          {wallets.map((wallet) => {
            return (
              <ListItem key={wallet.id}>
                <Wallet data={wallet} />
              </ListItem>
            );
          })}
        </List>
      </Box>
    </React.Fragment>
  );
}
