import { useEffect, useState } from "react";
import { UserType } from "../types";
import { fetchSuggestions } from "../services/feed";
import { Link } from "react-router-dom";

export default function SuggestionsSidebar() {
  const [suggestions, setSuggestions] = useState<UserType[]>([]);

  useEffect(() => {
    fetchSuggestions().then(setSuggestions);
  }, []);

  return (
    <div className="max-h-screen bg-white p-4 rounded shadow w-64">
      <h2 className="font-semibold mb-2">Sugestões para seguir</h2>
      {suggestions.length === 0 && <p>Nenhuma sugestão</p> ||
      suggestions.map((user) => (
        <Link
          to={`/profile/${user.id}`}
          key={user.id}
          className="block text-blue-600 hover:underline mb-1"
        >
          @{user.username}
        </Link>
      ))}
    </div>
  );
}
