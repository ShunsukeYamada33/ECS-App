import {Routes, Route} from "react-router-dom";
import Login from "./pages/Login.tsx";
import Callback from "./pages/Callback.tsx";
import Chat from "./pages/Chat.tsx";

function App() {
    return (
        <Routes>
            <Route path="/" element={<Login/>}/>
            <Route path="/callback" element={<Callback/>}/>
            <Route path="/chat" element={<Chat/>}/>
        </Routes>
    );
}

export default App;
