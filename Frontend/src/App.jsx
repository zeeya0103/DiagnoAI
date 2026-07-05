import { BrowserRouter } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { AuthProvider } from "./context/AuthContext";
import AppRoutes from "./routes/AppRoutes";

import "./styles/globals.css";
import "./styles/colors.css";
import "./styles/animations.css";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />

        <Toaster
          position="top-right"
          reverseOrder={false}
          toastOptions={{
            duration: 3000,
          }}
        />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;