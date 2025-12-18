import {refreshAccessToken} from "./auth.ts";

/**
 * 指定されたAPIエンドポイントからデータを取得し、アクセストークンによる認証を自動的に処理
 * アクセストークンが期限切れの場合、トークンの更新を試行し、フェッチリクエストを再試行
 *
 * @param {string} url - データを取得するためのAPIエンドポイント
 * @param {RequestInit} [options={}] - フェッチリクエストのオプション設定（メソッド、ヘッダー、ボディなど）
 * @return {Promise<Response>} APIからの応答
 * @throws {Error} ユーザーが未認証の場合、トークンの更新に失敗すると、ログインページへのリダイレクトが発生
 */
export async function apiFetch(
    url: string,
    options: RequestInit = {}
): Promise<Response> {
    let res = await fetch(url, {
        ...options,
        headers: {
            ...(options.headers || {}),
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        credentials: "include",
    });


    if (res.status === 401) {
        // access_token 期限切れ → refresh
        const refreshed = refreshAccessToken();

        if (!refreshed) {
            window.location.href = "/";
            throw new Error("Session expired");
        }

        // 再試行
        res = await fetch(url, {
            ...options,
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            credentials: "include",
        });
    }

    return res;
}