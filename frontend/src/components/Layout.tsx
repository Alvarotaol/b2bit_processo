import { ReactNode } from "react";
import { Link } from "react-router-dom";
import { handleLogout } from "../services/auth";
import UserContextProvider from "./UserContext";
import SuggestionsSidebar from "./SuggestionsSidebar";

type Props = {
  children: ReactNode;
};

export default function Layout({ children }: Props) {

  const onLogout = async () => {
    const success = await handleLogout();
    if(success) {
      window.location.href = "/login";
    }
  };

  return (
    <UserContextProvider>
      <div className="min-h-screen bg-gray-100">
        <header className="flex items-center justify-between bg-white shadow px-6 py-4">
          <div className="flex items-center space-x-2">
            <img src="/b2ico.svg" alt="Logo" className="w-8 h-8" />
            {/*<span className="text-xl font-bold text-blue-600">b2</span>*/}
          </div>
          <nav className="space-x-4">
            <Link to="/feed" className="text-sm hover:underline">Feed</Link>
            <Link to="/profile" className="text-sm hover:underline">Perfil</Link>
            <button onClick={onLogout} className="text-sm text-white bg-red-500 hover:bg-red-600 px-4 py-2 rounded" >
              Logout
            </button>
          </nav>
        </header>
        <main className="flex max-w-6xl mx-auto mt-6 px-4 gap-6">
          <div className="flex-1">{children}</div>
          <SuggestionsSidebar />
        </main>
      </div>
    </UserContextProvider>
  );
}
