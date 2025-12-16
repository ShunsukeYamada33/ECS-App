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
    const accessToken = localStorage.getItem("access_token");
    let res = await fetch(url, {
        ...options,
        headers: {
            ...(options.headers || {}),
            Authorization: `Bearer ${accessToken}`,
        },
        credentials: "include",
    });


    if (res.status === 401) {
        // access_token 期限切れ → refresh
        const refreshRes = await fetch("/api/auth/refresh", {
            method: "POST",
            credentials: "include",
        });

        if (!refreshRes.ok) {
            window.location.href = "/";
            throw new Error("Session expired");
        }

        const data = await refreshRes.json();
        localStorage.setItem("access_token", data.access_token);

        // 再試行
        res = await fetch(url, {
            ...options,
            headers: {
                Authorization: `Bearer ${data.access_token}`,
            },
            credentials: "include",
        });
    }

    return res;
}