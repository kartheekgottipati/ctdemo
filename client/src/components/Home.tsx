import * as React from "react";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import { WalletList } from "../features/wallets/WalletList";

export default function Home() {
  return (
    <Box sx={{ flexGrow: 1, m: 4 }}>
      <Grid
        spacing={2}
        sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}
      >
        <Grid item md={10} xs={12}>
          <WalletList />
        </Grid>
      </Grid>
    </Box>
  );
}
