export const COGNITO_DOMAIN =
    import.meta.env.VITE_COGNITO_DOMAIN;

export const COGNITO_CLIENT_ID =
    import.meta.env.VITE_COGNITO_CLIENT_ID;

export const REDIRECT_URI =
    import.meta.env.VITE_REDIRECT_URI;

/**
 * 保存されたリフレッシュトークンを使用してアクセストークンを更新
 * ローカルストレージから`refresh_token`を取得し、
 * リフレッシュエンドポイントから新しいアクセストークンをリクエストするために使用
 * 成功した場合、新しいアクセストークンはローカルストレージに保存
 *
 * @return {Promise<boolean>} トークンの更新が成功した場合に `true` を返し、失敗した場合に `false`
 */
export async function refreshAccessToken(): Promise<boolean> {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) return false;

    const res = await fetch("/api/auth/refresh", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({refresh_token: refreshToken}),
    });

    if (!res.ok) return false;

    const data = await res.json();
    localStorage.setItem("access_token", data.access_token);
    return true;
}

/**
 * 指定されたAPIエンドポイントにPOSTリクエストを送信し、認証コードをアクセストークンと交換
 *
 * @param {string} code - 交換される認証コード
 * @return {Promise<any>} JSONオブジェクトを返却
 * @throws {Error} 応答ステータスが成功していない場合（OK以外）
 */
export async function exchangeCode(code: string) {
    const res = await fetch("/api/auth/callback", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code}),
    });

    if (!res.ok) {
        throw new Error("Auth failed");
    }

    return res.json();
}
