import { useState } from "react";
import { updatePost } from "../services/feed";
import { PostType } from "../types";
import { ImageIcon } from "lucide-react";

interface Props {
  post: PostType;
  onClose: () => void;
  onUpdated: (post: PostType) => void;
}

export default function EditPostModal({ post, onClose, onUpdated }: Props) {
  const [text, setText] = useState(post.text);
  const [imageEdit, setImageEdit] = useState<File | null>(null);
  const [removeImage, setRemoveImage] = useState(false);

  const hasExistingImage = post.image && !removeImage;

  async function handleSubmit() {
    const formData = new FormData();
    formData.append("text", text);
    if (imageEdit) {
      formData.append("image", imageEdit);
    } else if (removeImage) {
      formData.append("image", "");
    }

    for (const [key, value] of formData) {
      console.log(key, value);
    }

    try {
      const res = await updatePost(post.id, formData);
      onUpdated(res.data);
      onClose();
    } catch (err) {
      console.error("Erro ao atualizar post", err);
    }
  }

  return (
    <>
      <div className="fixed inset-0 bg-black opacity-75 flex items-center justify-center z-50"></div>
      <div className="fixed inset-0 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg w-full max-w-md shadow-lg">
          <h2 className="text-xl font-bold mb-4">Editar Post</h2>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full border p-2 rounded mb-3"
          />
          {hasExistingImage && (
            <div className="mb-3">
              <img
                src={post.image}
                alt="Imagem do post"
                className="w-32 h-32 object-cover rounded mb-1"
              />
              <button
                className="text-sm text-red-500"
                onClick={() => setRemoveImage(true)}
              >
                Remover imagem
              </button>
            </div>
          )}
          {!hasExistingImage && (
            <>
              {!imageEdit && (
                <div>
                  <label htmlFor={"file-upload"+post.id} className="cursor-pointer inline-flex items-center gap-2 text-blue-600 hover:underline">
                    <ImageIcon />
                  </label>
                  <input
                    id={"file-upload"+post.id}
                    type="file"
                    accept="image/*"
                    onChange={(e) => setImageEdit(e.target.files?.[0] || null)}
                    className="hidden"
                  />
                </div>
              )}
              {imageEdit && (
                <div className="mb-3">
                  <img
                    src={URL.createObjectURL(imageEdit)}
                    alt="Imagem do post"
                    className="w-32 h-32 object-cover rounded mb-1"
                  />
                  <button
                    className="text-sm text-red-500"
                    onClick={() => setImageEdit(null)}
                  >
                    Remover imagem
                  </button>
                </div>
              )}
            </>
          )}
          <div className="flex justify-end gap-2">
            <button onClick={onClose} className="text-gray-500">Cancelar</button>
            <button onClick={handleSubmit} className="bg-blue-500 text-white px-4 py-2 rounded">
              Salvar
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
