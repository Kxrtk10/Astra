(function () {
  const nativeFetch = window.fetch.bind(window);
  const config = window.APP_CONFIG || {};
  const apiBaseUrl = String(config.api_base_url || "").trim();
  const suppressedSessionPaths = new Set([
    "/api/auth/login",
    "/api/auth/register",
    "/api/health",
    "/api/readiness",
    "/api/video-library",
    "/api/avatar-presets",
    "/api/exam-catalog",
  ]);

  function isApiPath(input) {
    return typeof input === "string" && input.startsWith("/api/");
  }

  function getAuthHeaders() {
    const token = localStorage.getItem("alt_auth_token");
    return token
      ? {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        }
      : {
          "Content-Type": "application/json",
        };
  }

  if (typeof window.getAuthHeaders !== "function") {
    window.getAuthHeaders = getAuthHeaders;
  }

  function resolveRequestPath(input) {
    if (typeof input === "string") {
      return input;
    }
    if (input && typeof input.url === "string") {
      return input.url;
    }
    return "";
  }

  function resolveApiInput(input) {
    if (!isApiPath(input) || !apiBaseUrl) {
      return input;
    }
    return `${apiBaseUrl.replace(/\/$/, "")}${input}`;
  }

  function buildHeaders(init = {}) {
    const headers = new Headers(init.headers || {});
    const authHeaders = typeof window.getAuthHeaders === "function" ? window.getAuthHeaders() : getAuthHeaders();
    Object.entries(authHeaders || {}).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        headers.set(key, value);
      }
    });

    const body = init.body;
    const hasBinaryBody =
      (typeof FormData !== "undefined" && body instanceof FormData) ||
      (typeof Blob !== "undefined" && body instanceof Blob) ||
      (typeof URLSearchParams !== "undefined" && body instanceof URLSearchParams) ||
      (typeof ArrayBuffer !== "undefined" && (body instanceof ArrayBuffer || ArrayBuffer.isView(body)));
    if (hasBinaryBody) {
      headers.delete("Content-Type");
    }
    return headers;
  }

  async function fetchWithRetry(input, init = {}, retries = 1) {
    const method = String((init && init.method) || "GET").toUpperCase();
    const allowRetry = method === "GET" || method === "HEAD" || method === "OPTIONS";
    let attempt = 0;
    const requestPath = resolveRequestPath(input);
    const requestInit = { ...init, headers: buildHeaders(init) };

    while (true) {
      try {
        const response = await nativeFetch(resolveApiInput(input), requestInit);
        if (response.status === 401 && !suppressedSessionPaths.has(requestPath) && typeof window.handleSessionExpired === "function") {
          window.handleSessionExpired();
        }
        if (!allowRetry || response.ok || response.status < 500 || attempt >= retries) {
          return response;
        }
      } catch (error) {
        if (!allowRetry || attempt >= retries) {
          throw error;
        }
      }
      attempt += 1;
    }
  }

  window.fetch = function (input, init) {
    if (!isApiPath(input)) {
      return nativeFetch(input, init);
    }
    return fetchWithRetry(input, init);
  };

  window.apiFetchJson = async function (input, init) {
    const response = await window.fetch(input, init);
    const text = await response.text();
    let payload = null;

    if (text) {
      try {
        payload = JSON.parse(text);
      } catch (error) {
        payload = text;
      }
    }

    if (!response.ok) {
      const message =
        payload && typeof payload === "object" && payload.detail
          ? payload.detail
          : `Request failed with status ${response.status}.`;
      throw new Error(message);
    }

    return payload;
  };
})();
