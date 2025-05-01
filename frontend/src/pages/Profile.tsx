// src/pages/Profile.tsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Layout from "../components/Layout";
import { PostType, UserProfileType } from "../types";
import { fetchProfileData, toggleFollow, loadPosts } from "../services/profile";
import PostCard from "../components/PostCard";
import Loader from "../components/Loader";


function getUser() {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
}

export default function Profile() {
  const { profile_id } = useParams();
  const [profile, setProfile] = useState<UserProfileType | null>(null);
  const [posts, setPosts] = useState<PostType[]>([]);
  const [loading, setLoading] = useState(true);
  const user = getUser();

  const isOwnProfile = !profile_id || profile_id === user?.id?.toString();
  let didRun = false;

  useEffect(() => {
    async function loadProfile() {
      if(!user.id) return;
      setLoading(true);
      try {
        const data = await fetchProfileData(profile_id);
        setProfile(data);
        loadPosts(profile_id || user.id).then((posts) => setPosts(posts.data.results));
      } catch (err) {
        console.error("Erro ao carregar perfil", err);
      } finally {
        setLoading(false);
      }
    }
    if(!didRun) {
      didRun = true;
      loadProfile();
    }
  }, [profile_id]);

  const handleFollow = async () => {
    if (!profile) return;
    const updated = await toggleFollow(profile);
    if (updated === undefined) return;
    setProfile({...profile, is_following: updated});
  };

  if (loading || !profile) return (
      <Layout>
        <div className="max-w-2xl mx-auto p-4">
          <Loader />
        </div>
      </Layout>
  )

  return (
    <Layout>
      <div className="max-w-2xl mx-auto p-4">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-2xl font-bold">{profile.username}</h2>
            <div className="text-sm text-gray-600">
              {profile.followers_count} seguidores · {profile.following_count} seguindo
            </div>
          </div>
          {!isOwnProfile && (
            <button
              onClick={handleFollow}
              className={`px-4 py-2 rounded ${
                profile.is_following ? "bg-red-500" : "bg-blue-500"
              } text-white`}
            >
              {profile.is_following ? "Deixar de seguir" : "Seguir"}
            </button>
          )}
        </div>

        <div className="space-y-4">
          {posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      </div>
    </Layout>
  );
}
