import React from "react";
import { Outlet } from "react-router-dom";
import { Header } from "./Header";

export default function Layout() {
  return (
    <React.Fragment>
      <Header />
      <Outlet />
    </React.Fragment>
  );
}
