import {useEffect, useRef} from "react";
import {useLocation, useNavigate} from "react-router-dom";
import {exchangeCode} from "../auth/auth.ts";

function Callback() {
    const location = useLocation();
    const navigate = useNavigate();
    const executedRef = useRef(false);

    useEffect(() => {
        if (executedRef.current) return;
        executedRef.current = true;

        // 今のURLを取得
        const params = new URLSearchParams(location.search);

        // ?code=xxxx を取り出す
        const code = params.get("code");

        // code がない場合はリターン
        if (!code) return;

        // トークンの取得
        exchangeCode(code).then((data) => {
            localStorage.setItem("id_token", data.id_token);
            localStorage.setItem("access_token", data.access_token);
            navigate("/chat");
        });
    }, []);

    return <h1>ログイン処理中...</h1>;
}

export default Callback;
