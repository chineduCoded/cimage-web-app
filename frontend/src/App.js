import "./App.css"
import HomeScreen from "./pages/homeScreen";
import { Toaster } from "react-hot-toast"


function App() {
  return (
    <div className="App">
      <Toaster position="bottom-right" reverseOrder={false} />
      <HomeScreen />
    </div>
  );
}

export default App;
