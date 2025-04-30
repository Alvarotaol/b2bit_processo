import { useEffect, useState } from "react";
import { fetchFeed } from "../services/feed";
import { PostType } from "../types";
import Loader from "../components/Loader";
import Layout from "../components/Layout";
import PostCard from "../components/PostCard";
import { useNavigate } from "react-router-dom";
import NewPostForm from "../components/NewPostForm";

export default function Feed() {
  const [posts, setPosts] = useState<PostType[]>([]);
  const [nextUrl, setNextUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigator = useNavigate();
  let didRun = false;

  async function loadFeed(url?: string) {

    try {
      setLoading(true);
      const response = await fetchFeed(url);
      //const response = {data: {next: null, results: []}}
      setPosts((prev) => [...prev, ...response.data.results]);
      setNextUrl(response.data.next);
    } catch (err: any) {
      if(err.response.status === 401) {
        navigator("/login");
      }
      setError("Erro ao carregar feed");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!didRun) {
      //setDidRun(true);
      didRun = true;
      loadFeed();
    }
  }, []);

  if (loading && posts.length === 0) return <Loader />;

  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <Layout>
      <div className="max-w-2xl mx-auto font-semibold mb-4 text-center">
        <NewPostForm onPostCreated={(post) => setPosts([post, ...posts])} />
      </div>
      <div className="max-w-2xl mx-auto p-4">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
        {nextUrl && (
          <button
            onClick={() => loadFeed(nextUrl)}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            disabled={loading}
          >
            {loading ? "Carregando..." : "Carregar mais"}
          </button>
        ) || <div className="text-gray-500 text-center">Fim dos posts</div>}
      </div>
    </Layout>
  );
}
