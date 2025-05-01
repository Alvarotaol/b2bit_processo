import Api from "./http";

async function fetchFeed(url?: string) {
  return Api.get(url || "http://localhost:8000/api/feed/");
}

async function sendLike(postId: number) {
  try {
    Api.post(`/posts/${postId}/like/`);
    return true;
  } catch (error: any) {
    console.error("Erro ao curtir o post", error);
    return false;
  }
  return false;
}

async function deletePost(postId: number) {
  try {
    Api.delete(`/posts/${postId}/`);
    return true;
  } catch (error: any) {
    console.error("Erro ao deletar o post", error);
    return false;
  }
  return false;
}

async function sendPost(formData: FormData) {
  const response = await Api.post(`/posts/`, formData);
  return response;
}

async function fetchSuggestions() {
  const response = await Api.get("users/suggestions/");
  return response.data;
}

export { fetchFeed, sendPost,sendLike, deletePost, fetchSuggestions };