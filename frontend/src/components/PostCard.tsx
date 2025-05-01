import React, { useState } from "react";
import { PostType } from "../types";
import { Heart } from "lucide-react";
import { sendLike, deletePost } from "../services/feed";
import { UserContext } from "../components/UserContext";
import { Link } from "react-router-dom";
import EditPostModal from "./EditPostModal";

type PostProps = {
  post: PostType;
};

const PostCard: React.FC<PostProps> = ({ post }) => {
  const [like_count, setLikes] = useState(post.like_count);
  const [liked, setLiked] = useState(post.has_liked);
  const [currentPost, setCurrentPost] = useState<PostType | null>(null);
  const user = React.useContext(UserContext);

  const onLike = async () => {
    try {
      const success = await sendLike(post.id);
      if(success) {
        setLikes((prev) => (liked ? prev - 1 : prev + 1));
        setLiked(!liked);
      }
    } catch (error: any) {
      console.error("Erro ao curtir o post", error);
    }
  };

  const handleUpdate = (post: PostType) => {
    setCurrentPost(post);
    window.location.reload();
  }
  const onDelete = async () => {
    const success = await deletePost(post.id);
    if(success) {
      window.location.reload();
    }
  };

  return (
    <>
      <div className="border rounded-2xl p-4 shadow-sm mb-4 bg-white flex flex-col gap-2">
        <div className="flex justify-between items-center">
          <div className="text-sm font-semibold">
            <Link to={`/profile/${post.user_id}`}>{post.username}</Link>
            <span className="text-gray-500 text-xs ml-2">
              {new Date(post.created_at).toLocaleString()}
            </span>
          </div>
          {user && post.user_id === user.id  && (
            <span>
              <button className="text-red-500 text-sm hover:underline" onClick={onDelete}>
                Excluir
              </button>
              <button onClick={() => setCurrentPost(post)} className="text-blue-500 text-sm">Editar</button>
            </span>
          )}
        </div>
        <div className="text-gray-800">{post.text}</div>
        {post.image && <img src={post.image} alt="" />}
        <div className="flex justify-between items-center mt-2">
          <button onClick={onLike} className="text-blue-500 text-sm hover:underline flex items-center">
            <Heart className={liked ? "fill-red-500 mr1" : "mr1"} /> {` ${like_count}`}
          </button>
        </div>
      </div>
      {currentPost && currentPost && <EditPostModal post={currentPost} onClose={() => setCurrentPost(null)} onUpdated={handleUpdate} />}
    </>
  );
};

export default PostCard;
