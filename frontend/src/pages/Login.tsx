import {
    COGNITO_DOMAIN,
    COGNITO_CLIENT_ID,
    REDIRECT_URI,
} from "../auth/auth.ts";

function Login() {
    const login = () => {
        window.location.href =
            `${COGNITO_DOMAIN}/login?` +
            `response_type=code&` +
            `client_id=${COGNITO_CLIENT_ID}&` +
            `scope=openid+email&` +
            `redirect_uri=${encodeURIComponent(REDIRECT_URI)}`;
    };

    return (
        <div style={{padding: 30}}>
            <h1>JWT Auth Chat</h1>
            <button onClick={login}>Login</button>
        </div>
    );
}

export default Login;

