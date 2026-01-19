import { BrowserRouter } from "react-router-dom";
import { AppRouter } from "@core/router";

export default function App() {
  return (
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  );
}