import React, {createContext, useState} from "react";

export type AuthContextType = {
    accessToken: string | null;
    isAuthenticated: boolean;
    login: (token: string) => void;
    logout: () => void;
};

const AuthContext =
    createContext<AuthContextType | undefined>(undefined);
export default AuthContext

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
    const [accessToken, setAccessToken] = useState<string | null>(() => {
        return localStorage.getItem("access_token");
    });

    const login = (token: string) => {
        localStorage.setItem("access_token", token);
        setAccessToken(token);
    };

    const logout = () => {
        localStorage.removeItem("access_token");
        setAccessToken(null);
    };

    return (
        <AuthContext.Provider
            value={{
                accessToken,
                isAuthenticated: !!accessToken,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
