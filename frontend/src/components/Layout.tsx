import { ReactNode, createContext } from "react";
import { Link } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import { UserType } from "../types";

type Props = {
  children: ReactNode;
};

export const UserContext = createContext({ user: {} as UserType | null });

export default function Layout({ children }: Props) {

  const { handleLogout, user } = useAuth();
  return (
    <UserContext.Provider value={{user}}>
      <div className="min-h-screen bg-gray-100">
        <header className="flex items-center justify-between bg-white shadow px-6 py-4">
          <div className="flex items-center space-x-2">
            <img src="/b2ico.svg" alt="Logo" className="w-8 h-8" />
            {/*<span className="text-xl font-bold text-blue-600">b2</span>*/}
          </div>
          <nav className="space-x-4">
            <Link to="/feed" className="text-sm hover:underline">Feed</Link>
            <Link to="/profile" className="text-sm hover:underline">Perfil {user? ` de ${user.username}` : ""}</Link>
            <button onClick={handleLogout} className="text-sm text-white bg-red-500 hover:bg-red-600 px-4 py-2 rounded" >
              Logout
            </button>
          </nav>
        </header>
        <main className="p-6">{children}</main>
      </div>
    </UserContext.Provider>
  );
}
