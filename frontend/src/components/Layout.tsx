import { ReactNode, useState } from "react";
import { Link } from "react-router-dom";
import { handleLogout } from "../services/auth";
import UserContextProvider from "./UserContext";
import SuggestionsSidebar from "./SuggestionsSidebar";
import { Menu, X } from "lucide-react";

type Props = {
  children: ReactNode;
};

export default function Layout({ children }: Props) {
  const [showSidebar, setShowSidebar] = useState(false);

  const onLogout = async () => {
    const success = await handleLogout();
    if (success) {
      window.location.href = "/login";
    }
  };

  return (
    <UserContextProvider>
      <div className="min-h-screen bg-gray-100 relative">
        <header className="flex items-center justify-between bg-white shadow px-6 py-4">
          <div className="flex items-center space-x-2">
            <img src="/b2ico.svg" alt="Logo" className="w-8 h-8" />
          </div>
          <nav className="space-x-4">
            <Link to="/feed" className="text-sm hover:underline">
              Feed
            </Link>
            <Link to="/profile" className="text-sm hover:underline">
              Perfil
            </Link>
            <button
              onClick={onLogout}
              className="text-sm text-white bg-red-500 hover:bg-red-600 px-4 py-2 rounded"
            >
              Logout
            </button>
          </nav>
        </header>

        <main className="flex flex-col md:flex-row max-w-6xl mx-auto mt-6 px-4 gap-6">
          <div className="flex-1 order-1 md:order-none">{children}</div>

          {/* Sidebar no modo normal */}
          <div className="hidden md:block w-64">
            <SuggestionsSidebar />
          </div>
        </main>

        {/* Sidebar flutuante para telas pequenas */}
        <div
          className={`fixed top-0 right-0 h-full w-64 bg-white shadow-lg z-50 p-4 transition-transform duration-300 md:hidden ${
            showSidebar ? "translate-x-0" : "translate-x-full"
          }`}
        >
          <button
            className="mb-4 text-sm text-gray-500 hover:text-black"
            onClick={() => setShowSidebar(false)}
          >
            <X className="w-6 h-6" />
          </button>
          <SuggestionsSidebar />
        </div>

        {/* Botão flutuante */}
        {!showSidebar && (
          <button
            className="fixed bottom-4 right-4 z-50 bg-blue-600 text-white p-3 rounded-full shadow-lg md:hidden"
            onClick={() => setShowSidebar(true)}
          >
            <Menu className="w-6 h-6" />
          </button>
        )}
      </div>
    </UserContextProvider>
  );
}
