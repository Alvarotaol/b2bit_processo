import { useEffect, useRef, useState } from "react";
import { fetchFeed, searchFeed } from "../services/feed";
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
  const [searchTerm, setSearchTerm] = useState("");
  const navigator = useNavigate();
  const loaderRef = useRef<HTMLDivElement | null>(null);

  let didRun = false;

  async function loadFeed(url?: string) {
    try {
      setLoading(true);
      const response = await fetchFeed(url);
      setPosts((prev) => [...prev, ...response.data.results]);
      setNextUrl(response.data.next);
    } catch (err: any) {
      if (err.response?.status === 401) {
        navigator("/login");
      }
      setError("Erro ao carregar feed");
    } finally {
      setLoading(false);
    }
  }

  async function searchPosts() {
    try {
      setLoading(true);
      const response = await searchFeed(searchTerm);
      setPosts(response.data.results);
      setNextUrl(null);
    } catch (err: any) {
      if (err.response?.status === 401) {
        navigator("/login");
      }
      setError("Erro ao carregar feed");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (didRun) return;
    didRun = true;
    if (searchTerm) {
      searchPosts();
    } else {
      loadFeed();
    }
  }, [searchTerm]);

  // Observa o loaderRef
  useEffect(() => {
    if (!nextUrl || loading) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadFeed(nextUrl);
        }
      },
      { threshold: 1.0 }
    );

    const el = loaderRef.current;
    if (el) observer.observe(el);

    return () => {
      if (el) observer.unobserve(el);
    };
  }, [nextUrl, loading]);

  if (loading && posts.length === 0) return <Loader />;

  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <Layout>
      <div className="max-w-2xl mx-auto font-semibold mb-4 text-center">
        <NewPostForm onPostCreated={(post) => setPosts([post, ...posts])} />
      </div>
      <div className="max-w-2xl mx-auto p-4">
      <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="mb-4 p-2 w-full border border-gray-300 rounded"
          placeholder="Buscar por palavras-chave"
        />
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}

        <div ref={loaderRef} className="h-10" />

        {loading && <div className="text-center my-4">Carregando...</div>}

        {!nextUrl && !loading && (
          <div className="text-gray-500 text-center mt-4">Fim dos posts</div>
        )}
      </div>
    </Layout>
  );
}
