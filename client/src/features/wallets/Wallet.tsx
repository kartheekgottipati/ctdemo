import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardActionArea from "@mui/material/CardActionArea";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { Link, useNavigate } from "react-router-dom";
import { Wallet as WalletData } from "../../app/services/wallet";
import {
  useDeleteWalletMutation,
  useSyncWalletMutation,
} from "../../app/services/wallet";

type WalletProps = {
  data: WalletData;
};

export function Wallet(props: WalletProps) {
  const { data } = props;
  const navigate = useNavigate();
  const [deleteWallet] = useDeleteWalletMutation();
  const [syncWallet] = useSyncWalletMutation();

  const onDeleteClick = async () => {
    deleteWallet(data.address);
    navigate("/");
  };

  const onSyncClick = async () => {
    const syncResponse = await syncWallet(data.address).unwrap();
    console.log(syncResponse);
  };

  return (
    <Card sx={{ display: "flex", width: "100%" }}>
      <CardActionArea component={Link} to={`/transactions/${data.address}`}>
        <CardContent>
          <Typography component="div" variant="h5">
            Address: {data.address}
          </Typography>
          <Typography
            variant="subtitle1"
            color="text.secondary"
            component="div"
          >
            Balance: {data.final_balance} Transactions: {data.transaction_count}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions
        sx={{ display: "block", justifyContent: "start", alignItems: "start" }}
      >
        <Button size="small" color="error" onClick={onDeleteClick}>
          Delete
        </Button>
        <Button size="small" color="primary" onClick={onSyncClick}>
          Sync
        </Button>
      </CardActions>
    </Card>
  );
}
