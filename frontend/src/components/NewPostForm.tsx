import { useState } from "react";
import { PostType } from "../types";
import { sendPost } from "../services/feed";

type Props = {
  onPostCreated: (post: PostType) => void;
};

export default function NewPostForm({ onPostCreated }: Props) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!text.trim()) return;

    try {
      setLoading(true);
      const response = await sendPost(text);
      onPostCreated(response.data);
      setText("");
    } catch (err: any) {
      setError("Erro ao publicar");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mb-4 p-4 border rounded bg-white shadow">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="No que você está pensando?"
        className="w-full p-2 border rounded resize-none"
        rows={3}
      />
      {error && <div className="text-red-500 text-sm mt-1">{error}</div>}
      <button
        type="submit"
        disabled={loading}
        className="mt-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        {loading ? "Publicando..." : "Publicar"}
      </button>
    </form>
  );
}
