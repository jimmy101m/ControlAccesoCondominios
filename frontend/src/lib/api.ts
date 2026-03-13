const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api/v1";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

type ApiRequestOptions = {
  method?: HttpMethod;
  body?: unknown;
  headers?: HeadersInit;
  cache?: RequestCache;
};

export async function apiRequest<T>(
  endpoint: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const { method = "GET", body, headers, cache = "no-store" } = options;

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
    cache,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return (await response.json()) as T;
}

export const api = {
  get: <T>(endpoint: string, headers?: HeadersInit) =>
    apiRequest<T>(endpoint, { method: "GET", headers }),
  post: <T>(endpoint: string, body?: unknown, headers?: HeadersInit) =>
    apiRequest<T>(endpoint, { method: "POST", body, headers }),
  patch: <T>(endpoint: string, body?: unknown, headers?: HeadersInit) =>
    apiRequest<T>(endpoint, { method: "PATCH", body, headers }),
  put: <T>(endpoint: string, body?: unknown, headers?: HeadersInit) =>
    apiRequest<T>(endpoint, { method: "PUT", body, headers }),
  delete: <T>(endpoint: string, headers?: HeadersInit) =>
    apiRequest<T>(endpoint, { method: "DELETE", headers }),
};
