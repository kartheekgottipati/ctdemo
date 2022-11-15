import { Navigate, useLocation } from "react-router-dom";

export default function RequireAuth({ children }: { children: JSX.Element }) {
  let token = localStorage.getItem("CoinTrackerDemoToken");
  let location = useLocation();

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
