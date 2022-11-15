import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import * as React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { LoginResponse, useLoginMutation } from "../../app/services/auth";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputAdornment from "@mui/material/InputAdornment";
import IconButton from "@mui/material/IconButton";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import Visibility from "@mui/icons-material/Visibility";
import LoadingButton from "@mui/lab/LoadingButton";
import { useDispatch } from "react-redux";
import { setToken } from "./authSlice";

export function LogIn() {
  const {
    reset,
    register,
    handleSubmit,
    formState: { isSubmitSuccessful },
  } = useForm<LoginResponse>();

  const [passwordShown, setPasswordShown] = React.useState(false);
  const togglePasswordVisiblity = () => {
    setPasswordShown(passwordShown ? false : true);
  };
  const handleMouseDownPassword = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.preventDefault();
  };

  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();

  const from = ((location.state as any)?.from.pathname as string) || "/";

  const [login, { isLoading, isError, error, isSuccess }] = useLoginMutation();
  const onSubmit: SubmitHandler<LoginResponse> = async (values) => {
    console.log("Login input data: ", values);
    try {
      const userResponse = await login(values).unwrap();
      dispatch(setToken(userResponse));
    } catch (err) {
      console.error((err as any).message);
    }
  };

  React.useEffect(() => {
    if (isSuccess) {
      console.log(from);
      navigate(from);
    }

    if (isError) {
      if (Array.isArray((error as any).data.error)) {
        (error as any).data.error.forEach((el: any) => {
          console.error(el.message);
        });
      } else {
        console.error((error as any).data.message);
      }
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
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign In
        </Typography>
        <Box
          component="form"
          noValidate
          onSubmit={handleSubmit(onSubmit)}
          sx={{ mt: 3 }}
        >
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                id="username"
                label="User Name"
                autoComplete="username"
                {...register("username")}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl variant="outlined" fullWidth>
                <InputLabel htmlFor="outlined-adornment-password">
                  Password
                </InputLabel>
                <OutlinedInput
                  id="outlined-adornment-password"
                  type={passwordShown ? "text" : "password"}
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={togglePasswordVisiblity}
                        onMouseDown={handleMouseDownPassword}
                        edge="end"
                      >
                        {passwordShown ? <Visibility /> : <VisibilityOff />}
                      </IconButton>
                    </InputAdornment>
                  }
                  autoComplete="current-password"
                  {...register("password")}
                  label="Password"
                />
              </FormControl>
            </Grid>
          </Grid>
          <LoadingButton
            type="submit"
            loading={isLoading}
            loadingIndicator="Loading…"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign In
          </LoadingButton>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link to="/signup">Don't have an account? Sign Up</Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}
