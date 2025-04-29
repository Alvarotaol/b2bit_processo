import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signup } from "../services/auth";

export default function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
  email: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      await signup(formData);
      navigate("/login"); // Redireciona pro login após cadastro
    } catch (err: any) {
      setError(err.response?.data?.message || "Erro ao criar conta");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Criar Conta</h2>

        {error && <div className="text-red-500 mb-4">{error}</div>}

        <div className="mb-4">
          <label className="block mb-1 text-gray-700" htmlFor="username">
            Usuário
          </label>
          <input
            id="username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2"
            required
          />
        </div>

    <div className="mb-4">
      <label className="block mb-1 text-gray-700" htmlFor="email">
      Email
      </label>
      <input
      id="email"
      name="email"
      type="email"
      value={formData.email}
      onChange={handleChange}
      className="w-full border border-gray-300 rounded px-3 py-2"
      required
      />
    </div>

        <div className="mb-6">
          <label className="block mb-1 text-gray-700" htmlFor="password">
            Senha
          </label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Criar Conta
        </button>
      </form>
    </div>
  );
}
