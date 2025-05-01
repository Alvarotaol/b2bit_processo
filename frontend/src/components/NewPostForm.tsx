import { useState } from "react";
import { PostType } from "../types";
import { sendPost } from "../services/feed";
import { ImageIcon } from "lucide-react";

type Props = {
  onPostCreated: (post: PostType) => void;
};

export default function NewPostForm({ onPostCreated }: Props) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [image, setImage] = useState<File | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!text.trim() && !image) return;

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("text", text);
      if (image) {
        formData.append("image", image);
      }
      const response = await sendPost(formData);
      onPostCreated(response.data);
      setText("");
      setImage(null);
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
      <div className="flex justify-between mt-2">
        {!image && <><label htmlFor="file-upload" className="cursor-pointer inline-flex items-center gap-2 text-blue-600 hover:underline">
          <ImageIcon />
        </label>
        <input
          id="file-upload"
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files?.[0] || null)}
          className="hidden"
        /></>}
        {
          image && (
            <span className="flex gap-2"><img src={URL.createObjectURL(image)} alt="Preview" className="w-12 h-12 object-cover rounded" />
            <button type="button" onClick={() => setImage(null)}>Remover</button>
            </span>
          )
        }
        <button
          type="submit"
          disabled={loading}
          className="mt-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
          {loading ? "Publicando..." : "Publicar"}
        </button>
        </div>
    </form>
  );
}
