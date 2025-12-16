import {apiFetch} from "../auth/client.ts";

function Chat() {
    const accessToken = localStorage.getItem("access_token");

    const callSecure = async () => {
        const res = await apiFetch("/api/secure");
        const data = await res.json();
        alert(data.message);
    };


    return (
        <div style={{padding: 30}}>
            <h1>Chat Page</h1>
            <p>JWT exists: {accessToken ? "YES" : "NO"}</p>
            <button onClick={callSecure}>Call Secure API</button>
        </div>
    );
}

export default Chat;