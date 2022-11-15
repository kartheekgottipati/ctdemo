import * as React from "react";
import Box from "@mui/material/Box";
import LoadingButton from "@mui/lab/LoadingButton";
import { SubmitHandler, useForm } from "react-hook-form";
import { useAddWalletMutation } from "../../app/services/wallet";
import { useLocation, useNavigate } from "react-router-dom";
import TextField from "@mui/material/TextField";

export function AddWallet() {
  const {
    reset,
    register,
    handleSubmit,
    formState: { isSubmitSuccessful },
  } = useForm<{ address: string }>();

  const navigate = useNavigate();
  const location = useLocation();

  const from = ((location.state as any)?.from.pathname as string) || "/";
  const [addWallet, { isLoading, isError, error, isSuccess }] =
    useAddWalletMutation();

  const onSubmit: SubmitHandler<{ address: string }> = async (values) => {
    try {
      await addWallet(values).unwrap();
      navigate("/");
    } catch (err) {}
  };

  React.useEffect(() => {
    if (isSuccess) {
      navigate(from);
    }

    if (isError) {
      console.log();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLoading]);

  React.useEffect(() => {
    if (isSubmitSuccessful) {
      reset();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSubmitSuccessful]);

  return (
    <Box
      sx={{
        margin: 8,
        display: "flex",
        justifyContent: "center",
      }}
    >
      <Box
        component="form"
        onSubmit={handleSubmit(onSubmit)}
        noValidate
        sx={{ mt: 1, width: "800px" }}
      >
        <TextField
          margin="normal"
          required
          fullWidth
          id="add-wallet"
          label="Wallet Address"
          {...register("address")}
          autoComplete="off"
          autoFocus
          error={isError}
          helperText={isError ? (error as any)?.data.msg[0] : ""}
        />
        <LoadingButton
          type="submit"
          loading={isLoading}
          loadingIndicator="Loading…"
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
        >
          Add Wallet
        </LoadingButton>
      </Box>
    </Box>
  );
}
