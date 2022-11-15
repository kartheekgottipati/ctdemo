import * as React from "react";
import Box from "@mui/material/Box";
import ListItem from "@mui/material/ListItem";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import { useParams } from "react-router-dom";
import { useGetTransactionsQuery } from "../../app/services/transaction";
import { Transaction } from "./Transaction";

export function TransactionList() {
  let [page, setPage] = React.useState(1);

  let limit = 10;
  let [offset, setOffset] = React.useState(0);

  const { address } = useParams<{ address: any }>();
  const { data, isLoading } = useGetTransactionsQuery({
    address,
    limit,
    offset,
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!data?.results.length) {
    return (
      <Box sx={{ m: 2, display: "flex", justifyContent: "center" }}>
        No transactions
      </Box>
    );
  }

  const handleChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
    setOffset(limit * (value - 1));
  };

  return (
    <Box sx={{ flexGrow: 1, m: 4 }}>
      {data?.results.map((transaction) => {
        return (
          <ListItem key={transaction.id}>
            <Transaction data={transaction} />
          </ListItem>
        );
      })}
      {data?.count > 0 ? (
        <Stack spacing={2}>
          <Pagination
            count={Math.ceil(data?.count / limit)}
            page={page}
            onChange={handleChange}
            variant="outlined"
            shape="rounded"
          />
        </Stack>
      ) : (
        <></>
      )}
    </Box>
  );
}
